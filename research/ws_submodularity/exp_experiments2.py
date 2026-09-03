"""ARCHIVED P1/P2 exploratory analysis, not a benchmark or certificate.

The historic sampled-interaction and runtime outputs cannot establish global
bounds, parallel execution, or a journal-ready algorithm claim. Retained only
for provenance; see ARCHIVE_NOTICE.md and p1_p2_forensic_audit.py.
"""

import numpy as np, pathlib, floris, time, json
from floris import FlorisModel
from scipy.optimize import minimize
pkg = pathlib.Path(floris.__file__).parent
D = 126.0
OUT = pathlib.Path("expcache"); OUT.mkdir(exist_ok=True)
MODEL = dict(velocity_model="gauss", deflection_model="gauss",
             turbulence_model="crespo_hernandez", combination_model="sosfs")

def make(xs, ys, wd=270.0, ti=0.06):
    fm = FlorisModel(str(pkg/"default_inputs.yaml"))
    fm.set_param(["wake","model_strings"], MODEL)
    fm.set(layout_x=xs, layout_y=ys)
    fm.set(wind_speeds=[8.0], wind_directions=[wd], turbulence_intensities=[ti])
    return fm

def power(fm, yaw):
    fm.set(yaw_angles=np.asarray(yaw, dtype=float).reshape(1,-1)); fm.run()
    return float(fm.get_farm_power().sum()/1e3)

def Mij(fm, base, i, j, hh=5.0):
    b = np.array(base, float)
    def P(y): return power(fm, y)
    def d(k):
        v = np.zeros_like(b); v[k] = hh; return v
    if i == j:
        return (P(b+d(i)) + P(b-d(i)) - 2*P(b))/hh**2
    return (P(b+d(i)+d(j)) - P(b+d(i)-d(j)) - P(b-d(i)+d(j)) + P(b-d(i)-d(j)))/(4*hh**2)

def greedy(fm, n, angles=np.arange(0,31,5)):
    # wind_directions is meteorological (FROM, clockwise from north);
    # flow vector in FLORIS coords (x=east, y=north): v = [-sin(wd), -cos(wd)]
    wd = np.deg2rad(float(fm.core.flow_field.wind_directions[0]))
    u = np.array([-np.sin(wd), -np.cos(wd)])
    pos = np.stack([fm.core.farm.layout_x, fm.core.farm.layout_y], axis=1)
    order = np.argsort(pos @ u)   # ascending projection = most upstream first
    yaw = np.zeros(n)
    def P(y): return power(fm, y)
    for i in order:
        ba, bp = 0, P(yaw)
        for a in angles:
            yaw[i] = float(a); p = P(yaw)
            if p > bp: bp, ba = p, a
        yaw[i] = float(ba)
    return yaw, power(fm, yaw)

def slsqp_ref(fm, n, starts=4, maxiter=300):
    def f(yaw):
        fm.set(yaw_angles=np.asarray(yaw, dtype=float).reshape(1,-1)); fm.run()
        return -float(fm.get_farm_power().sum()/1e3)
    best = None
    for x0 in [np.zeros(n), np.full(n,15.0), np.full(n,25.0), np.random.default_rng(1).uniform(0,30,n)]:
        res = minimize(f, x0, bounds=[(0,30)]*n, method="SLSQP", options={"maxiter":maxiter})
        if best is None or res.fun < best.fun: best = res
    return best.x, -best.fun

results = {}

# ---------- 1. certificate benchmark: 12 random layouts ----------
rng = np.random.default_rng(42)
certs = []
for trial in range(12):
    n = int(rng.integers(6, 10))
    xs = (rng.uniform(0, 7, n)*D).tolist(); ys = (rng.uniform(-2.5, 2.5, n)*D).tolist()
    wd = float(rng.uniform(240, 300))
    fm = make(xs, ys, wd=wd)
    pbase = power(fm, np.zeros(n))
    g_yaw, g_p = greedy(fm, n)
    y_s, p_s = slsqp_ref(fm, n)
    gap = (p_s - g_p)/p_s*100
    # sampled mean off-diagonal interactions (valid region: yaw <= 20 everywhere)
    r2 = np.random.default_rng(7)
    Msum = np.zeros((n,n)); cnt = 0
    sample_pts = [np.zeros(n)] + [r2.uniform(0, 20, n) for _ in range(4)]
    for pt in sample_pts:
        H = np.zeros((n,n))
        for i in range(n):
            for j in range(i+1, n):
                m = Mij(fm, pt, i, j)
                H[i,j] = H[j,i] = m
        Msum += np.triu(H,1); cnt += 1
    Mbar = Msum/cnt
    bound = 0.5*np.sum(np.maximum(0, Mbar))*30**2
    pstar = p_s; pbase_pct = (pstar/pbase-1)*100
    certs.append(dict(n=n, xs=xs, ys=ys, wd=wd, gap=gap, bound=bound, pbase=pbase,
                      gain_slsqp=pbase_pct, gain_greedy=(g_p/pbase-1)*100))
    print(f"trial{trial:02d}: n={n} wd={wd:.0f} gap={gap:+.4f}% bound={bound:.2f} kW bound/pbase={bound/pbase*100:.2f}%")
gaps = np.array([c["gap"] for c in certs])
print(f"CERT: mean gap={gaps.mean():.4f}% max={gaps.max():.4f}%")
results["certs"] = certs

# ---------- 2. 5x5 sign-matrix heatmap at origin ----------
xs5 = [r*5*D for r in range(5) for c in range(5)]
ys5 = [(c-2)*3*D for r in range(5) for c in range(5)]
fm = make(xs5, ys5, wd=270.0)
H5 = np.zeros((25,25))
for i in range(25):
    for j in range(i+1, 25):
        H5[i,j] = H5[j,i] = Mij(fm, np.zeros(25), i, j)
results["h5x5"] = H5.tolist()
print("5x5 matrix done; max|M|=", np.abs(H5).max())
# clustering at tau=0.05 (on |M|)
import itertools
adj = np.abs(H5) > 0.05
seen = set(); clusters = []
for i in range(25):
    if i in seen: continue
    comp = set([i]); frontier = [i]
    while frontier:
        k = frontier.pop()
        for j in range(25):
            if adj[k,j] and j not in comp:
                comp.add(j); frontier.append(j)
    seen |= comp; clusters.append(sorted(comp))
results["clusters_tau005"] = clusters
print("clusters:", clusters)

# ---------- 3. wall-time scaling ----------
wt = {}
cases = {
 "chain3": ([0,630,1260],[0,0,0]),
 "grid3x3": ([r*5*D for r in range(3) for c in range(3)], [(c-1)*3*D for r in range(3) for c in range(3)]),
 "grid4x4": ([r*5*D for r in range(4) for c in range(4)], [(c-1.5)*3*D for r in range(4) for c in range(4)]),
 "grid5x5": (xs5, ys5),
 "rand16": (np.random.default_rng(123).uniform(0,14,16)*D, np.random.default_rng(456).uniform(-3,3,16)*D),
}
for cname,(xs,ys) in cases.items():
    fm = make(xs, ys); n = len(xs)
    t0 = time.time(); yopt, pstar = slsqp_ref(fm, n); t_s = time.time()-t0
    t0 = time.time(); g_yaw, g_p = greedy(fm, n); t_g = time.time()-t0
    t0 = time.time()
    y = np.zeros(n)
    for s in range(3):
        ynew = y.copy()
        for i in range(n):
            ba, bp = ynew[i], power(fm, ynew)
            for a in np.arange(0, 30.01, 1.0):
                ynew[i] = a; p = power(fm, ynew)
                if p > bp + 1e-12: bp, ba = p, a
            ynew[i] = ba
        y = ynew
    t_d = time.time()-t0
    wt[cname] = dict(n=n, t_slsqp=t_s, t_greedy=t_g, t_djs=t_d)
    print(f"WT {cname}: n={n} slsqp={t_s:.1f}s greedy={t_g:.2f}s djs={t_d:.1f}s")
results["walltime"] = wt

with open(OUT/"exp_p2.json","w") as f:
    json.dump(results, f)
print("PART2 SAVED ->", OUT/"exp_p2.json")
