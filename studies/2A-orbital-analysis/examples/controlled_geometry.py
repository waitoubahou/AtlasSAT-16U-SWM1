"""Public controlled demonstration. No GMAT execution, real ephemeris or GIS inputs."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from atlas_analysis.oem import read_oem
from atlas_analysis.geometry import Orbit,geodetic,normal_at
from atlas_analysis.optical_access import compute
def run():
 x=json.loads((ROOT/"data/examples/controlled_inputs.json").read_text())
 optical=json.loads((ROOT/"config/optical_geometry.json").read_text())["optical"]
 q=geodetic(x["latitude_deg"],x["longitude_deg"]);normal=normal_at(x["latitude_deg"],x["longitude_deg"])
 lon=np.radians(x["longitude_deg"]);east=np.array([-np.sin(lon),np.cos(lon),0])
 t=np.array(x["times_s"],float);r=np.array([q+x["height_km"]*normal+(s-x["crossing_s"])*x["speed_km_s"]*east for s in t])
 state=np.c_[r,np.tile(x["speed_km_s"]*east,(len(t),1))]
 orbit=Orbit(t,state,optical);targets=[dict(id="CONTROLLED_POINT",q=q,normal=normal)]
 epoch=datetime(2026,10,20,12,tzinfo=timezone.utc);results={}
 for name,sign in (("synthetic_day",1),("synthetic_night",-1)):
  sun=np.tile(q+sign*x["synthetic_sun_distance_km"]*normal,(len(t),1))
  windows=compute(orbit,sun,targets,[30],[0,10,20],epoch,progress=False)
  assert len(windows)==3
  assert all(0<w["exit_s"]-w["entry_s"]<.002 for w in windows)
  assert all(w["daylight"]==(sign==1) for w in windows)
  results[name]=windows
 oem=read_oem(ROOT/"data/examples/CONTROLLED_NOT_GMAT.oem")
 return dict(scope="Controlled unit demonstration only; synthetic linear path and synthetic Sun vectors",parser_rows=len(oem.times),parser_duration_s=float(oem.times[-1]),windows=results)
if __name__=="__main__":print(json.dumps(run(),indent=2,allow_nan=False))
