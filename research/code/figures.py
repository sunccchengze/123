"""Flagship figures (robust)."""
import numpy as np, sys, json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0, '/home/user/research/code')
OUT = '/home/user/research'
plt.rcParams.update({'font.size': 11, 'figure.dpi': 150})
u_cut = 3.5

# ---------- B2: corrected propagation via cross-correlation ----------
t = np.load(f'{OUT}/B_t.npy')
infl = np.load(f'{OUT}/B_inflow.npy')
N = infl.shape[0]; nsteps = infl.shape[1]
dt = t[1]-t[0]
L = 4.0*126; tau_ad = L/3.65
b = infl < u_cut
maxlag = 300
def upcross(x):
    return (x[1:] >= u_cut) & (x[:-1] < u_cut)

cc_real = np.zeros(maxlag//2)
for i in range(N-1):
    ui = upcross(infl[i, :nsteps-maxlag])
    uj = upcross(infl[i+1, maxlag:])
    n = len(ui)
    cc_real += np.array([np.sum(ui[:n-lg]*uj[lg:]) for lg in range(0, maxlag, 2)])
lags = np.arange(0, maxlag, 2)*dt
peak_real = lags[np.argmax(cc_real)]

rng = np.random.default_rng(3)
cc_surr = np.zeros(maxlag//2)
for i in range(N-1):
    ui = upcross(infl[i, :nsteps-maxlag]).astype(float)
    uj = upcross(infl[i+1, maxlag:]).astype(float)
    n = len(ui)
    ui_s = ui.copy(); rng.shuffle(ui_s)
    cc_surr += np.array([np.sum(ui_s[:n-lg]*uj[lg:]) for lg in range(0, maxlag, 2)])
peak_surr = lags[np.argmax(cc_surr)]
ia = int(round(tau_ad/dt/2))
print(f"B2 cross-corr: real peak lag={peak_real:.0f}s, surrogate peak={peak_surr:.0f}s, advection={tau_ad:.0f}s, lift at advection={cc_real[ia]/max(cc_surr[ia],1e-9):.2f}x")

# ---------- FIGURE 1: excitable trigger wave (raster) ----------
tA = np.load(f'{OUT}/A_t.npy'); inflA = np.load(f'{OUT}/A_inflow.npy')
state = (inflA >= u_cut).astype(float)
i0, i1 = int(1500/0.5), int(4500/0.5)
fig, ax = plt.subplots(figsize=(9.5, 6.5))
ax.imshow(state[:, i0:i1].T, aspect='auto', origin='lower',
          extent=[tA[i0], tA[i1], 0.5, 24.5],
          cmap=matplotlib.colors.ListedColormap(['#d9d9d9', '#1f5fbf']), vmin=0, vmax=1)
ax.invert_yaxis()
ax.set_ylim(24, 0)
ax.set_xlim(1500, 4500)
ax.set_ylabel('turbine index (1 = upwind)')
ax.set_xlabel('time (s)')
ax.axvline(2000, color='red', ls='--', lw=1.2)
ax.text(2015, 1.0, 'local stimulus at t$_1$\n(width 0.8D, gone by ~2050 s)', color='red', fontsize=9)
ax.set_yticks(np.arange(0.5, 24, 2)); ax.set_yticklabels(np.arange(1, 25, 2))
ax.set_title('Excitable trigger wave: a local suprathreshold stimulus launches a\nregenerative downstream wave (blue = above cut-in = firing)', fontsize=12)
plt.tight_layout(); plt.savefig(f'{OUT}/fig1_trigger_wave.png'); plt.close()

# ---------- FIGURE 2: phase diagram ----------
d = json.load(open(f'{OUT}/results_v2.json')); grid = d['S3']
U0s = [g[0] for g in grid]; Lds = [3.0,4.0,5.0,6.0,8.0,10.0]
fig, ax = plt.subplots(figsize=(8.5, 6.2))
for gi, g in enumerate(grid):
    for li, (Ld, pat8, p) in enumerate(g[1]):
        n1 = sum(1 for c in pat8 if c=='1')
        ax.text(Ld, g[0], pat8, ha='center', va='center', fontsize=10.5, fontfamily='monospace',
                color='white' if n1>=4 else 'k',
                bbox=dict(boxstyle='square,pad=0.4', fc=('tab:blue' if n1>=4 else 'white'), ec='0.25', alpha=0.9))
ax.set_xlim(2.4, 10.6); ax.set_ylim(U0s[-1]-0.06, U0s[0]+0.06)
ax.set_xticks(Lds); ax.set_xticklabels([str(int(x)) for x in Lds])
ax.set_xlabel('spacing L/D'); ax.set_ylabel('freestream speed U$_0$ (m/s)')
ax.set_title('Discrete on/off pattern selection: phase diagram in (U$_0$, L/D)\neach cell = first-8-turbine pattern (1 = spinning); darker = more turbines ON', fontsize=12)
plt.tight_layout(); plt.savefig(f'{OUT}/fig2_phase_diagram.png'); plt.close()

# ---------- FIGURE 3: quantized power steps ----------
C = np.load(f'{OUT}/C_pow.npy')
fig, ax = plt.subplots(figsize=(7, 4.6))
ax.plot(C[:,0], C[:,1], 'o-', color='tab:red', lw=2, ms=7, label='simulated power')
ax.step(C[:,0], C[:,1], where='mid', color='tab:red', alpha=0.3)
for x,y in C:
    ax.annotate(f'{y:.2f}', (x,y), textcoords='offset points', xytext=(0,9), ha='center', fontsize=8)
ax.set_xlabel('spacing L/D'); ax.set_ylabel('steady farm power (MW)')
ax.set_title('Quantized power steps in the near-cut-in regime\n(N=8, U$_0$=3.8 m/s, settled T=6000 s)', fontsize=11)
plt.tight_layout(); plt.savefig(f'{OUT}/fig3_power_steps.png'); plt.close()

# ---------- FIGURE 4: defibrillation ----------
scan = np.load(f'{OUT}/s4_scan.npy')
gain = (scan[:,4]-scan[:,3])*100
fig, axes = plt.subplots(1, 2, figsize=(10, 4.3))
ax = axes[0]
for kk in sorted(set(scan[:,2])):
    m = scan[:,2]==kk
    ax.scatter(scan[m,0], gain[m], label=f'k={int(kk)}', s=40, alpha=0.8)
ax.set_xscale('log'); ax.set_xlabel('pulse duration (s)'); ax.set_ylabel('power gain (%)')
ax.set_title('Defibrillation gain vs duration (strength & k in legend)'); ax.legend(fontsize=8)
ax = axes[1]
durs = sorted(set(scan[:,0]))
ax.bar([str(int(x)) for x in durs], [gain[scan[:,0]==x].mean() for x in durs], color='tab:green')
ax.set_xlabel('pulse duration (s)'); ax.set_ylabel('mean gain (%)')
ax.set_title('Broad optimum: max ~+13% (480 s, k=4, x0.2)')
plt.tight_layout(); plt.savefig(f'{OUT}/fig4_defibrillation.png'); plt.close()

# ---------- FIGURE 5: stochastic firing + refractory + cross-corr ----------
CTA = np.load(f'{OUT}/A_CT.npy'); tA2 = tA
fig, axes = plt.subplots(1, 3, figsize=(12.5, 4))
ax = axes[0]
j0, j1 = int(2500/0.5), int(4000/0.5)
for i in [0, 3, 7]:
    ax.plot(tA2[j0:j1], CTA[i, j0:j1], lw=0.8, label=f'turbine {i+1}')
ax.axhline(0.05, color='k', ls=':', lw=1)
ax.set_xlabel('time (s)'); ax.set_ylabel('thrust coeff $C_T$')
ax.set_title('Refractory tail: slow $C_T$ recovery\n(wake re-establishment) after each stop'); ax.legend(fontsize=8)
ax = axes[1]
ax.plot(lags, cc_real, label='adjacent (real)')
ax.plot(lags, cc_surr, label='surrogate (shuffled)')
ax.axvline(tau_ad, color='red', ls='--', lw=1)
ax.text(tau_ad+4, cc_real.max()*0.85, f'L/U = {tau_ad:.0f}s', color='red', fontsize=8)
ax.set_xlabel('time lag (s)'); ax.set_ylabel('restart cross-correlation')
ax.set_title(f'Propagation peak at advection lag\n(real peak {peak_real:.0f}s vs surrogate {peak_surr:.0f}s)'); ax.legend(fontsize=8)
ax = axes[2]
b5 = infl[4]
up5 = np.where((b5[1:]>=u_cut)&(b5[:-1]<u_cut))[0]
itv5 = np.diff(up5)*dt
ax.hist(itv5[itv5>1], bins=40, color='tab:purple', alpha=0.85)
ax.set_xlabel('inter-firing interval (s)'); ax.set_ylabel('count')
ax.set_title('Inter-firing interval distribution\n(turbine 5, stochastic regime, TI=4%)')
plt.tight_layout(); plt.savefig(f'{OUT}/fig5_stochastic.png'); plt.close()
print("FIGURES DONE")
