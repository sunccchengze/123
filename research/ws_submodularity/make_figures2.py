"""Regenerate archived P1/P2/P3 figure artifacts.

P1/P2 figures contain withdrawn phase, decoupling, certificate, DJS, and timing
interpretations; they are preserved as historical outputs, not research results.
P3 figures have a separate finite-grid/static-benchmark limitation. Read
ARCHIVE_NOTICE.md, THEORY.md, and the top-level forensic status before use.
"""

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

# WES requires raster figure files at 300 dpi.  ``savefig.dpi`` is explicit so
# every output, including figures that do not pass a dpi argument, carries that
# resolution in both pixels and PNG metadata.
plt.rcParams.update({"font.size": 9, "axes.titlesize": 10, "figure.dpi": 300, "savefig.dpi": 300})
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
import json as _json, pathlib as _pl
_qf = _pl.Path("expcache/qc_fine.json")
qc = _json.load(open(_qf)) if _qf.exists() else p1["qc"]  # 0.5deg fine grid if available
fig, ax = plt.subplots(figsize=(4.8, 3.4))
for s in ["4", "5", "6", "7"]:
    d = qc[s]
    g, P = np.asarray(d["g"]), np.asarray(d["P"])
    ax.plot(g, (P/P[0]-1)*100, "o-", ms=3.5, lw=1.3, label=f"{s}D (peak {d['peak']:.1f}°)")
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

# ---------------- Paper 3: cache-backed figures ----------------
# The operational 41-point rays, exact inversions, and proxy comparison are
# read from experiment caches. This prevents Table 2 and Figs. C1/C3/C4 from
# silently drifting to separately recomputed target grids or traces.
tracking_path = CACHE / "table2_tracking.json"
proxy_path = CACHE / "proxy_tracking_benchmark.json"
ray_path = CACHE / "ray_monotonicity.json"
if not tracking_path.exists() or not proxy_path.exists() or not ray_path.exists():
    raise RuntimeError(
        "Run exp_inverse.py to regenerate the ray-screen and matched-target tracking caches."
    )
tracking_records = json.loads(tracking_path.read_text())
proxy_benchmark = json.loads(proxy_path.read_text())
ray_benchmark = json.loads(ray_path.read_text())
exact_targets = np.asarray([float(record["target"]) for record in tracking_records])
proxy_targets = np.asarray(proxy_benchmark["targets_kW"], dtype=float)
if exact_targets.shape != proxy_targets.shape or not np.allclose(
    exact_targets, proxy_targets, rtol=0.0, atol=1e-8
):
    raise RuntimeError("Proxy and exact benchmark target grids differ; refusing to draw an unfair comparison.")

# ---------------- Paper 3: figC1 rays ----------------
traces = ray_benchmark["operational_41_point_screen"]["traces"]
trace_specs = [
    ("two_turbine_30_0", "2T ray [30,0]·t"),
    ("three_turbine_30_22p6_0", "3-chain ray [30,22.6,0]·t"),
    ("three_by_three_30_30_30_20_20_20_0_0_0", "3×3 ray [30,30,30,20,20,20,0,0,0]·t"),
]
ts = np.asarray(traces[trace_specs[0][0]]["sample_t"], dtype=float)
rays = {}
for key, label in trace_specs:
    trace = traces[key]
    trace_t = np.asarray(trace["sample_t"], dtype=float)
    if trace_t.shape != ts.shape or not np.allclose(trace_t, ts, rtol=0.0, atol=1e-12):
        raise RuntimeError("Ray traces do not share the declared 41-point grid.")
    rays[label] = np.asarray(trace["power_kW"], dtype=float)
fig, ax = plt.subplots(figsize=(5.2, 3.6))
for name, powers in rays.items():
    ax.plot(ts, (powers - powers[0]) / (powers.max() - powers[0]) * 100, "o-", ms=3, lw=1.3, label=name)
ax.set_xlabel("ray parameter t"); ax.set_ylabel("share of available gain [%]")
ax.set_title("Power response along profile rays")
ax.legend(fontsize=7)
fig.tight_layout(); fig.savefig(D/"figC1_rays.png"); plt.close(fig)

# ---------------- Paper 3: figC2 quasi-concavity (reuse qc) ----------------
fig, ax = plt.subplots(figsize=(4.8, 3.4))
for s in ["4", "5", "6", "7"]:
    d = qc[s]
    g, P = np.asarray(d["g"]), np.asarray(d["P"])
    ax.plot(g, (P/P[0]-1)*100, "o-", ms=3.5, lw=1.3, label=f"{s}D (peak {d['peak']:.1f}°)")
ax.set_xlabel("γ₁ [deg]"); ax.set_ylabel("ΔP/P₀ [%]")
ax.set_title("Quasi-concave single-peak response (two turbines)")
ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(D/"figC2_quasiconcavity.png"); plt.close(fig)

# ---------------- Paper 3: figC3 bisection iteration study ----------------
fig, ax = plt.subplots(figsize=(4.8, 3.2))
ax.semilogy(
    [int(record["calls"]) for record in tracking_records],
    [float(record["err"]) for record in tracking_records],
    "o-",
    lw=1.3,
)
ax.set_xlabel("model evaluations"); ax.set_ylabel("|tracking error| [kW]")
ax.set_title("Bracketed ray inversion: error vs evaluation budget")
fig.tight_layout(); fig.savefig(D/"figC3_bisection.png"); plt.close(fig)
print(
    "ray-inversion study:",
    [
        (f"{float(record['target']):.0f}", int(record["calls"]), f"{float(record['err']):.2e}")
        for record in tracking_records
    ],
)

# ---------------- Appendix C Fig. C4: proxy versus exact inverse ----------------
# Both bars use the cache-backed nine-target benchmark already validated above.
exact_max_error = max(float(record["err"]) for record in tracking_records)
proxy_max_error = float(proxy_benchmark["max_error_kW"])
fig, ax = plt.subplots(figsize=(4.8, 3.4))
bars = ax.bar(
    [0, 1],
    [proxy_max_error, exact_max_error],
    color=["#D55E00", "#0072B2"],
    width=0.62,
)
ax.set_yscale("log")
ax.set_ylim(1e-5, 1e3)
ax.set_xticks([0, 1])
ax.set_xticklabels(["five-node proxy slice\n(reverse search)", "ray bisection\n(same 9 targets)"])
ax.set_ylabel("maximum tracking error [kW] (log scale)")
ax.set_title("Matched-target tracking accuracy on the 3$\\times$3 farm")
for bar, value, text in zip(bars, [proxy_max_error, exact_max_error], [f"{proxy_max_error:.2f} kW", f"{exact_max_error:.3g} kW"]):
    ax.text(bar.get_x() + bar.get_width() / 2, value * 1.8, text, ha="center", va="bottom", fontsize=8)
fig.tight_layout(); fig.savefig(D/"figC4_proxy_vs_exact.png"); plt.close(fig)
print(f"matched-target proxy-versus-exact maximum errors: {proxy_max_error:.2f} kW vs {exact_max_error:.3g} kW")

print("ALL FIGURES DONE")
