"""Regenerate archived P1 exploratory figures; do not use them as results.

The phase, decoupling, and sampled-bound interpretations formerly associated
with these images were withdrawn by the 2026-08-31 forensic audit. The raster
files remain unchanged as historical evidence. New generation is therefore for
provenance only, not validation. Read ARCHIVE_NOTICE.md before use.

Environment for the historic calculation: Python 3.11, FLORIS 4.6.6, NumPy,
and Matplotlib.
"""
from __future__ import annotations

import json
from pathlib import Path

import floris
import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from floris import FlorisModel

ROOT = Path(__file__).parent
CACHE = ROOT / "expcache"
D_ROTOR = 126.0  # m, NREL 5 MW rotor diameter in default_inputs.yaml
DPI = 300

plt.rcParams.update(
    {
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "figure.dpi": DPI,
        "savefig.dpi": DPI,
    }
)


def load_json(name: str):
    return json.loads((CACHE / name).read_text())


def save_json(name: str, value: dict) -> None:
    (CACHE / name).write_text(json.dumps(value, indent=2))


def make(layout_x, layout_y, wd: float = 270.0, ti: float = 0.06) -> FlorisModel:
    pkg = Path(floris.__file__).parent
    fm = FlorisModel(str(pkg / "default_inputs.yaml"))
    fm.set(layout_x=layout_x, layout_y=layout_y)
    fm.set(wind_speeds=[8.0], wind_directions=[wd], turbulence_intensities=[ti])
    return fm


def power(fm: FlorisModel, yaw) -> float:
    """Farm power in kW."""
    fm.set(yaw_angles=np.asarray(yaw, dtype=float).reshape(1, -1))
    fm.run()
    return float(fm.get_farm_power().sum() / 1e3)


def mixed_partial(fm: FlorisModel, base, i: int, j: int, h: float = 5.0) -> float:
    """Central finite-difference d2P/(dgamma_i dgamma_j), kW deg^-2."""
    b = np.asarray(base, dtype=float)
    ei = np.zeros_like(b)
    ej = np.zeros_like(b)
    ei[i] = h
    ej[j] = h
    return (power(fm, b + ei + ej) - power(fm, b + ei - ej)
            - power(fm, b - ei + ej) + power(fm, b - ei - ej)) / (4.0 * h**2)


def hessian(fm: FlorisModel, base, h: float = 5.0) -> np.ndarray:
    """Symmetric central-difference Hessian, evaluated efficiently once per pair."""
    b = np.asarray(base, dtype=float)
    n = len(b)
    out = np.zeros((n, n))
    p0 = power(fm, b)
    for i in range(n):
        ei = np.zeros(n)
        ei[i] = h
        out[i, i] = (power(fm, b + ei) + power(fm, b - ei) - 2.0 * p0) / h**2
        for j in range(i + 1, n):
            out[i, j] = out[j, i] = mixed_partial(fm, b, i, j, h)
    return out


p1 = load_json("exp_p1.json")
p2 = load_json("exp_p2.json")
decoupling = load_json("decoupling_table.json")
ti_sweep = load_json("ti_sweep.json")

# ---------------------------------------------------------------------------
# Fig. 1: 3-turbine phase map.  Cells at 25 degrees and beyond are omitted
# because the manuscript declares that the high-yaw corner warning zone is
# outside the reported-validity domain.
# ---------------------------------------------------------------------------
phase_cache = CACHE / "fig1_phasemap.json"
if phase_cache.exists():
    phase = json.loads(phase_cache.read_text())
    gamma_grid = np.asarray(phase["gamma_grid"], dtype=float)
    phase_values = np.asarray(phase["M12_kW_per_deg2"], dtype=float)
else:
    gamma_grid = np.arange(0.0, 21.0, 5.0)
    fm3 = make([0.0, 5.0 * D_ROTOR, 10.0 * D_ROTOR], [0.0, 0.0, 0.0])
    phase_values = np.empty((len(gamma_grid), len(gamma_grid)))
    for row, gamma3 in enumerate(gamma_grid):
        for col, gamma2 in enumerate(gamma_grid):
            phase_values[row, col] = mixed_partial(fm3, [20.0, gamma2, gamma3], 0, 1)
    phase = {
        "floris_version": floris.__version__,
        "wind_speed_m_per_s": 8.0,
        "wind_direction_deg": 270.0,
        "turbulence_intensity": 0.06,
        "gamma1_deg": 20.0,
        "h_deg": 5.0,
        "gamma_grid": gamma_grid.tolist(),
        "M12_kW_per_deg2": phase_values.tolist(),
    }
    save_json("fig1_phasemap.json", phase)

fig, ax = plt.subplots(figsize=(5.6, 4.6))
vmax = max(0.7, float(np.max(np.abs(phase_values))))
im = ax.imshow(
    phase_values,
    cmap="RdBu_r",
    vmin=-vmax,
    vmax=vmax,
    origin="lower",
    extent=[-2.5, 22.5, -2.5, 22.5],
)
ax.set_xlabel(r"$\gamma_2$ [deg]")
ax.set_ylabel(r"$\gamma_3$ [deg]")
ax.set_title(r"$M_{12}$ phase map at $\gamma_1=20^\circ$ (three-turbine chain)")
for col, gamma2 in enumerate(gamma_grid):
    for row, gamma3 in enumerate(gamma_grid):
        ax.text(gamma2, gamma3, f"{phase_values[row, col]:+.2f}", ha="center", va="center", fontsize=7)
ax.set_xticks(gamma_grid)
ax.set_yticks(gamma_grid)
fig.colorbar(im, ax=ax, fraction=0.046, label=r"$M_{12}$ [kW deg$^{-2}$]")
fig.tight_layout()
fig.savefig(ROOT / "fig1_phasemap.png", dpi=DPI)
plt.close(fig)
print("fig1 done")

# ---------------------------------------------------------------------------
# Fig. 2: sign matrices.  The two 270-degree matrices come from the audited
# experiment cache.  The rotated 300-degree matrix is cached after first use.
# The diagonal is intentionally blanked: this plot is about pairwise mixed
# partials, while Fig. 3 reports their normalization by diagonal curvature.
# ---------------------------------------------------------------------------
H0 = np.asarray(p1["sign_mats"]["gauss"]["H0"], dtype=float)
Hopt = np.asarray(p1["sign_mats"]["gauss"]["Hstar"], dtype=float)
wd300_cache = CACHE / "fig2_hessian_wd300.json"
if wd300_cache.exists():
    H300 = np.asarray(json.loads(wd300_cache.read_text())["H_kW_per_deg2"], dtype=float)
else:
    x9 = [row * 5.0 * D_ROTOR for row in range(3) for _ in range(3)]
    y9 = [(col - 1) * 3.0 * D_ROTOR for _ in range(3) for col in range(3)]
    H300 = hessian(make(x9, y9, wd=300.0), np.zeros(9), h=5.0)
    save_json(
        "fig2_hessian_wd300.json",
        {
            "floris_version": floris.__version__,
            "wind_speed_m_per_s": 8.0,
            "wind_direction_deg": 300.0,
            "turbulence_intensity": 0.06,
            "h_deg": 5.0,
            "H_kW_per_deg2": H300.tolist(),
        },
    )

fig, axes = plt.subplots(1, 3, figsize=(15.0, 4.6), layout="constrained")
cmap = plt.get_cmap("RdBu_r").copy()
cmap.set_bad(color="#efefef")
for ax, matrix, title in [
    (axes[0], H0, r"wd $270^\circ$, baseline"),
    (axes[1], Hopt, r"wd $270^\circ$, optimum"),
    (axes[2], H300, r"wd $300^\circ$, baseline"),
]:
    display = matrix.copy()
    np.fill_diagonal(display, np.nan)
    im = ax.imshow(display, cmap=cmap, vmin=-0.75, vmax=0.75)
    ax.set_title(title, fontsize=11)
    ax.set_xticks(range(9))
    ax.set_yticks(range(9))
    ax.set_xticklabels([f"T{i + 1}" for i in range(9)], fontsize=7)
    ax.set_yticklabels([f"T{i + 1}" for i in range(9)], fontsize=7)
    for i in range(9):
        for j in range(9):
            if i != j:
                ax.text(j, i, f"{matrix[i, j]:+.2f}", ha="center", va="center", fontsize=6.2)
fig.colorbar(im, ax=axes, shrink=0.82, pad=0.02, label=r"mixed partial [kW deg$^{-2}$]")
fig.suptitle(r"Pairwise interaction matrices of the 3$\times$3 farm (central differences, $h=5^\circ$)")
fig.savefig(ROOT / "fig2_signmatrices.png", dpi=DPI)
plt.close(fig)
print("fig2 done")

# ---------------------------------------------------------------------------
# Fig. 3: decoupling at the optimum.  All values come from the uniform-h=5
# recomputation in decoupling_table.json.
# ---------------------------------------------------------------------------
case_keys = ["3x3 wd270", "3x3 wd300", "3-chain 5D", "4x4 wd270", "3x3 AEP"]
case_labels = [
    r"3$\times$3" "\n" r"wd $270^\circ$",
    r"3$\times$3" "\n" r"wd $300^\circ$",
    "3-chain",
    r"4$\times$4",
    "AEP\n12 directions",
]
opt = np.asarray([decoupling[key]["opt"] for key in case_keys], dtype=float)
zero = np.asarray([decoupling[key]["zero"] for key in case_keys], dtype=float)
x = np.arange(len(case_keys))
width = 0.38
fig, ax = plt.subplots(figsize=(6.8, 4.1))
ax.bar(x - width / 2, opt, width, label="at optimum", color="#0072B2")
ax.bar(x + width / 2, zero, width, label=r"at $\gamma=0$", color="#D55E00")
ax.set_yscale("log")
ax.set_xticks(x)
ax.set_xticklabels(case_labels)
ax.set_ylabel(r"$\|M_{\rm off}\|_F / \|\operatorname{diag}(M)\|_F$ (log scale)")
ax.set_title("Decoupling at the optimum")
ax.legend()
fig.tight_layout()
fig.savefig(ROOT / "fig3_decoupling.png", dpi=DPI)
plt.close(fig)
print("fig3 done")

# ---------------------------------------------------------------------------
# Fig. 4: TI comparative statics, read from the checked ti_sweep cache.
# ---------------------------------------------------------------------------
tis = np.asarray(ti_sweep["tis"], dtype=float)
yaw_star = np.asarray(ti_sweep["y1star"], dtype=float)
gains = np.asarray(ti_sweep["gains_pct"], dtype=float)
fig, ax1 = plt.subplots(figsize=(6.0, 4.2))
ax1.plot(tis, yaw_star, "o-", color="#0072B2")
ax1.set_xlabel("turbulence intensity")
ax1.set_ylabel(r"optimal $\gamma_1^\ast$ [deg]", color="#0072B2")
ax1.tick_params(axis="y", labelcolor="#0072B2")
ax2 = ax1.twinx()
ax2.plot(tis, gains, "s--", color="#D55E00")
ax2.set_ylabel("farm-power gain [%]", color="#D55E00")
ax2.tick_params(axis="y", labelcolor="#D55E00")
ax1.set_title("Two turbines at 5D: comparative statics in turbulence intensity")
fig.tight_layout()
fig.savefig(ROOT / "fig4_ti_sweep.png", dpi=DPI)
plt.close(fig)
print("fig4 done")

# ---------------------------------------------------------------------------
# Fig. 5: the 4x4 profile previously came from a non-versioned .npy cache.
# It now comes from the tracked uniform-h=5 decoupling table cache.
# ---------------------------------------------------------------------------
y4 = np.asarray(decoupling["4x4 wd270"]["ystar"], dtype=float).reshape(4, 4)
fig, ax = plt.subplots(figsize=(5.2, 4.4))
im = ax.imshow(y4, cmap="YlGnBu", vmin=0, vmax=30)
ax.set_title(r"4$\times$4 optimal yaw profile (SLSQP, +34.19 %)")
ax.set_xticks(range(4))
ax.set_yticks(range(4))
ax.set_xticklabels([f"column {i + 1}" for i in range(4)])
ax.set_yticklabels([f"row {i + 1}" for i in range(4)])
for i in range(4):
    for j in range(4):
        ax.text(j, i, f"{y4[i, j]:.0f}", ha="center", va="center", fontsize=11)
fig.colorbar(im, ax=ax, fraction=0.046, label="yaw [deg]")
fig.tight_layout()
fig.savefig(ROOT / "fig5_y4x4.png", dpi=DPI)
plt.close(fig)
print("fig5 done")

# ---------------------------------------------------------------------------
# Fig. 6: observed Boolean-greedy gaps and their sampled interaction-energy
# certificates, all from the fixed-seed 12-layout cache.
# ---------------------------------------------------------------------------
certs = p2["certs"]
gap_pct_popt = np.asarray([record["gap"] for record in certs], dtype=float)
# Convert the observed gap from percent of P* to percent of baseline farm power
# before dividing by a certificate expressed as percent of baseline farm power.
gap_pct_pbase = gap_pct_popt * np.asarray(
    [1.0 + record["gain_slsqp"] / 100.0 for record in certs], dtype=float
)
bound_pct_pbase = np.asarray(
    [record["bound"] / record["pbase"] * 100.0 for record in certs], dtype=float
)
certificate_ratio = gap_pct_pbase / bound_pct_pbase
trial = np.arange(1, len(certs) + 1)
fig, (ax_gap, ax_certificate) = plt.subplots(1, 2, figsize=(9.2, 3.7), gridspec_kw={"wspace": 0.33})
colors = np.where(gap_pct_popt < 0, "#E69F00", "#009E73")
ax_gap.bar(trial, gap_pct_popt, color=colors)
ax_gap.axhline(0, color="black", linewidth=0.7)
ax_gap.set_xlabel("random layout")
ax_gap.set_ylabel(r"greedy gap [% of $P^\ast$]")
ax_gap.set_title(f"Observed gaps (mean {gap_pct_popt.mean():.3f} %, max {gap_pct_popt.max():.3f} %)")
ax_gap.set_xticks(trial)
ax_gap.legend(
    handles=[Patch(facecolor="#E69F00", label="greedy above multistart SLSQP")],
    loc="upper left",
    fontsize=7,
)
ax_certificate.bar(trial, certificate_ratio, color="#56B4E9")
ax_certificate.axhline(1.0, color="#D55E00", linestyle="--", linewidth=1.0, label="certificate limit")
ax_certificate.axhline(0, color="black", linewidth=0.7)
ax_certificate.set_xlabel("random layout")
ax_certificate.set_ylabel("observed gap / sampled bound")
ax_certificate.set_title("Every observation is within its certificate")
ax_certificate.set_xticks(trial)
ax_certificate.set_ylim(-0.05, 1.05)
ax_certificate.legend(fontsize=7, loc="upper right")
fig.tight_layout()
fig.savefig(ROOT / "fig6_greedygaps.png", dpi=DPI)
plt.close(fig)
print(
    "fig6 done: mean gap = %.4f%%, max gap = %.4f%%, maximum normalized gap = %.3f"
    % (gap_pct_popt.mean(), gap_pct_popt.max(), certificate_ratio.max())
)

print("ALL PAPER-1 FIGURES DONE")
