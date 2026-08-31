import numpy as np, pathlib, floris, time, json
from floris import FlorisModel
from scipy.optimize import minimize
pkg = pathlib.Path(floris.__file__).parent
D = 126.0
OUT = pathlib.Path("expcache")
MODEL = dict(velocity_model="gauss", deflection_model="gauss",
             turbulence_model="crespo_hernandez", combination_model="sosfs")

def make(xs, ys, wd=270.0):
    fm = FlorisModel(str(pkg/"default_inputs.yaml"))
    fm.set_param(["wake","model_strings"], MODEL)
    fm.set(layout_x=xs, layout_y=ys)
    fm.set(wind_speeds=[8.0], wind_directions=[wd], turbulence_intensities=[0.06])
    return fm
def power(fm, yaw):
    fm.set(yaw_angles=np.asarray(yaw, dtype=float).reshape(1,-1)); fm.run()
    return float(fm.get_farm_power().sum()/1e3)
def djs(fm, y0, max_sweeps=6, trace=False):
    y = np.array(y0, float); n = len(y)
    best = power(fm, y); hist = [best]; ts = [0.0]; t0 = time.time()
    for s in range(max_sweeps):
        ynew = y.copy()
        for i in range(n):
            ba, bp = ynew[i], power(fm, ynew)
            for a in np.arange(0, 30.01, 1.0):
                ynew[i] = a; p = power(fm, ynew)
                if p > bp + 1e-12: bp, ba = p, a
            ynew[i] = ba
        y = ynew; pnew = power(fm, y)
        hist.append(pnew); ts.append(time.time()-t0)
        if abs(pnew - best) < 1e-4: best = pnew; break
        best = pnew
    return y, best, hist, ts
def slsqp_ref(fm, n, starts=4, maxiter=300):
    def f(yaw):
        fm.set(yaw_angles=np.asarray(yaw, dtype=float).reshape(1,-1)); fm.run()
        return -float(fm.get_farm_power().sum()/1e3)
    best = None
    for x0 in [np.zeros(n), np.full(n,15.0), np.full(n,25.0), np.random.default_rng(1).uniform(0,30,n)]:
        res = minimize(f, x0, bounds=[(0,30)]*n, method="SLSQP", options={"maxiter":maxiter})
        if best is None or res.fun < best.fun: best = res
    return best.x, -best.fun

cases = {
 "chain3": ([0,630,1260],[0,0,0]),
 "grid3x3": ([r*5*D for r in range(3) for c in range(3)], [(c-1)*3*D for r in range(3) for c in range(3)]),
 "grid4x4": ([r*5*D for r in range(4) for c in range(4)], [(c-1.5)*3*D for r in range(4) for c in range(4)]),
 "rand16": (np.random.default_rng(123).uniform(0,14,16)*D, np.random.default_rng(456).uniform(-3,3,16)*D),
}
traces = {}
for cname,(xs,ys) in cases.items():
    fm = make(xs, ys); n = len(xs)
    t0 = time.time(); yopt, pstar = slsqp_ref(fm, n); t_slsqp = time.time()-t0
    t0 = time.time(); yd, pd, hist, ts = djs(fm, np.zeros(n), trace=True); t_djs = time.time()-t0
    pbase = power(fm, np.zeros(n))
    gap = (pstar-pd)/pstar*100
    traces[cname] = dict(n=n, pbase=pbase, pstar=pstar, pdjs=pd, gap=gap,
                         hist=hist, ts=ts, t_slsqp=t_slsqp, t_djs=t_djs,
                         gain_slsqp=(pstar/pbase-1)*100, gain_djs=(pd/pbase-1)*100)
    print(f"{cname}: n={n} gap={gap:.4f}% t_djs={t_djs:.1f}s t_slsqp={t_slsqp:.1f}s sweeps={len(hist)-1}")

# merge into exp_p1.json if present, else standalone
p1f = OUT/"exp_p1.json"
data = {}
if p1f.exists():
    data = json.loads(p1f.read_text())
data["traces"] = traces
json.dump(data, open(p1f,"w"))
print("traces merged ->", p1f)
