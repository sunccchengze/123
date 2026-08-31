import numpy as np, pathlib, floris
from floris import FlorisModel
from scipy.optimize import minimize
pkg = pathlib.Path(floris.__file__).parent

def make(layout_x, layout_y, wd=270.0, ti=0.06, ws=8.0):
    fm = FlorisModel(str(pkg/"default_inputs.yaml"))
    fm.set(layout_x=layout_x, layout_y=layout_y)
    fm.set(wind_speeds=[ws], wind_directions=[wd], turbulence_intensities=[ti])
    return fm
def power(fm, yaw):
    fm.set(yaw_angles=np.asarray(yaw, dtype=float).reshape(1,-1))
    fm.run()
    return float(fm.get_farm_power().sum())  # W

def hessian(fm, base, hh=2.5):
    n = len(base); b = np.array(base, float); H = np.zeros((n,n))
    def P(y): return power(fm, y)
    for i in range(n):
        d = np.zeros(n); d[i]=hh
        H[i,i] = (P(b+d)+P(b-d)-2*P(b))/hh**2
    for i in range(n):
        for j in range(i+1,n):
            di = np.zeros(n); di[i]=hh; dj = np.zeros(n); dj[j]=hh
            H[i,j] = H[j,i] = (P(b+di+dj)-P(b+di-dj)-P(b-di+dj)+P(b-di-dj))/(4*hh**2)
    return H
def od_ratio(H):
    off = H - np.diag(np.diag(H))
    return np.linalg.norm(off)/max(np.linalg.norm(np.diag(H)),1e-9)

D=126.0
xs3=[]; ys3=[]
for row in range(3):
    for col in range(3):
        xs3.append(row*5*D); ys3.append((col-1)*3*D)
cases = [("3x3 aligned", xs3, ys3, 270.0), ("3x3 wd300", xs3, ys3, 300.0),
         ("3-chain 5D", [0,630,1260], [0,0,0], 270.0)]
rng = np.random.default_rng(7)
cases.append(("random6 A", (rng.uniform(0,8,6)*D).tolist(), (rng.uniform(-3,3,6)*D).tolist(), 270.0))

print("=== od/diag at optima vs at non-optimal bases ===")
for name, xs, ys, wd in cases:
    fm = make(xs, ys, wd=wd); n=len(xs)
    def f(yaw):
        fm.set(yaw_angles=np.asarray(yaw,dtype=float).reshape(1,-1)); fm.run()
        return -float(fm.get_farm_power().sum())
    best=None
    for x0 in [np.zeros(n), np.full(n,15.0), np.full(n,25.0), np.random.default_rng(1).uniform(0,30,n)]:
        res = minimize(f, x0, bounds=[(0,30)]*n, method="SLSQP", options={"maxiter":300,"ftol":1e-9})
        if best is None or res.fun < best.fun: best=res
    ystar=best.x
    p0 = power(fm, np.zeros(n))
    r_opt = od_ratio(hessian(fm, ystar))
    r_zero = od_ratio(hessian(fm, np.zeros(n)))
    r_mid = od_ratio(hessian(fm, np.full(n,20.0)))
    print(f"{name:12s} y*={np.round(ystar,1)} gain={(power(fm,ystar)/p0-1)*100:+.2f}% | od/diag: opt={r_opt:.3f} zero={r_zero:.3f} mid20={r_mid:.3f}")

print()
print("=== 3-chain phase map (FLORIS): sign of M12 over (g2,g3), g1=20deg ===")
fm = make([0,630,1260],[0,0,0])
def M12(g1,g2,g3,hh=5.0):
    b=np.array([g1,g2,g3],float); d1=np.array([hh,0,0]); d2=np.array([0,hh,0])
    P=lambda y: power(fm,y)
    return (P(b+d1+d2)-P(b+d1-d2)-P(b-d1+d2)+P(b-d1-d2))/(4*hh**2)
for g3 in [0,10,20,30]:
    row=[]
    for g2 in [0,5,10,15,20,25,30]:
        m=M12(20,g2,g3); row.append("+" if m>0.05 else ("-" if m<-0.05 else "0"))
    print(f"  g3={g3:2d}: "+" ".join(row))

print()
print("=== comparative statics: 3-chain SLSQP optimum vs TI ===")
for ti in [0.04,0.06,0.08,0.10,0.12]:
    fm = make([0,630,1260],[0,0,0], ti=ti)
    def f(yaw):
        fm.set(yaw_angles=np.asarray(yaw,dtype=float).reshape(1,-1)); fm.run()
        return -float(fm.get_farm_power().sum())
    best=None
    for x0 in [np.zeros(3), np.array([25,15,0]), np.array([20,10,0])]:
        res = minimize(f, x0, bounds=[(0,30)]*3, method="SLSQP", options={"maxiter":300,"ftol":1e-9})
        if best is None or res.fun < best.fun: best=res
    p0=power(fm,np.zeros(3))
    print(f"  TI={ti}: y*={np.round(best.x,1)} gain={(power(fm,best.x)/p0-1)*100:+.2f}%")
