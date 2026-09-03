"""
Fix battery (integrity corrections after first battery):
F1: rigorous defibrillation: settled-vs-settled, T=9000, no-pulse control,
    full 60-case grid. Pulse [3000, 3000+d]; re-settle completes by 3000+d+(N-1)L/U.
    before window [4200,6000] (both runs settled there for the pulse-free branch),
    after window [7000,9000] (post re-settle for d<=480: 3480+3050=6530 < 7000).
    control: no-pulse run must have equal power in both windows.
F2: trigger wave full depth (all 23 downstream turbines) + fine amplitude sweep.
F3: robust period_of (tolerance) for E9 re-run.
F4: save baseline P_tot trajectory (verification-path figure).
"""
import numpy as np, sys, json, time
sys.path.insert(0, '/home/user/research/code')
from windfarm_excitable import simulate
OUT = '/home/user/research'
R = {}
t0 = time.time()
L_U = 4*126/3.8  # 132.636 s

def period_of_tol(pat, tol=0.8):
    p = pat[:24]
    bestp = None
    for per in range(1, 9):
        agree = sum(1 for i in range(len(p)) if p[i] == p[i % per]) / len(p)
        if agree >= tol:
            bestp = per; break
    return bestp

# ---------- F1: rigorous defibrillation grid, T=9000 ----------
print("F1: rigorous defibrillation grid (T=9000, settled-vs-settled, control run)")
def defib_run(dur, mult, kk, T=9000.0):
    r = simulate(N=24, T=T, U0=3.8, L_over_D=4.0, sigma_u=0.0,
                 yaw_pulses=[(3000.0, 3000.0+dur, kk, mult)])
    P = r['P_tot']/1e6
    pre = P[int(4200/0.5):int(6000/0.5)].mean()
    post = P[int(7000/0.5):].mean()
    return r, pre, post

r0, pre0, post0 = defib_run(0, 1.0, 1)  # no-pulse control (dur=0 -> empty pulse window)
ctrl_drift = post0 - pre0
print(f"  CONTROL (no pulse): pre={pre0:.4f}  post={post0:.4f}  drift={ctrl_drift:+.4f} MW")
np.save(f'{OUT}/f1_base_traj.npy', np.vstack([r0['t'], r0['P_tot']/1e6]))

grid = []
for dur in [30, 60, 120, 240, 480]:
    for mult in [0.0, 0.2, 0.5]:
        for kk in [1, 2, 4, 8]:
            r, pre, post = defib_run(dur, mult, kk)
            gain = 100*(post - post0)/post0  # vs control's post (same clock)
            grid.append((dur, mult, kk, float(pre), float(post), float(gain)))
grid = np.array(grid)
best = grid[np.argmax(grid[:,5])]
print(f"  grid: n={len(grid)}, gains {grid[:,5].min():+.1f}% .. {grid[:,5].max():+.1f}%")
print(f"  BEST: dur={int(best[0])} mult={best[1]} k={int(best[2])}  pre={best[3]:.3f} post={best[4]:.3f} gain={best[5]:+.1f}% (vs control)")
np.save(f'{OUT}/f1_grid.npy', grid)
R['F1'] = dict(control=dict(pre=float(pre0), post=float(post0), drift=float(ctrl_drift)),
               gains_pct=[float(grid[:,5].min()), float(grid[:,5].max())],
               best=[int(best[0]), float(best[1]), int(best[2]), float(best[3]), float(best[4]), float(best[5])])
# save best-protocol series
rb, preb, postb = defib_run(int(best[0]), float(best[1]), int(best[2]))
np.save(f'{OUT}/f1_best_traj.npy', np.vstack([rb['t'], rb['P_tot']/1e6]))
np.save(f'{OUT}/f1_best_state.npy', (rb['inflow']>=3.5).astype(np.int8))
np.save(f'{OUT}/f1_base_state.npy', (r0['inflow']>=3.5).astype(np.int8))

# ---------- F2: trigger wave full depth + fine amplitudes ----------
print("\nF2: trigger wave vs amplitude, full depth (23 downstream), N=24, T=6000")
f2 = []
for A in [0.2, 0.3, 0.4, 0.6, 1.0, 2.0, 3.0]:
    r = simulate(N=24, T=6000, U0=3.8, gust_A=A, gust_w=0.8*126, gust_center_t=2000.0, sigma_u=0.0)
    first = {}
    for (tt, i, kk) in sorted(r['events']):
        if kk == 'up' and tt > 2100 and i not in first:
            first[i] = tt
    idxs = sorted(i for i in first if i > 0)
    depth = len(idxs)
    slope = float(np.polyfit(idxs[:min(len(idxs),10)], [first[i] for i in idxs[:min(len(idxs),10)]], 1)[0]) if len(idxs) >= 4 else None
    f2.append((A, depth, slope))
    print(f"  A={A:.1f}: wave depth={depth}/23   slope={slope if slope is None else round(slope,1)} s/turb")
R['F2'] = f2

# ---------- F3: E9 redo with robust period ----------
print("\nF3: period vs L/D at U0 in {3.65, 3.80, 3.95}, N=24, T=6000 (robust period)")
e9 = []
for U0 in [3.65, 3.80, 3.95]:
    for Ld in [3.0, 4.0, 5.0, 6.0, 8.0, 10.0]:
        r = simulate(N=24, T=6000, U0=U0, L_over_D=Ld, sigma_u=0.0)
        sf = np.mean((r['inflow'][:, int(0.7*len(r['t'])):int(0.95*len(r['t']))] >= r['u_cut'] if 'u_cut' in r else (r['inflow'][:, int(0.7*len(r['t'])):int(0.95*len(r['t']))] >= 3.5)), axis=1)
        pat = "".join("1" if f > 0.5 else ("h" if f > 0.15 else "0") for f in sf)
        e9.append((U0, Ld, pat, period_of_tol(pat)))
    print(f"  U0={U0}: " + "  ".join(f"{a[1]}:{a[3]}" for a in e9 if a[0] == U0))
R['F3'] = e9

R['elapsed_s'] = round(time.time()-t0, 1)
with open(f'{OUT}/results_fix.json', 'w') as f:
    json.dump(R, f, indent=1, default=str)
print(f"\nFIX BATTERY DONE in {R['elapsed_s']}s")
