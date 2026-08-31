import numpy as np, pathlib, floris, warnings
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
    return float(fm.get_farm_power().sum()/1e3)

def hessian(fm, base, hh=2.5):
    """central-difference Hessian of P (in deg coordinates)"""
    n = len(base); b = np.array(base, float); H = np.zeros((n,n))
    def P(y): return power(fm, y)
    # diagonal
    for i in range(n):
        d = np.zeros(n); d[i]=hh
        H[i,i] = (P(b+d)+P(b-d)-2*P(b))/hh**2
    for i in range(n):
        for j in range(i+1,n):
            di = np.zeros(n); di[i]=hh; dj = np.zeros(n); dj[j]=hh
            H[i,j] = H[j,i] = (P(b+di+dj)-P(b+di-dj)-P(b-di+dj)+P(b-di-dj))/(4*hh**2)
    return H

def od_ratio(H):
    d = np.diag(H).copy(); d[d==0]=1e-12
    off = H - np.diag(np.diag(H))
    return np.linalg.norm(off)/np.linalg.norm(np.diag(H))

D=126.0
# ---- Case set: (name, xs, ys, wd) ----
cases = []
xs3=[]; ys3=[]
for row in range(3):
    for col in range(3):
        xs3.append(row*5*D); ys3.append((col-1)*3*D)
cases.append(("3x3 aligned", xs3, ys3, 270.0))
cases.append(("3x3 wd300", xs3, ys3, 300.0))
cases.append(("3-chain 5D", [0,630,1260], [0,0,0], 270.0))
rng = np.random.default_rng(7)
cases.append(("random6 A", (rng.uniform(0,8,6)*D).tolist(), (rng.uniform(-3,3,6)*D).tolist(), 270.0))
cases.append(("random6 B", (rng.uniform(0,8,6)*D).tolist(), (rng.uniform(-3,3,6)*D).tolist(), 255.0))

print("=== Hessian at SLSQP optima: decoupling test ===")
for name, xs, ys, wd in cases:
    fm = make(xs, ys, wd=wd)
    n = len(xs)
    def f(yaw):
        fm.set(yaw_angles=np.asarray(yaw,dtype=float).reshape(1,-1)); fm.run()
        return -float(fm.get_farm_power().sum())
    best = None
    for x0 in [np.zeros(n), np.full(n,15.0), np.full(n,25.0), np.random.default_rng(1).uniform(0,30,n)]:
        res = minimize(f, x0, bounds=[(0,30)]*n, method="SLSQP", options={"maxiter":200,"ftol":1e-8})
        if best is None or res.fun < best.fun: best = res
    ystar = best.x
    H = hessian(fm, ystar, hh=2.5)
    ev = np.linalg.eigvalsh((H+H.T)/2)
    print(f"{name:15s} | y*={np.round(ystar,1)} | gain={(-best.fun/power(fm,np.zeros(n))-1)*100:+.2f}% | od/diag={od_ratio(H):.3f} | max|eig|={np.max(np.abs(ev)):.1f}")

print()
print("=== Greedy (upstream->downstream, 5deg grid) vs SLSQP on random layouts ===")
def greedy(fm, n, angles=np.arange(0,31,5)):
    order = np.argsort(fm.core.farm.layout_x)[::-1] if fm.core.farm.wind_directions[0]==270.0 else np.arange(n)
    # order by projection onto wind direction
    wd = np.deg2rad(fm.core.farm.wind_directions[0])
    u = np.array([np.cos(wd), np.sin(wd)])
    pos = np.stack([fm.core.farm.layout_x, fm.core.farm.layout_y],axis=1)
    proj = pos @ u
    order = np.argsort(proj)  # most upstream first
    yaw = np.zeros(n)
    def P(y): return power(fm, y)
    for i in order:
        best_a, best_p = 0, P(yaw)
        for a in angles:
            yaw[i]=float(a); p=P(yaw)
            if p>best_p: best_p, best_a = p, a
        yaw[i]=float(best_a)
    return yaw, best_p

rng = np.random.default_rng(42)
gaps=[]; inter=[]
for trial in range(8):
    n = 6
    xs = (rng.uniform(0,7,n)*D).tolist(); ys=(rng.uniform(-2.5,2.5,n)*D).tolist()
    wd = float(rng.uniform(240,300))
    fm = make(xs, ys, wd=wd)
    g_yaw, g_p = greedy(fm, n)
    def f(yaw):
        fm.set(yaw_angles=np.asarray(yaw,dtype=float).reshape(1,-1)); fm.run()
        return -float(fm.get_farm_power().sum())
    res = minimize(f, np.zeros(n), bounds=[(0,30)]*n, method="SLSQP", options={"maxiter":200})
    H = hessian(fm, g_yaw, hh=5.0)
    inter.append(np.linalg.norm(H-np.diag(np.diag(H))))
    gap = (-res.fun - g_p)/-res.fun*100
    gaps.append(gap)
    print(f"trial{trial}: wd={wd:.0f} greedy_gap={gap:+.2f}%  offdiag_norm={inter[-1]:.1f}")
print("correlation(gap, offdiag):", np.corrcoef(gaps, inter)[0,1])
