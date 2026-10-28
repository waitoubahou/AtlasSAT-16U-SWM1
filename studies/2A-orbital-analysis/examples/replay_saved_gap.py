"""Reaggregate six included saved point windows; not full-ROI reproduction."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"src"))
from atlas_analysis.metrics import exact_gap_statistics
def run():
 x=json.loads((ROOT/"data/examples/saved_daylight_intervals.json").read_text())
 windows=[dict(entry_s=float(w["entry_s"]),exit_s=float(w["exit_s"])) for w in x["intervals"]]
 result=exact_gap_statistics(windows,x["duration_s"])
 residual=abs(result["maximum_complete_gap_h"]-x["reported_maximum_complete_gap_h"])
 assert residual<1e-9 and result["observed_72h_failure"]
 return dict(scope="Single saved target; independently reaggregated intervals, not independently discovered events",window_count=len(windows),reported_maximum_complete_gap_h=x["reported_maximum_complete_gap_h"],gap_residual_h=residual,**result)
if __name__=="__main__":print(json.dumps(run(),indent=2,allow_nan=False))
