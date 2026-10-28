"""Public scope tests; no private datasets, kernels, mission execution or network."""
from pathlib import Path
import ast,hashlib,json,math,sys,unittest
import numpy as np
from unittest import mock
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/"src"),str(ROOT/"examples")]
from atlas_analysis.geometry import geodetic,normal_at
from atlas_analysis.metrics import exact_gap_statistics
from atlas_analysis.provenance import code_fingerprint
from atlas_analytical import formulae as f
import controlled_geometry,analytical_checks,replay_saved_gap
from ast_identity import stable_ast_sha256
class PublicExamples(unittest.TestCase):
 def test_controlled_geometry_and_synthetic_day_night(self):
  result=controlled_geometry.run()
  self.assertEqual(result["parser_rows"],2)
  self.assertEqual(len(result["windows"]["synthetic_day"]),3)
  self.assertEqual(len(result["windows"]["synthetic_night"]),3)
 def test_controlled_circular_solution(self):
  self.assertLess(analytical_checks.run()["max_position_residual_km"],1e-8)
 def test_saved_single_target_gap(self):
  result=replay_saved_gap.run()
  self.assertEqual(result["window_count"],6)
  self.assertAlmostEqual(result["maximum_complete_gap_h"],312.21995813943926,places=8)
  self.assertTrue(result["observed_72h_failure"])
 def test_saved_example_is_ordered_and_bounded(self):
  x=json.loads((ROOT/"data/examples/saved_daylight_intervals.json").read_text())
  windows=x["intervals"]
  self.assertTrue(all(0<=float(w["entry_s"])<float(w["exit_s"])<=x["duration_s"] for w in windows))
  self.assertEqual(windows,sorted(windows,key=lambda w:float(w["entry_s"])))
 def test_23_extracted_function_bodies_are_unchanged(self):
  audit=json.loads((ROOT/"qa/function_extraction_audit.json").read_text())
  source=(ROOT/"src/atlas_analytical/formulae.py").read_text()
  nodes={n.name:n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef)}
  self.assertEqual(len(audit["functions"]),23)
  for record in audit["functions"]:
   node=nodes[record["function"]]
   self.assertEqual(hashlib.sha256(ast.get_source_segment(source,node).encode()).hexdigest(),record["original_function_sha256"])
   self.assertEqual(stable_ast_sha256(node),record["portable_ast_sha256"])
 def test_ast_identity_is_independent_of_interpreter_dump_format(self):
  audit=json.loads((ROOT/"qa/function_extraction_audit.json").read_text())
  nodes={n.name:n for n in ast.parse((ROOT/"src/atlas_analytical/formulae.py").read_text()).body if isinstance(n,ast.FunctionDef)}
  with mock.patch.object(ast,"dump",side_effect=AssertionError("Version-specific dump must not be used")):
   for row in audit["functions"]:
    self.assertEqual(stable_ast_sha256(nodes[row["function"]]),row["portable_ast_sha256"])
 def test_independent_wgs84_formula_agrees(self):
  for lat,lon in ((0,0),(30.1,-9.5),(-55,120)):
   q,n=f.surface_point(lat,lon)
   np.testing.assert_allclose(q,geodetic(lat,lon),atol=1e-11)
   np.testing.assert_allclose(n,normal_at(lat,lon),atol=1e-14)
 def test_keplerian_transform_preserves_norm(self):
  o=dict(a=7000.,e=.01,i=.5,node=.4,peri=.2,true=.3,mu=398600.4415)
  r,v=f.initial_cartesian(o)
  self.assertAlmostEqual(np.linalg.norm(r),o["a"]*(1-o["e"]**2)/(1+o["e"]*math.cos(o["true"])),places=9)
 def test_precession_is_rotation(self):
  matrix,_=f.precession_j2000_to_mod(f.EPOCH)
  np.testing.assert_allclose(matrix@matrix.T,np.eye(3),atol=1e-14)
 def test_spherical_nadir_has_zero_reach(self):
  self.assertEqual(f.spherical_reach(0)["ground_arc_km"],0)
 def test_ellipsoid_intersection(self):
  q=f.ellipsoid_ray(np.array([f.WGS_A+550,0,0]),np.array([-1.,0,0]))
  np.testing.assert_allclose(q,[f.WGS_A,0,0],atol=1e-9)
 def test_censored_empty_case_is_not_complete_gap(self):
  result=exact_gap_statistics([],720*3600)
  self.assertIsNone(result["maximum_complete_gap_h"])
  self.assertEqual(result["no_access_span_h"],720)
 def test_threshold_boundary(self):
  self.assertFalse(exact_gap_statistics([],72*3600)["observed_72h_failure"])
  self.assertTrue(exact_gap_statistics([],72*3600+1)["observed_72h_failure"])
 def test_source_fingerprint_is_not_empty_directory_hash(self):
  self.assertNotEqual(code_fingerprint(ROOT),hashlib.sha256(b"").hexdigest())
 def test_public_metrics_keep_the_negative_verdict(self):
  data=json.loads((ROOT/"data/published_results.json").read_text())
  self.assertEqual(data["verdict"],"NOT MET")
  self.assertEqual(data["criterion_h"],72)
  self.assertGreater(data["maximum_complete_daylight_gap_h"],data["criterion_h"])
  daylight=[r for r in data["modes"] if r["mode"]=="daylight"]
  self.assertEqual(len(daylight),3)
  self.assertTrue(all(r["rolling_hourly_coverage"]["72"]["min"]==0 for r in daylight))
if __name__=="__main__":unittest.main(verbosity=2)
