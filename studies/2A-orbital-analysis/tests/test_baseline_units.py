"""Focused parser, geometry, event and statistics tests; no orbital propagation."""
import copy
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from atlas_analysis.oem import read_oem
from atlas_analysis.geometry import Orbit, geodetic, normal_at
from atlas_analysis.optical_access import along_crossings,event_window,angles
from atlas_analysis.metrics import exact_gap_statistics,rolling_fractions
from atlas_analysis.provenance import new_run_directory,sha256

OEM="""CCSDS_OEM_VERS = 1.0
META_START
OBJECT_NAME = Test
CENTER_NAME = Earth
REF_FRAME = EME2000
TIME_SYSTEM = UTC
START_TIME = 2026-10-20T12:00:00.000
STOP_TIME = 2026-10-20T12:00:30.000
META_STOP
2026-10-20T12:00:00.000 6928 0 0 0 7.5 0
2026-10-20T12:00:30.000 6924 225 0 -0.24 7.49 0
"""
class OEMTests(unittest.TestCase):
    def parse(self,text):
        with tempfile.TemporaryDirectory(dir=ROOT/"tests") as folder:
            path=Path(folder)/"input.oem"
            path.write_text(text,encoding="utf-8")
            return read_oem(path)
    def test_valid_contract_units_are_km(self):
        ephemeris=self.parse(OEM)
        self.assertEqual(ephemeris.times[-1],30)
        self.assertEqual(ephemeris.epoch,datetime(2026,10,20,12,tzinfo=timezone.utc))
    def test_reject_wrong_frame(self):
        with self.assertRaises(ValueError): self.parse(OEM.replace("EME2000","ITRF93"))
    def test_reject_wrong_time_system(self):
        with self.assertRaises(ValueError): self.parse(OEM.replace("TIME_SYSTEM = UTC","TIME_SYSTEM = TAI"))
    def test_reject_wrong_units(self):
        with self.assertRaises(ValueError): self.parse(OEM.replace("META_STOP","STATE_UNITS = m, m/s\nMETA_STOP"))
    def test_reject_truncated_export(self):
        with self.assertRaises(ValueError): self.parse(OEM.replace("STOP_TIME = 2026-10-20T12:00:30","STOP_TIME = 2026-10-21T12:00:30"))
    def test_reject_duplicate_epoch(self):
        with self.assertRaises(ValueError): self.parse(OEM.replace("2026-10-20T12:00:30.000 6924","2026-10-20T12:00:00.000 6924"))
    def test_reject_nan_state(self):
        with self.assertRaises(ValueError): self.parse(OEM.replace("6928 0","nan 0"))
    def test_reject_multiple_segments(self):
        with self.assertRaises(ValueError): self.parse(OEM+OEM)
    def test_accept_other_year(self):
        self.assertEqual(self.parse(OEM.replace("2026","2027")).epoch.year,2027)

class OEMContractTests(unittest.TestCase):
    def contract_read(self,contract):
        with tempfile.TemporaryDirectory(dir=ROOT/"tests") as folder:
            path=Path(folder)/"input.oem"
            path.write_text(OEM,encoding="utf-8")
            return read_oem(path,contract)
    def test_epoch_contract(self):
        with self.assertRaises(ValueError):
            self.contract_read(dict(expected_start_utc="2027-10-20T12:00:00Z",expected_duration_s=30,max_sample_gap_s=30.001))
    def test_duration_contract(self):
        with self.assertRaises(ValueError):
            self.contract_read(dict(expected_start_utc="2026-10-20T12:00:00Z",expected_duration_s=60,max_sample_gap_s=30.001))
    def test_cadence_contract(self):
        with self.assertRaises(ValueError):
            self.contract_read(dict(expected_start_utc="2026-10-20T12:00:00Z",expected_duration_s=30,max_sample_gap_s=15))

class GeometryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.optical=json.loads((ROOT/"config/optical_geometry.json").read_text(encoding="utf-8-sig"))["optical"]
        cls.q=geodetic(30.1,-9.5)
        normal=normal_at(30.1,-9.5)
        east=np.array([-np.sin(np.radians(-9.5)),np.cos(np.radians(-9.5)),0])
        cls.normal=normal
        cls.times=np.array([0.,30.])
        # Artificial linear terrestrial test trajectory, not an orbital prediction.
        r=np.array([cls.q+550*normal+(t-15)*7.5*east for t in cls.times])
        state=np.c_[r,np.tile(7.5*east,(2,1))]
        cls.orbit=Orbit(cls.times,state,cls.optical)
    def test_no_extrapolation(self):
        with self.assertRaises(ValueError): self.orbit.rv(-1)
    def test_millisecond_window_between_samples(self):
        roots=along_crossings(self.orbit,self.q)
        self.assertEqual(len(roots),1)
        self.assertAlmostEqual(roots[0],15,places=6)
        result=event_window(self.orbit,self.q,self.normal,roots[0],30,0)
        self.assertIsNotNone(result)
        self.assertLess(result[1]-result[0],.002)
        # Neither 30-second endpoint sees the target's narrow along-track slit.
        half=np.arctan(.005/550)
        self.assertTrue(all(abs(angles(self.orbit,t,self.q,0)[1])>half for t in self.times))
    def endpoint_orbit(self,center_time):
        east=np.array([-np.sin(np.radians(-9.5)),np.cos(np.radians(-9.5)),0])
        r=np.array([self.q+550*self.normal+(t-center_time)*7.5*east for t in self.times])
        return Orbit(self.times,np.c_[r,np.tile(7.5*east,(2,1))],self.optical)
    def test_window_clipped_at_start_when_center_precedes_ephemeris(self):
        orbit=self.endpoint_orbit(-.0005)
        roots=along_crossings(orbit,self.q)
        self.assertEqual(roots,[0.])
        win=event_window(orbit,self.q,self.normal,roots[0],30,0)
        self.assertEqual(win[0],0.)
        self.assertGreater(win[1],0.)
    def test_window_clipped_at_end_when_center_follows_ephemeris(self):
        orbit=self.endpoint_orbit(30.0005)
        roots=along_crossings(orbit,self.q)
        self.assertEqual(roots,[30.])
        win=event_window(orbit,self.q,self.normal,roots[0],30,0)
        self.assertLess(win[0],30.)
        self.assertEqual(win[1],30.)
    def test_local_axes_are_orthonormal(self):
        _,n,a,c=self.orbit.axes(15.)
        np.testing.assert_allclose(np.array([n,a,c])@np.array([n,a,c]).T,np.eye(3),atol=1e-14)
    def test_forward_ray_inverse_angles_near_cross_boundary(self):
        _,n,a,c=self.orbit.axes(15.)
        r=self.orbit.rv(15)[0]
        limit=np.arctan(15/550)
        from atlas_analysis.geometry import A,B
        scale=np.array([A,A,B])
        for sign in (-1,1):
            for epsilon in (-2e-7,2e-7):
                theta=sign*(limit+epsilon)
                ray=n+np.tan(theta)*c
                rr=r/scale
                dr=ray/scale
                roots=np.roots([dr@dr,2*(rr@dr),rr@rr-1])
                point=r+min(x.real for x in roots if abs(x.imag)<1e-10 and x.real>0)*ray
                alpha,beta,_=angles(self.orbit,15,point,0)
                self.assertEqual(abs(alpha)<=limit,epsilon<0)
                self.assertLess(abs(beta),1e-14)
                window=event_window(self.orbit,point,point/scale**2,15.,30,0)
                self.assertEqual(window is not None,epsilon<0)

class MetricTests(unittest.TestCase):
    def test_no_access_is_censored_not_complete_gap(self):
        result=exact_gap_statistics([],30*86400)
        self.assertIsNone(result["maximum_complete_gap_h"])
        self.assertEqual(result["no_access_span_h"],720)
        self.assertTrue(result["observed_72h_failure"])
    def test_exact_gap_uses_exit_to_entry(self):
        result=exact_gap_statistics([dict(entry_s=0,exit_s=20),dict(entry_s=80,exit_s=100)],100)
        self.assertAlmostEqual(result["maximum_complete_gap_h"],60/3600)
    def test_overlapping_windows_merged(self):
        result=exact_gap_statistics([dict(entry_s=0,exit_s=30),dict(entry_s=20,exit_s=40)],50)
        self.assertIsNone(result["maximum_complete_gap_h"])
    def test_rolling_closed_endpoint_and_area_weights(self):
        result=rolling_fractions([np.array([86400.]),np.array([])],np.array([.25,.75]),86400,24)
        np.testing.assert_array_equal(result,[.25])
    def test_run_paths_reject_traversal(self):
        with self.assertRaises(ValueError): new_run_directory(ROOT,"../../frozen")
    def test_input_hash_changes(self):
        with tempfile.TemporaryDirectory(dir=ROOT/"tests") as folder:
            path=Path(folder)/"state"
            path.write_text("a")
            original=sha256(path)
            path.write_text("b")
            self.assertNotEqual(original,sha256(path))

if __name__=="__main__":
    unittest.main(verbosity=2)

