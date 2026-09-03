"""ARCHIVED P1 local-diagnostic table generator.

A sampled off-diagonal/diagonal ratio is not a decoupling law or a certificate.
Retained for provenance; see ARCHIVE_NOTICE.md and THEORY.md.
"""

import numpy as np, pathlib, floris, json, warnings
warnings.filterwarnings("ignore")
from floris import FlorisModel
from scipy.optimize import minimize
pkg = pathlib.Path(floris.__file__).parent
D = 126.0

def make(xs, ys, wd=270.0, ti=0.06, ws=8.0):
    fm = FlorisModel(str(pkg/"default_inputs.yaml"))
    fm.set(layout_x=xs, layout_y=ys)
    fm.set(wind_speeds=[ws], wind_directions=[wd], turbulence_intensities=[ti])
    return fm

def power(fm, yaw):
    fm.set(yaw_angles=np.asarray(yaw, dtype=float).reshape(1,-1)); fm.run()
    return float(fm.get_farm_power().sum()/1e3)

def hessian(fm, base, hh=5.0):
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
    return float(np.linalg.norm(off)/max(np.linalg.norm(np.diag(H)), 1e-9))

def slsqp_opt(fm, x0s=None):
    n = len(fm.layout_x)
    if x0s is None:
        x0s = [np.zeros(n), np.full(n,15.0), np.full(n,25.0), np.random.default_rng(1).uniform(0,30,n)]
    def f(yaw):
        fm.set(yaw_angles=np.asarray(yaw, dtype=float).reshape(1,-1)); fm.run()
        return -float(fm.get_farm_power().sum())
    best = None
    for x0 in x0s:
        res = minimize(f, x0, bounds=[(0,30)]*n, method="SLSQP", options={"maxiter":300,"ftol":1e-9})
        if best is None or res.fun < best.fun: best = res
    return best.x, -best.fun/1e3

x9=[]; y9=[]
for row in range(3):
    for col in range(3):
        x9.append(row*5*D); y9.append((col-1)*3*D)
x16=[]; y16=[]
for row in range(4):
    for col in range(4):
        x16.append(row*5*D); y16.append((col-1.5)*3*D)

out = {}

def row(name, xs, ys, wd):
    fm = make(xs, ys, wd=wd); n = len(xs)
    ystar, p_opt = slsqp_opt(fm)
    p0 = power(fm, np.zeros(n))
    r_opt = od_ratio(hessian(fm, ystar))
    r_zero = od_ratio(hessian(fm, np.zeros(n)))
    r_mid = od_ratio(hessian(fm, np.full(n, 20.0))) if n <= 9 else None
    rec = dict(opt=round(r_opt,3), zero=round(r_zero,3), mid20=(round(r_mid,3) if r_mid is not None else None),
               ystar=[round(v,1) for v in ystar], gain=round((p_opt/p0-1)*100, 2))
    out[name] = rec
    print(f"{name:18s} y*={rec['ystar']} gain={rec['gain']:+.2f}% | od: opt={rec['opt']} zero={rec['zero']} mid20={rec['mid20']}", flush=True)

row("3x3 wd270", x9, y9, 270.0)
row("3x3 wd300", x9, y9, 300.0)
row("3-chain 5D", [0,630,1260], [0,0,0], 270.0)
row("4x4 wd270", x16, y16, 270.0)
rng = np.random.default_rng(7)
row("random6 A", (rng.uniform(0,8,6)*D).tolist(), (rng.uniform(-3,3,6)*D).tolist(), 270.0)

# AEP over 12 directions: mixture Hessian at per-direction optima and at origin
dirs = np.arange(0, 360, 30)
weights = np.array([0.04,0.05,0.06,0.08,0.10,0.12,0.12,0.10,0.09,0.08,0.08,0.08]); weights/=weights.sum()
H0_mix = np.zeros((9,9)); Hst_mix = np.zeros((9,9)); aep_gain = 0.0; aep0 = 0.0; aep1 = 0.0
for k, wd in enumerate(dirs):
    fm = make(x9, y9, wd=float(wd))
    p0 = power(fm, np.zeros(9))
    ystar, p_opt = slsqp_opt(fm)
    H0_mix += weights[k]*hessian(fm, np.zeros(9))
    Hst_mix += weights[k]*hessian(fm, ystar)
    aep0 += weights[k]*p0; aep1 += weights[k]*p_opt
    print(f"  AEP dir {wd:3.0f}: +{(p_opt/p0-1)*100:+.2f}%", flush=True)
out["3x3 AEP"] = dict(opt=round(od_ratio(Hst_mix),3), zero=round(od_ratio(H0_mix),3), mid20=None,
                      ystar=None, gain=round((aep1/aep0-1)*100,2))
print(f"AEP row: od opt={out['3x3 AEP']['opt']} zero={out['3x3 AEP']['zero']} gain={out['3x3 AEP']['gain']:+.2f}%", flush=True)

json.dump(out, open("expcache/decoupling_table.json","w"), indent=1)
print("saved expcache/decoupling_table.json", flush=True)
