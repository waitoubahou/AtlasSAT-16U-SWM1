"""Explicit OEM postprocessing only. No GMAT subprocess, mission writer or cache."""
import argparse
import csv
import json
import time
from pathlib import Path
import numpy as np
from .oem import read_oem
from .frames import transform_ephemeris
from .geometry import Orbit, read_targets, A, B
from .optical_access import compute, scenario, utc
from .metrics import summarize
from .provenance import fingerprint, new_run_directory, write_json

def write_csv(path, rows):
    if not rows:
        Path(path).write_text("", encoding="utf-8")
        return
    with Path(path).open("w", newline="",encoding="utf-8") as stream:
        writer = csv.DictWriter(stream,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

def run(oem, targets_path, config_path, tag):
    root = Path(__file__).resolve().parents[2]
    config = json.loads(Path(config_path).read_text(encoding="utf-8-sig"))
    before = fingerprint(root,oem,config_path,targets_path,config)
    ephemeris = read_oem(oem, config["oem"])
    targets = read_targets(targets_path,config["optical"])
    optical = config["optical"]
    if config["earth"] != {"equatorial_radius_km": A, "flattening": 1/298.257223563}:
        raise ValueError("Only the pinned WGS84 target ellipsoid is supported")
    if (not optical["swaths_km"] or not optical["roll_limits_deg"] or
        any(s not in (20,30,40) for s in optical["swaths_km"]) or
        any(r not in (0,10,20) for r in optical["roll_limits_deg"]) or
        optical["along_track_sample_m"] != 10 or
        optical["regional_prefilter_km"] != 2000 or
        optical["candidate_slant_filter_km"] != 1600 or
        optical["supported_target_radius_km"] > 150):
        raise ValueError("Optical settings outside validated regional search domain; review before extending")
    radius = np.linalg.norm(ephemeris.states[:,:3],axis=1)
    if radius.min() < A+200 or radius.max() > A+1000:
        raise ValueError("OEM outside 200–1000 km radial-altitude search domain; revalidate range filters")
    directory = new_run_directory(root,tag)
    write_json(directory/"RUNNING.json",dict(status="started",**before))
    started = time.perf_counter()
    print(f"Explicit OEM: {Path(oem).resolve()}\nTargets: {len(targets)}\nOutput: {directory}",flush=True)
    state,sun = transform_ephemeris(ephemeris,config,root)
    orbit = Orbit(ephemeris.times,state,config["optical"])
    print("Frame/time conversion complete; detecting continuous access boundaries",flush=True)
    optical = config["optical"]
    windows = compute(orbit,sun,targets,optical["swaths_km"],optical["roll_limits_deg"],ephemeris.epoch)
    scenarios = [scenario(sw,r) for sw in optical["swaths_km"] for r in optical["roll_limits_deg"]]
    rows,summaries,subregions = summarize(windows,targets,float(ephemeris.times[-1]),scenarios)
    write_csv(directory/"access.csv",windows)
    write_csv(directory/"per_target.csv",rows)
    write_csv(directory/"subregions.csv",subregions)
    write_json(directory/"summary.json",summaries)
    # Radial-nadir intersection with WGS84, distinct from the geodetic subpoint.
    xyz = state[:,:3]
    surface = xyz/np.sqrt((xyz[:,:2]**2).sum(axis=1)/A**2+xyz[:,2]**2/B**2)[:,None]
    lat = np.degrees(np.arctan2(surface[:,2]/B**2,np.linalg.norm(surface[:,:2],axis=1)/A**2))
    lon = np.degrees(np.arctan2(surface[:,1],surface[:,0]))
    write_csv(directory/"radial_nadir_groundtrack.csv",[
        dict(utc=utc(ephemeris.epoch,t),elapsed_s=float(t),latitude_deg=float(la),longitude_deg=float(lo))
        for t,la,lo in zip(ephemeris.times,lat,lon)])
    after = fingerprint(root,oem,config_path,targets_path,config)
    if after != before:
        raise RuntimeError("Inputs or code changed during execution; discard this incomplete run")
    import scipy, spiceypy, erfa
    write_json(directory/"run_manifest.json",dict(status="complete",**before,
        oem=str(Path(oem).resolve()),targets=str(Path(targets_path).resolve()),
        config=str(Path(config_path).resolve()),epoch=ephemeris.epoch.isoformat(),
        duration_s=float(ephemeris.times[-1]),oem_rows=len(ephemeris.times),targets_count=len(targets),
        access_count=len(windows),elapsed_wall_s=time.perf_counter()-started,
        dependencies=dict(numpy=np.__version__,scipy=scipy.__version__,spiceypy=spiceypy.__version__,erfa=erfa.__version__),
        cache_policy="Always recompute; no disk result cache",
        scientific_status="Experimental numerical transfer only; no operational validation"))
    print(f"Completed: {directory}",flush=True)
    return directory

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--oem",required=True,type=Path)
    parser.add_argument("--targets",required=True,type=Path)
    parser.add_argument("--config",required=True,type=Path)
    parser.add_argument("--tag",default="analysis")
    args = parser.parse_args()
    run(args.oem,args.targets,args.config,args.tag)

if __name__ == "__main__":
    main()

