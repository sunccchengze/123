import numpy as np, pathlib, floris, time, json
from floris import FlorisModel
from scipy.optimize import minimize
pkg = pathlib.Path(floris.__file__).parent
D = 126.0
OUT = pathlib.Path("expcache"); OUT.mkdir(exist_ok=True)

def make(xs, ys, wd=270.0, ti=0.06, model=None, ws=8.0):
    fm = FlorisModel(str(pkg/"default_inputs.yaml"))
    if model is not None:
        fm.set_param(["wake","model_strings"], model)
        if model.get("velocity_model") == "empirical_gauss":
            fm.set_param(["wake","enable_secondary_steering"], False)
            fm.set_param(["wake","enable_transverse_velocities"], False)
            for key, val in EMPGAUSS_PARAMS.items():
                fm.set_param(["wake", key], val)
    fm.set(layout_x=xs, layout_y=ys)
    fm.set(wind_speeds=[ws], wind_directions=[wd], turbulence_intensities=[ti])
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

def hessian(fm, base, hh=5.0):
    n = len(base)
    H = np.zeros((n,n))
    for i in range(n):
        H[i,i] = Mij(fm, base, i, i, hh)
        for j in range(i+1, n):
            H[i,j] = H[j,i] = Mij(fm, base, i, j, hh)
    return H

def od_ratio(H):
    off = H - np.diag(np.diag(H))
    return float(np.linalg.norm(off)/np.linalg.norm(np.diag(H)))

def djs(fm, y0, max_sweeps=6, grid_step=1.0, trace=False):
    y = np.array(y0, float); n = len(y)
    best = power(fm, y); hist = [best]; ts = [0.0]; t0 = time.time()
    for s in range(max_sweeps):
        ynew = y.copy()
        for i in range(n):
            ba, bp = ynew[i], power(fm, ynew)
            for a in np.arange(0, 30.01, grid_step):
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

MODELS = {
 "gauss": dict(velocity_model="gauss", deflection_model="gauss", turbulence_model="crespo_hernandez", combination_model="sosfs"),
 "cc": dict(velocity_model="cc", deflection_model="gauss", turbulence_model="crespo_hernandez", combination_model="sosfs"),
 "empgauss": dict(velocity_model="empirical_gauss", deflection_model="empirical_gauss", turbulence_model="wake_induced_mixing", combination_model="sosfs"),
 "jensen": dict(velocity_model="jensen", deflection_model="jimenez", turbulence_model="crespo_hernandez", combination_model="sosfs"),
}
EMPGAUSS_PARAMS = dict(
 wake_velocity_parameters=dict(empirical_gauss=dict(wake_expansion_rates=[0.023, 0.008], breakpoints_D=[10], sigma_0_D=0.28, smoothing_length_D=2.0, mixing_gain_velocity=2.0)),
 wake_deflection_parameters=dict(empirical_gauss=dict(horizontal_deflection_gain_D=2.0, vertical_deflection_gain_D=-1.0, mixing_gain_deflection=0.0, yaw_added_mixing_gain=0.0)),
 wake_turbulence_parameters=dict(wake_induced_mixing=dict(atmospheric_ti_gain=0.0)),
)

results = {}

# ---------- 0. reproducibility anchor (gauss 2T 5D) ----------
fm = make([0,630],[0,0], model=MODELS["gauss"])
p0 = power(fm,[0,0]); p25 = power(fm,[25,0])
print(f"ANCHOR gauss 2T: P(0)={p0:.2f} P(25)={p25:.2f} (+{(p25/p0-1)*100:.2f}%)  [expect 2190.39 / 2368.40 / +8.13]")

# ---------- 1. two-turbine power-yaw curves + cos^p fits, all models ----------
gs = np.arange(0, 31, 1.0)
curves = {}
for name, mdl in MODELS.items():
    try:
        fm = make([0,630],[0,0], model=mdl)
        P = np.array([power(fm,[g,0]) for g in gs])
        mask = (gs>0) & (P>0)
        c = np.cos(np.deg2rad(gs[mask])); lr = np.log(P[mask]/P[0])
        p_fit = float(np.sum(np.log(c)*lr)/np.sum(np.log(c)**2))
        res = lr - p_fit*np.log(c)
        r2 = float(1 - np.sum(res**2)/np.sum((lr-lr.mean())**2))
        curves[name] = (gs, P, p_fit, r2)
        print(f"cos^p fit {name}: p={p_fit:.3f} R2={r2:.5f}")
    except Exception as e:
        print(f"model {name} FAILED: {type(e).__name__} {e}")
results["power_curves"] = {k: (v[0].tolist(), v[1].tolist(), v[2], v[3]) for k,v in curves.items()}
results["power_curves"]["jensen"] = (gs.tolist(), curves["jensen"][1].tolist(), None, None)

# ---------- 2. 3-chain phase flip across models ----------
pts = {"origin":[0,0,0], "mid":[20,20,20], "near_opt":[30,20,0]}
flips = {}
for name, mdl in MODELS.items():
    try:
        fm = make([0,630,1260],[0,0,0], model=mdl)
        flips[name] = {pname: [Mij(fm, pt, 0, 1), Mij(fm, pt, 0, 2), Mij(fm, pt, 1, 2)]
                       for pname, pt in pts.items()}
        print(f"flip {name}: origin M12={flips[name]['origin'][0]:+.3f} mid M12={flips[name]['mid'][0]:+.3f}")
    except Exception as e:
        print(f"flip {name} FAILED: {e}")
results["phase_flip"] = flips

# ---------- 3. 3x3 sign matrices (origin + own optimum) ----------
x9=[]; y9=[]
for row in range(3):
    for col in range(3):
        x9.append(row*5*D); y9.append((col-1)*3*D)
sign_mats = {}
for name in ["gauss","cc","empgauss"]:
    try:
        fm = make(x9, y9, model=MODELS[name])
        H0 = hessian(fm, np.zeros(9), hh=5.0)
        yopt, popt, _, _ = djs(fm, np.zeros(9))
        Hstar = hessian(fm, yopt, hh=5.0)
        pbase = power(fm, np.zeros(9))
        sign_mats[name] = dict(H0=H0.tolist(), Hstar=Hstar.tolist(), yopt=yopt.tolist(),
                               gain=(popt/pbase-1)*100, od0=od_ratio(H0), odst=od_ratio(Hstar))
        print(f"3x3 {name}: gain={sign_mats[name]['gain']:+.2f}% od/diag {sign_mats[name]['od0']:.3f}->{sign_mats[name]['odst']:.3f} y*={np.round(yopt,1)}")
    except Exception as e:
        print(f"3x3 {name} FAILED: {e}")
results["sign_mats"] = sign_mats

# ---------- 4. wind-speed sweep: decoupling ratio vs speed (gauss, cc) ----------
ws_sweep = {}
for name in ["gauss","cc"]:
    ws_sweep[name] = dict(speeds=[], od0=[], odst=[], gains=[], ystar=[])
    for ws in [6,7,8,9,10]:
        try:
            fm = make(x9, y9, model=MODELS[name], ws=ws)
            H0 = hessian(fm, np.zeros(9), hh=5.0)
            yopt, popt, _, _ = djs(fm, np.zeros(9))
            Hstar = hessian(fm, yopt, hh=5.0)
            pbase = power(fm, np.zeros(9))
            ws_sweep[name]["speeds"].append(ws); ws_sweep[name]["od0"].append(od_ratio(H0))
            ws_sweep[name]["odst"].append(od_ratio(Hstar)); ws_sweep[name]["gains"].append((popt/pbase-1)*100)
            ws_sweep[name]["ystar"].append(np.round(yopt,1).tolist())
            print(f"ws={ws} {name}: gain={ws_sweep[name]['gains'][-1]:+.2f}% od {ws_sweep[name]['od0'][-1]:.3f}->{ws_sweep[name]['odst'][-1]:.3f}")
        except Exception as e:
            print(f"ws={ws} {name} FAILED: {e}")
results["ws_sweep"] = ws_sweep

# ---------- 5. wind-rose AEP (gauss 3x3, 12 directions) ----------
dirs = np.arange(0, 360, 30)
weights = np.array([0.04,0.05,0.06,0.08,0.10,0.12,0.12,0.10,0.09,0.08,0.08,0.08]); weights/=weights.sum()
rose = dict(dirs=[], weights=weights.tolist(), base=[], djs_p=[], gains=[])
for wd in dirs:
    fm = make(x9, y9, wd=float(wd), model=MODELS["gauss"])
    pbase = power(fm, np.zeros(9))
    yopt, popt, _, _ = djs(fm, np.zeros(9))
    rose["dirs"].append(float(wd)); rose["base"].append(pbase); rose["djs_p"].append(popt)
    rose["gains"].append((popt/pbase-1)*100)
    print(f"rose wd={wd}: +{rose['gains'][-1]:+.2f}%")
aep0 = float(np.sum(weights*np.array(rose["base"]))*8760)
aep1 = float(np.sum(weights*np.array(rose["djs_p"]))*8760)
rose["aep0"], rose["aep1"], rose["aep_gain"] = aep0, aep1, (aep1/aep0-1)*100
print(f"AEP: {aep0:.3e} -> {aep1:.3e} kWh  (+{rose['aep_gain']:.2f}%)")
results["rose"] = rose

# ---------- 6. DJS convergence traces + walltimes vs SLSQP ----------
traces = {}
cases = {
 "chain3": ([0,630,1260],[0,0,0]),
 "grid3x3": (x9, y9),
 "grid4x4": ([r*5*D for r in range(4) for c in range(4)], [(c-1.5)*3*D for r in range(4) for c in range(4)]),
 "rand16": (np.random.default_rng(123).uniform(0,14,16)*D, np.random.default_rng(456).uniform(-3,3,16)*D),
}
for cname,(xs,ys) in cases.items():
    fm = make(xs, ys, model=MODELS["gauss"])
    n = len(xs)
    t0 = time.time(); yopt, pstar = slsqp_ref(fm, n); t_slsqp = time.time()-t0
    t0 = time.time(); yd, pd, hist, ts = djs(fm, np.zeros(n), trace=True); t_djs = time.time()-t0
    pbase = power(fm, np.zeros(n))
    gap = (pstar-pd)/pstar*100
    traces[cname] = dict(n=n, pbase=pbase, pstar=pstar, pdjs=pd, gap=gap,
                         hist=hist, ts=ts, t_slsqp=t_slsqp, t_djs=t_djs,
                         gain_slsqp=(pstar/pbase-1)*100, gain_djs=(pd/pbase-1)*100)
    print(f"trace {cname}: n={n} gap={gap:.4f}% t_djs={t_djs:.1f}s t_slsqp={t_slsqp:.1f}s sweeps={len(hist)-1}")
results["traces"] = traces

# ---------- 7. two-turbine quasi-concavity across spacings ----------
qc = {}
for s in [4,5,6,7]:
    fm = make([0,s*D],[0,0], model=MODELS["gauss"])
    g = np.arange(0, 36, 1.0)
    P = np.array([power(fm,[gg,0]) for gg in g])
    peak = int(np.argmax(P))
    up = P[:peak+1]; dn = P[peak:]
    qc[s] = dict(g=g.tolist(), P=P.tolist(), peak=float(g[peak]),
                 up_mono=bool(all(np.diff(up)>=-1e-9)), dn_mono=bool(all(np.diff(dn)<=1e-9)))
    print(f"QC spacing {s}D: peak={g[peak]:.0f} up={qc[s]['up_mono']} dn={qc[s]['dn_mono']}")
results["qc"] = qc

# ---------- 8. wind-direction robustness of greedy gain (3x3) ----------
wd_rob = dict(wd=[], gains=[], yopt=[])
for wd in np.arange(240, 301, 5):
    fm = make(x9, y9, wd=float(wd), model=MODELS["gauss"])
    pbase = power(fm, np.zeros(9))
    yopt, popt, _, _ = djs(fm, np.zeros(9))
    wd_rob["wd"].append(float(wd)); wd_rob["gains"].append((popt/pbase-1)*100)
    wd_rob["yopt"].append(np.round(yopt,1).tolist())
results["wd_rob"] = wd_rob

with open(OUT/"exp_p1.json","w") as f:
    json.dump(results, f)
print("PART1 SAVED ->", OUT/"exp_p1.json")
