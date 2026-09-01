import numpy as np, pathlib
import floris
from floris import FlorisModel
pkg = pathlib.Path(floris.__file__).parent

fmodel = FlorisModel(str(pkg/"default_inputs.yaml"))
print("wake:", fmodel.core.farm.wake.model_strings, "| superpos:", fmodel.core.farm.wake.superposition_model, "| turbine:", fmodel.core.farm.turbine_type)

def mkfarm(xs, ys):
    fmodel.set(layout_x=xs, layout_y=ys)
    fmodel.set(wind_speeds=[8.0], wind_directions=[270.0], turbulence_intensities=[0.06])

def power(yaw):
    fmodel.set(yaw_angles=np.asarray(yaw, dtype=float).reshape(1,-1))
    fmodel.run()
    return float(fmodel.get_farm_power().sum()/1e3)

# 2-turbine serial 5D
mkfarm([0,630],[0,0])
p0 = power([0,0]); p25 = power([25,0])
print(f"2T serial 5D: gain@25deg = {(p25/p0-1)*100:+.2f}%  (target +8.13%)")

# 3x3 grid 5D
xs=[0,630,1260]*3; ys=[0,0,0,630,630,630,1260,1260,1260]
mkfarm(xs,ys)
p0 = power([0]*9)
for k,v in {"row1+30":[30,30,30,0,0,0,0,0,0],
            "rows12+30":[30,30,30,30,30,30,0,0,0],
            "greedy30/20/0":[30,30,30,20,20,20,0,0,0]}.items():
    P=power(v); print(f"3x3 {k}: gain {(P/p0-1)*100:+.2f}%  (targets +14.87/+22.73/+24.04)")
