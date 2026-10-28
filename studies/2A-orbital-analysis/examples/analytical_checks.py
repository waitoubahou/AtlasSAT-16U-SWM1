"""Independent formula checks on a controlled circle, not the AtlasSAT mission."""
from pathlib import Path
import sys,json,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"src"))
from atlas_analytical.formulae import universal_two_body
def run():
 x=json.loads((ROOT/"data/examples/controlled_inputs.json").read_text());a=x["toy_circular_radius_km"];mu=x["toy_mu_km3_s2"]
 n=math.sqrt(mu/a**3);t=np.array([0.,100.,1000.,2*math.pi/n])
 r0=np.array([a,0.,0.]);v0=np.array([0.,math.sqrt(mu/a),0.])
 r,v,_=universal_two_body(r0,v0,t,mu)
 expected=np.c_[a*np.cos(n*t),a*np.sin(n*t),np.zeros(len(t))]
 velocity=np.c_[-a*n*np.sin(n*t),a*n*np.cos(n*t),np.zeros(len(t))]
 dr=float(np.linalg.norm(r-expected,axis=1).max());dv=float(np.linalg.norm(v-velocity,axis=1).max())
 assert dr<1e-8 and dv<1e-10
 return dict(scope="Controlled circular-solution check; no propagation, mission-design or saved-GMAT comparison",max_position_residual_km=dr,max_velocity_residual_km_s=dv)
if __name__=="__main__":print(json.dumps(run(),indent=2,allow_nan=False))
