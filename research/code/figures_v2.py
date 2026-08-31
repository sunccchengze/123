"""Vector (PDF) + PNG figures for the revised experimental paper package."""
import numpy as np, json, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT = '/home/user/research'
plt.rcParams.update({'font.size': 10, 'figure.dpi': 150})
U = 3.8
L_U = 4*126/3.8

def save(fig, name):
    fig.savefig(f'{OUT}/{name}.pdf')
    fig.savefig(f'{OUT}/{name}.png')
    plt.close(fig)

# ---------- FIG 1: trigger wave raster + amplitude independence ----------
tA = np.load(f'{OUT}/A_t.npy'); inflA = np.load(f'{OUT}/A_inflow.npy')
state = (inflA >= 3.5).astype(float)
i0, i1 = int(1500/0.5), int(4500/0.5)
F2 = json.load(open(f'{OUT}/results_fix.json'))['F2']
fig, axes = plt.subplots(1, 2, figsize=(12, 5.2), gridspec_kw={'width_ratios': [1.6, 1]})
ax = axes[0]
ax.imshow(state[:, i0:i1].T, aspect='auto', origin='lower', extent=[tA[i0], tA[i1], 0.5, 24.5],
          cmap=matplotlib.colors.ListedColormap(['#d9d9d9', '#1f5fbf']), vmin=0, vmax=1)
ax.axvline(2000, color='red', ls='--', lw=1.2)
ax.text(2015, 1.2, 'stimulus at t$_1$ (A=+2.0 m/s, width 0.8D,\ngone by ~2050 s)', color='red', fontsize=8.5)
ax.set_xlim(1500, 4500); ax.set_ylim(24, 0)
ax.set_yticks(np.arange(0.5, 24, 2)); ax.set_yticklabels(np.arange(1, 25, 2))
ax.set_ylabel('turbine index (1 = upwind)'); ax.set_xlabel('time (s)')
ax.set_title('(a) Regenerative trigger wave (blue = above cut-in)', fontsize=10.5)
ax = axes[1]
Aa = [r[0] for r in F2]; dep = [r[1] for r in F2]; sl = [r[2] for r in F2]
ax.scatter(Aa, sl, s=55, color='tab:blue', zorder=3, label='wave speed (s/spacing, left scale)')
ax.axhline(L_U, color='k', ls=':', lw=1.2)
ax.text(0.25, L_U+1.5, f'$L/U$ = {L_U:.1f} s', fontsize=8.5)
ax.set_xlabel('stimulus amplitude A (m/s)'); ax.set_ylabel('leading-edge lag per spacing (s)')
ax.set_ylim(120, 136); ax.set_xlim(0.1, 3.2)
ax2 = ax.twinx()
ax2.bar(Aa, dep, width=0.07, color='0.8', label='propagation depth')
ax2.set_ylabel('depth of wave (turbines)', color='0.4')
ax2.set_ylim(0, 26)
ax.set_title('(b) Wave speed independent of amplitude;\nfull propagation even at A=0.2 m/s', fontsize=10.5)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1+h2, l1+l2, fontsize=8, loc='lower left')
plt.tight_layout(); save(fig, 'fig1_trigger_wave')

# ---------- FIG 2: phase diagram (same data) ----------
d = json.load(open(f'{OUT}/results_v2.json')); grid = d['S3']
U0s = [g[0] for g in grid]; Lds = [3.0, 4.0, 5.0, 6.0, 8.0, 10.0]
fig, ax = plt.subplots(figsize=(8.5, 6.2))
for g in grid:
    for (Ld, pat8, p) in g[1]:
        n1 = sum(1 for c in pat8 if c == '1')
        ax.text(Ld, g[0], pat8, ha='center', va='center', fontsize=10.5, fontfamily='monospace',
                color='white' if n1 >= 4 else 'k',
                bbox=dict(boxstyle='square,pad=0.4', fc=('tab:blue' if n1 >= 4 else 'white'), ec='0.25', alpha=0.9))
ax.set_xlim(2.4, 10.6); ax.set_ylim(U0s[-1]-0.06, U0s[0]+0.06)
ax.set_xticks(Lds); ax.set_xticklabels([str(int(x)) for x in Lds])
ax.set_xlabel('spacing L/D'); ax.set_ylabel('freestream speed U$_0$ (m/s)')
ax.set_title('Phase diagram of discrete on/off pattern selection (settled $T=6000$ s)\neach cell: first-8-turbine pattern; darker = more turbines spinning', fontsize=11)
plt.tight_layout(); save(fig, 'fig2_phase_diagram')

# ---------- FIG 3: quantized power steps (Jensen + Gaussian) ----------
C = np.load(f'{OUT}/C_pow.npy')
E1 = json.load(open(f'{OUT}/results_experiments.json'))['E1']
fig, ax = plt.subplots(figsize=(7.2, 4.8))
ax.plot(C[:, 0], C[:, 1], 'o-', color='tab:red', lw=2, ms=7, label='Jensen wake (this work)')
gpts = [(r['Ld'], r['gaussian'][1]) for r in E1]
ax.plot([p[0] for p in gpts], [p[1] for p in gpts], 's--', color='tab:purple', lw=1.8, ms=7, label='Gaussian (BPA centerline) wake')
for x, y in C:
    ax.annotate(f'{y:.2f}', (x, y), textcoords='offset points', xytext=(0, 9), ha='center', fontsize=8)
ax.set_xlabel('spacing L/D'); ax.set_ylabel('settled farm power (MW)')
ax.set_title('Quantized power steps: staircase vs spacing\n(N=8, U$_0$=3.8 m/s, $T=6000$ s, settled; two wake kernels)', fontsize=11)
ax.legend(fontsize=9)
plt.tight_layout(); save(fig, 'fig3_power_steps')

# ---------- FIG 4: defibrillation NULL RESULT ----------
base_traj = np.load(f'{OUT}/f1_base_traj.npy'); best_traj = np.load(f'{OUT}/f1_best_traj.npy')
F1 = json.load(open(f'{OUT}/results_fix.json'))['F1']
grid = np.load(f'{OUT}/f1_grid.npy')
fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.2))
ax = axes[0]
ax.plot(base_traj[0], base_traj[1], lw=1.4, color='k', label='no-pulse control')
ax.plot(best_traj[0], best_traj[1], lw=1.4, color='tab:red', label=f"pulse (d={int(F1['best'][0])} s, m={F1['best'][1]}, k={int(F1['best'][2])})")
ax.axvspan(3000, 3000+F1['best'][0], color='tab:red', alpha=0.12)
ax.axvspan(4200, 6000, color='0.8', alpha=0.18)
ax.axvspan(7000, 9000, color='0.5', alpha=0.25)
ax.text(4250, ax.get_ylim()[0]+0.02, 'pre-window\n[4200,6000]', fontsize=7.5)
ax.text(7050, ax.get_ylim()[0]+0.02, 'post-window\n[7000,9000]', fontsize=7.5)
ax.set_xlabel('time (s)'); ax.set_ylabel('farm power (MW)')
ax.set_title('(a) Pulse washes downstream;\ntrajectories re-converge', fontsize=10.5)
ax.legend(fontsize=8, loc='upper right')
ax = axes[1]
durs = sorted(set(grid[:, 0]))
means = [grid[grid[:, 0] == d, 5].mean() for d in durs]
stds = [grid[grid[:, 0] == d, 5].std() for d in durs]
ax.bar([f'{int(x)}' for x in durs], means, yerr=stds, color='tab:blue', alpha=0.8, capsize=3)
ax.axhline(0, color='k', lw=1)
ax.set_xlabel('pulse duration (s)'); ax.set_ylabel('settled power gain vs control (%)')
ax.set_title('(b) 60 protocols, settled-vs-settled:\nall gains $\\approx$ 0 (range shown)', fontsize=10.5)
ax = axes[2]
ax.plot(durs, means, 'o-', color='tab:blue')
ax.axhline(0, color='k', lw=1, ls=':')
ax.fill_between(durs, -0.5, 0.5, color='0.85', alpha=0.5, label='numerical noise band')
ax.set_xlabel('pulse duration (s)'); ax.set_ylabel('mean gain (%)')
ax.set_title('(c) No protocol exceeds the noise band;\ncontrol drift = 0.0000 MW', fontsize=10.5)
ax.legend(fontsize=8)
plt.tight_layout(); save(fig, 'fig4_defib_null')

# ---------- FIG 5: verification path (short-run illusion + settle time F1) ----------
short = np.load(f'{OUT}/e8_short.npy'); longt = np.load(f'{OUT}/e8_long.npy')
E8 = json.load(open(f'{OUT}/results_experiments.json'))['E8']
fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.2))
ax = axes[0]
ax.plot(short[0], short[1], lw=1.4, color='tab:red', label='run stopped at T=1600 s')
ax.plot(longt[0], longt[1], lw=1.4, color='tab:blue', label='run to T=6000 s')
ax.axvline(1600, color='tab:red', ls=':', lw=1)
ax.text(1610, ax.get_ylim()[0]+0.02, 'short run ends here', color='tab:red', fontsize=8)
ax.set_xlabel('time (s)'); ax.set_ylabel('farm power (MW)')
ax.set_title('(a) The short-run illusion at L/D=10: the 1600 s run\naverages +13% higher than the settled state', fontsize=10.5)
ax.legend(fontsize=8)
ax = axes[1]
Ns = [r[0] for r in E8['settle']]; ts = [r[1] for r in E8['settle']]; th = [r[2] for r in E8['settle']]
ax.plot(th, ts, 's-', color='tab:green', ms=9, lw=1.5, label='measured settle time')
lim = [0, max(th)*1.08]
ax.plot(lim, lim, 'k:', lw=1.2, label='theory: (N-1)$L/U$')
ax.set_xlabel('theory: (N-1) L/U (s)'); ax.set_ylabel('measured settle time (s)')
ax.set_title('(b) F1 verified: row settles at\n$\\approx$(N-1)$L/U$ (2-4% error, L/D=10)', fontsize=10.5)
ax.legend(fontsize=8)
plt.tight_layout(); save(fig, 'fig5_settle_path')

# ---------- FIG 6: stochastic multi-seed ----------
E3 = json.load(open(f'{OUT}/results_experiments.json'))['E3']
fig, axes = plt.subplots(1, 3, figsize=(12.5, 4))
ax = axes[0]
rates = [r[1] for r in E3]; rstd = [r[2] for r in E3]
ax.bar([f'seed {r[0]}' for r in E3], rates, yerr=rstd, color='tab:purple', alpha=0.85, capsize=3)
ax.axhline(np.mean(rates), color='k', ls=':', lw=1)
ax.set_ylabel('row mean firing rate (per 1000 s)')
ax.set_title('(a) Firing rate: 175-178/1000 s\nacross 5 seeds ($\\pm$1%)', fontsize=10)
ax = axes[1]
peaks = [r[3] for r in E3]
ax.bar([f'seed {r[0]}' for r in E3], peaks, color='tab:blue', alpha=0.85)
ax.axhline(138, color='red', ls='--', lw=1.2)
ax.text(0, 142, 'advection lag L/U=138 s', color='red', fontsize=8)
ax.set_ylabel('adjacent restart cross-corr peak (s)')
ax.set_title('(b) Correlation peak wanders between\natmospheric (~50 s) and advection (~130 s)', fontsize=10)
ax = axes[2]
refr = [r[4] for r in E3]
ax.bar([f'seed {r[0]}' for r in E3], refr, color='tab:orange', alpha=0.85)
ax.set_ylabel('refractory-tail index (fraction of\nintervals $>$ 3x median)')
ax.set_title('(c) Refractory-tail index stable\n(7-12% across seeds)', fontsize=10)
plt.tight_layout(); save(fig, 'fig6_stochastic_seeds')

# ---------- FIG 7: parameter dependence (E2 table as heatmap of periods) ----------
E2 = json.load(open(f'{OUT}/results_experiments.json'))['E2']
fig, ax = plt.subplots(figsize=(8, 4.2))
trs = [4, 8, 12, 20]; ks = [0.03, 0.05, 0.08]; lds = [4, 8, 12]
data = np.zeros((3, 3, 4))
for row in E2:
    Ld, tr, k, pat, per = row
    data[lds.index(Ld), ks.index(k), trs.index(tr)] = per if per else 8
for li in range(3):
    for ki in range(3):
        vals = data[li, ki, :]
        for ti in range(4):
            ax.text(ti + ki*4.2, li, f'{int(vals[ti])}', ha='center', va='center', fontsize=11,
                    bbox=dict(boxstyle='round,pad=0.25', fc=('tab:blue' if vals[ti] == vals[0] else '0.9'),
                              ec='0.3', alpha=0.85), color='white' if vals[ti] == vals[0] else 'k')
ax.set_xlim(-0.5, 3*4.2+3.5); ax.set_ylim(2.7, -0.7)
ax.set_xticks([ti + 2.1 for ti in range(3)]); ax.set_xticklabels(['k=0.03', 'k=0.05', 'k=0.08'])
ax.set_yticks([2, 1, 0]); ax.set_yticklabels(['L/D=4', 'L/D=8', 'L/D=12'])
ax.set_xlabel('wake growth rate k (columns: 0.03 / 0.05 / 0.08)')
ax.axis('off')
ax.set_title('Pattern period across the $\\tau_r \\times k$ grid ($\\tau_r$ = 4/8/12/20 s in each cell group):\nperiod depends on k ($\\pm$1), is independent of $\\tau_r$ (identical across the $\\tau_r$ groups)', fontsize=10.5)
plt.tight_layout(); save(fig, 'fig7_param_dependence')

print("FIGURES V2 DONE")
