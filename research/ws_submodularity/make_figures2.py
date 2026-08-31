import json, pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = pathlib.Path(__file__).parent
CACHE = D/"expcache"
p1 = json.loads((CACHE/"exp_p1.json").read_text())
p2 = json.loads((CACHE/"exp_p2.json").read_text())
# merge empgauss supplement
supf = CACHE/"exp_empgauss_supp.json"
if supf.exists():
    sup = json.loads(supf.read_text())
    c = sup["curve"]
    p1.setdefault("power_curves", {})["empgauss"] = (c["gs"], c["P"], c["pfit"], c["r2"])
    p1.setdefault("phase_flip", {})["empgauss"] = {pt: v for pt, v in sup["flip"].items()}
    g = sup["grid3x3"]
    p1.setdefault("sign_mats", {})["empgauss"] = dict(H0=g["H0"], Hstar=g["Hstar"], yopt=g["yopt"],
        gain=g["gain"], od0=g["od0"], odst=g["odst"])

plt.rcParams.update({"font.size": 9, "axes.titlesize": 10, "figure.dpi": 150})
colors = {"gauss": "#1f77b4", "cc": "#d62728", "empgauss": "#2ca02c", "jensen": "#9467bd"}

# ---------------- Paper 1: fig7 model power curves + cos^p fits ----------------
curves = p1["power_curves"]
fig, ax = plt.subplots(figsize=(4.6, 3.4))
for name in ["gauss", "cc", "empgauss", "jensen"]:
    if name not in curves: continue
    g, P, p_fit, r2 = curves[name]
    g, P = np.asarray(g), np.asarray(P)
    if p_fit is not None:
        ax.plot(g, (P/P[0]-1)*100, "o-", ms=4, lw=1.4, color=colors[name], label=f"{name} (cos^p, p={p_fit:.2f}, R²={r2:.3f})")
        gm = g[g > 0]
        ax.plot(gm, ((np.cos(np.deg2rad(gm))**p_fit)-1)*100, "--", lw=1.0, color=colors[name], alpha=0.7)
    else:
        ax.plot(g, (P/P[0]-1)*100, "o-", ms=4, lw=1.4, color=colors[name], label=f"{name} (flat response)")
ax.axhline(0, color="gray", lw=0.7)
ax.set_xlabel("yaw misalignment γ₁ [deg]"); ax.set_ylabel("ΔP/P₀ [%] (two turbines, 5D)")
ax.set_title("Power–yaw response across wake models (FLORIS 4.6)")
ax.legend(fontsize=7)
fig.tight_layout(); fig.savefig(D/"fig7_model_curves.png"); plt.close(fig)

# ---------------- Paper 1: fig8 phase flip across models ----------------
flips = p1["phase_flip"]
pts = ["origin", "mid", "near_opt"]
fig, ax = plt.subplots(figsize=(4.8, 3.4))
xpos = np.arange(len(pts)); w = 0.2
for k, name in enumerate(["gauss", "cc", "empgauss", "jensen"]):
    if name not in flips: continue
    m12 = [flips[name][pt][0] for pt in pts]
    ax.bar(xpos + (k-1.5)*w, m12, w, label=name, color=colors[name])
ax.axhline(0, color="k", lw=0.8)
ax.set_xticks(xpos); ax.set_xticklabels(["(0,0,0)", "(20,20,20)", "(30,20,0)"])
ax.set_xlabel("operating point (γ₁,γ₂,γ₃) [deg]"); ax.set_ylabel("M₁₂ [kW/deg²]")
ax.set_title("Complement→substitute sign flip of the chain pair (3 turbines)")
ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(D/"fig8_flip_models.png"); plt.close(fig)

# ---------------- Paper 1: fig9 wind-speed sweep ----------------
ws = p1["ws_sweep"]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 3.2))
for name in ["gauss", "cc"]:
    if name not in ws: continue
    d = ws[name]
    ax1.plot(d["speeds"], d["od0"], "o-", color=colors[name], lw=1.3, label=f"{name} (generic pts)")
    ax1.plot(d["speeds"], d["odst"], "s--", color=colors[name], lw=1.3, label=f"{name} (optimum)")
    ax2.plot(d["speeds"], d["gains"], "o-", color=colors[name], lw=1.3, label=name)
ax1.set_xlabel("wind speed [m/s]"); ax1.set_ylabel("‖M_off‖/‖diag M‖")
ax1.set_title("Decoupling ratio vs wind speed (3×3)")
ax1.legend(fontsize=7)
ax2.set_xlabel("wind speed [m/s]"); ax2.set_ylabel("optimal gain [%]")
ax2.set_title("Steering gain vs wind speed")
ax2.legend(fontsize=7)
fig.tight_layout(); fig.savefig(D/"fig9_ws_decoupling.png"); plt.close(fig)

# ---------------- Paper 1: fig10 wind rose ----------------
rose = p1["rose"]
dirs = np.asarray(rose["dirs"]); gains = np.asarray(rose["gains"])
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 3.3), subplot_kw=dict(projection="polar"))
theta = np.deg2rad((270 - dirs) % 360)
ax1.bar(theta, gains, width=np.deg2rad(25), color="#1f77b4", alpha=0.85)
ax1.set_title(f"AEP gain per direction: {rose['aep_gain']:+.2f} %", pad=16)
ax1.set_theta_zero_location("N"); ax1.set_theta_direction(-1)
ax2.bar(theta, rose["weights"], width=np.deg2rad(25), color="gray", alpha=0.7)
ax2.set_title("Assumed direction weights", pad=16)
ax2.set_theta_zero_location("N"); ax2.set_theta_direction(-1)
fig.tight_layout(); fig.savefig(D/"fig10_windrose.png"); plt.close(fig)

# ---------------- Paper 1: fig11 DJS traces + walltime ----------------
tr = p1["traces"]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 3.3))
for name in ["chain3", "grid3x3", "grid4x4", "rand16"]:
    d = tr[name]
    pn = (np.asarray(d["hist"]) - d["pbase"])/(d["pstar"] - d["pbase"])
    ax1.plot(range(len(pn)), pn*100, "o-", lw=1.3, ms=3.5, label=f"{name} (n={d['n']})")
ax1.axhline(100, color="gray", lw=0.7, ls=":")
ax1.set_xlabel("sweep"); ax1.set_ylabel("share of SLSQP gain reached [%]")
ax1.set_title("DJS convergence (2–3 sweeps)")
ax1.legend(fontsize=7)
names = ["chain3", "grid3x3", "grid4x4", "rand16"]
x = np.arange(len(names)); w = 0.38
ax2.bar(x-w/2, [tr[n]["t_djs"] for n in names], w, label="DJS (3 sweeps)", color="#1f77b4")
ax2.bar(x+w/2, [tr[n]["t_slsqp"] for n in names], w, label="SLSQP (4 starts)", color="#ff7f0e")
ax2.set_yscale("log"); ax2.set_xticks(x); ax2.set_xticklabels(names, fontsize=8)
ax2.set_ylabel("wall time [s]"); ax2.set_title("Wall time (log scale)")
ax2.legend(fontsize=7)
fig.tight_layout(); fig.savefig(D/"fig11_djs_traces.png"); plt.close(fig)

# ---------------- Paper 1: fig12 quasi-concavity vs spacing ----------------
qc = p1["qc"]
fig, ax = plt.subplots(figsize=(4.8, 3.4))
for s in ["4", "5", "6", "7"]:
    d = qc[s]
    g, P = np.asarray(d["g"]), np.asarray(d["P"])
    ax.plot(g, (P/P[0]-1)*100, "o-", ms=3.5, lw=1.3, label=f"{s}D (peak {d['peak']:.0f}°)")
ax.set_xlabel("γ₁ [deg]"); ax.set_ylabel("ΔP/P₀ [%] (two turbines)")
ax.set_title("Quasi-concavity of P(γ₁, 0) across spacings")
ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(D/"fig12_quasiconcavity.png"); plt.close(fig)

# ---------------- Paper 2: figB3 5x5 heatmap + clusters ----------------
H5 = np.asarray(p2["h5x5"])
fig, ax = plt.subplots(figsize=(4.6, 4.0))
vmax = np.abs(H5).max()
im = ax.imshow(H5, cmap="RdBu_r", vmin=-vmax, vmax=vmax)
ax.set_title("Sign matrix M(0) of the 5×5 farm")
ax.set_xlabel("turbine j"); ax.set_ylabel("turbine i")
# cluster overlay: first 20 (rows 0-3) one cluster, last 5 isolated
for i in range(20):
    ax.add_patch(plt.Rectangle((-0.5, -0.5), 20, 20, fill=False, edgecolor="k", lw=1.2))
    break
fig.colorbar(im, ax=ax, label="M_ij [kW/deg²]")
fig.tight_layout(); fig.savefig(D/"figB3_heatmap5x5.png"); plt.close(fig)

# ---------------- Paper 2: figB4 walltime scaling ----------------
wt = p2["walltime"]
names = ["chain3", "grid3x3", "grid4x4", "grid5x5", "rand16"]
ns = [wt[n]["n"] for n in names]
fig, ax = plt.subplots(figsize=(4.8, 3.4))
ax.plot(ns, [wt[n]["t_slsqp"] for n in names], "o-", lw=1.4, label="SLSQP (4 starts)")
ax.plot(ns, [wt[n]["t_djs"] for n in names], "s-", lw=1.4, label="DJS (3 sweeps, 1° grid)")
ax.plot(ns, [wt[n]["t_greedy"] for n in names], "^-", lw=1.4, label="Boolean greedy (5° grid)")
ax.set_yscale("log"); ax.set_xlabel("number of turbines N"); ax.set_ylabel("wall time [s]")
ax.set_title("Wall-time scaling with farm size")
ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(D/"figB4_walltime.png"); plt.close(fig)

# ---------------- Paper 2: figB5 certificate scatter ----------------
certs = p2["certs"]
gaps = [c["gap"] for c in certs]; bounds = [c["bound"]/c["pbase"]*100 for c in certs]
fig, ax = plt.subplots(figsize=(4.6, 3.4))
ax.scatter(bounds, gaps, s=28, color="#1f77b4", zorder=3)
xs = np.linspace(0, max(bounds)*1.1, 100)
ax.plot(xs, xs, "k--", lw=1, label="bound = gap")
ax.fill_between(xs, 0, xs, alpha=0.12, color="green", label="certified region")
ax.set_xlabel("interaction-energy bound [% of P]"); ax.set_ylabel("measured greedy gap [% of P]")
ax.set_title("Bounded-interaction certificate, 12 random layouts")
ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(D/"figB5_certificate.png"); plt.close(fig)

# ---------------- Paper 3: figC1 rays ----------------
# 2T ray [30,0] (non-monotone past peak), 3-chain ray, 3x3 ray — recompute cheaply
import floris
from floris import FlorisModel
pkg = pathlib.Path(floris.__file__).parent
Dm = 126.0
def make(xs, ys, wd=270.0):
    fm = FlorisModel(str(pkg/"default_inputs.yaml")); fm.set(layout_x=xs, layout_y=ys)
    fm.set(wind_speeds=[8.0], wind_directions=[wd], turbulence_intensities=[0.06]); return fm
def power(fm, yaw):
    fm.set(yaw_angles=np.asarray(yaw, dtype=float).reshape(1,-1)); fm.run()
    return float(fm.get_farm_power().sum()/1e3)
x9 = [r*5*Dm for r in range(3) for c in range(3)]
y9 = [(c-1)*3*Dm for r in range(3) for c in range(3)]
rays = {}
fm2 = make([0, 630], [0, 0])
ts = np.linspace(0, 1, 41)
rays["2T ray [30,0]·t"] = np.array([power(fm2, [30*t, 0]) for t in ts])
fm3 = make([0, 630, 1260], [0, 0, 0])
rays["3-chain ray [30,22.6,0]·t"] = np.array([power(fm3, [30*t, 22.6*t, 0]) for t in ts])
fm9 = make(x9, y9)
prof = np.array([30,30,30,20,20,20,0,0,0])
rays["3×3 ray [30,30,30,20,20,20,0,0,0]·t"] = np.array([power(fm9, prof*t) for t in ts])
fig, ax = plt.subplots(figsize=(5.2, 3.6))
for k, (name, P) in enumerate(rays.items()):
    ax.plot(ts, (P-P[0])/(P.max()-P[0])*100, "o-", ms=3, lw=1.3, label=name)
ax.set_xlabel("ray parameter t"); ax.set_ylabel("share of available gain [%]")
ax.set_title("Power response along profile rays")
ax.legend(fontsize=7)
fig.tight_layout(); fig.savefig(D/"figC1_rays.png"); plt.close(fig)
np.save(D/"expcache/rays.npy", {k: v for k, v in rays.items()}, allow_pickle=True)

# ---------------- Paper 3: figC2 quasi-concavity (reuse qc) ----------------
fig, ax = plt.subplots(figsize=(4.8, 3.4))
for s in ["4", "5", "6", "7"]:
    d = qc[s]
    g, P = np.asarray(d["g"]), np.asarray(d["P"])
    ax.plot(g, (P/P[0]-1)*100, "o-", ms=3.5, lw=1.3, label=f"{s}D (peak {d['peak']:.0f}°)")
ax.set_xlabel("γ₁ [deg]"); ax.set_ylabel("ΔP/P₀ [%]")
ax.set_title("Quasi-concave single-peak response (two turbines)")
ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(D/"figC2_quasiconcavity.png"); plt.close(fig)

# ---------------- Paper 3: figC3 bisection iteration study ----------------
from scipy.optimize import brentq
P0 = rays["3×3 ray [30,30,30,20,20,20,0,0,0]·t"][0]
Pmax = rays["3×3 ray [30,30,30,20,20,20,0,0,0]·t"].max()
def Pt(t): return power(fm9, prof*t)
class Tracker:
    def __init__(self, target):
        self.target = target; self.calls = 0
    def f(self, t):
        self.calls += 1
        return Pt(t) - self.target
targets = np.linspace(P0 + 0.05*(Pmax-P0), Pmax - 0.01*(Pmax-P0), 9)
recs = []
for Pstar in targets:
    trk = Tracker(Pstar)
    tstar = brentq(trk.f, 0.0, 1.0, xtol=1e-6, rtol=1e-6)
    err = abs(Pt(tstar) - Pstar)
    recs.append((Pstar, tstar, err, trk.calls))
fig, ax = plt.subplots(figsize=(4.8, 3.2))
ax.semilogy([r[3] for r in recs], [r[2] for r in recs], "o-", lw=1.3)
ax.set_xlabel("model evaluations"); ax.set_ylabel("|tracking error| [kW]")
ax.set_title("Bisection on the ray: error vs evaluation budget")
fig.tight_layout(); fig.savefig(D/"figC3_bisection.png"); plt.close(fig)
print("bisection study:", [(f"{r[0]:.0f}", r[3], f"{r[2]:.2e}") for r in recs])

print("ALL FIGURES DONE")
