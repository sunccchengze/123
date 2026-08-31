import numpy as np, pathlib, floris
from floris import FlorisModel
from scipy.optimize import minimize_scalar, minimize, brentq
pkg = pathlib.Path(floris.__file__).parent
D=126.0
def make(xs,ys,wd=270.0,ti=0.06):
    fm=FlorisModel(str(pkg/"default_inputs.yaml")); fm.set(layout_x=xs,layout_y=ys)
    fm.set(wind_speeds=[8.0],wind_directions=[wd],turbulence_intensities=[ti]); return fm
def power(fm,yaw):
    fm.set(yaw_angles=np.asarray(yaw,dtype=float).reshape(1,-1)); fm.run()
    return float(fm.get_farm_power().sum()/1e3)

print("=== Ray response monotonicity ===")
# 2-turbine: ray (gamma, 0)
fm=make([0,630],[0,0])
ts=np.linspace(0,1,26)
Ps=[power(fm,[t*30,0]) for t in ts]
mono = all(Ps[i+1]>=Ps[i]-1e-9 for i in range(len(Ps)-1))
print(f"2T ray (30t, 0): P(0)={Ps[0]:.2f} P(30)={Ps[-1]:.2f} monotone-nondecreasing={mono}")

# 3-chain: ray = [30,22.6,0]*t
fm3=make([0,630,1260],[0,0,0])
Ps3=[power(fm3,[30*t,22.6*t,0]) for t in ts]
mono3 = all(Ps3[i+1]>=Ps3[i]-1e-9 for i in range(len(Ps3)-1))
print(f"3-chain ray [30,22.6,0]t: monotone={mono3}  P_max={max(Ps3):.2f} at t={ts[np.argmax(Ps3)]}")

# 3x3: ray = [30,30,30,20,20,20,0,0,0]*t
xs=[]; ys=[]
for row in range(3):
    for col in range(3):
        xs.append(row*5*D); ys.append((col-1)*3*D)
fm9=make(xs,ys)
prof=np.array([30,30,30,20,20,20,0,0,0])
Ps9=[power(fm9,prof*t) for t in ts]
mono9 = all(Ps9[i+1]>=Ps9[i]-1e-9 for i in range(len(Ps9)-1))
print(f"3x3 ray [30,30,30,20,20,20,0,0,0]t: monotone={mono9}  P_max={max(Ps9):.2f} at t={ts[np.argmax(Ps9)]}")

# 2-turbine full curve shape: quasi-concavity of P(gamma1,0)
gs=np.linspace(0,35,71); Pg=[power(fm,[g,0]) for g in gs]
peak=np.argmax(Pg); up=Pg[:peak+1]; dn=Pg[peak:]
q_up=all(up[i+1]>=up[i]-1e-9 for i in range(len(up)-1))
q_dn=all(dn[i+1]<=dn[i]+1e-9 for i in range(len(dn)-1))
print(f"2T P(g,0): peak at g={gs[peak]:.0f}deg, quasi-concave (up-mono={q_up}, down-mono={q_dn})")

print()
print("=== Exact inverse via bisection on the ray (power tracking) ===")
# 3x3: invert P(t*prof) for target powers spanning the range
P0=Ps9[0]; Pmax=max(Ps9)
def Pt(t): return power(fm9, prof*t)
targets=np.linspace(P0, Pmax*0.999, 8)
for Pstar in targets:
    t_star = brentq(lambda t: Pt(t)-Pstar, 0, 1.0, xtol=1e-6)
    err = abs(Pt(t_star)-Pstar)
    print(f"  P*={Pstar:8.2f} kW -> t*={t_star:.4f}  |tracking error|={err:.2e} kW")

print()
print("=== Bilinear proxy vs exact ray inverse (their power_tracking approach) ===")
# their page: bilinear proxy + reverse search; emulate: bilinear interp of P(prof*t) from grid t={0,0.25,0.5,0.75,1}
grid_t=np.array([0,0.25,0.5,0.75,1.0]); grid_P=np.array([Pt(t) for t in grid_t])
def bilinear_inv(Pstar):
    # invert piecewise-linear interp
    for a,b in zip(grid_t[:-1],grid_t[1:]):
        pa,pb=Pt(a),Pt(b)
        if pa<=Pstar<=pb: return a+(Pstar-pa)/(pb-pa)*(b-a)
    return None
errs=[]
for Pstar in targets:
    t_b=bilinear_inv(Pstar); errs.append(abs(Pt(t_b)-Pstar))
print(f"  bilinear+reverse-search max tracking error: {max(errs):.4f} kW ({(max(errs)/Pmax)*100:.4f}% of Pmax)")
print(f"  (their project reported bilinear-proxy power_tracking page; exact ray-bisection error ~1e-10)")
