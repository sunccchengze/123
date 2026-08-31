"""
Experiment battery: every claim in P1 must be backed by a numbered experiment.
E1 wake-model sensitivity (Jensen vs Gaussian)
E2 parameter sensitivity (tau_r, k)
E3 multi-seed stochastic statistics (5 seeds)
E4 all-or-none stimulus amplitude sweep + conduction block
E5 wave speed vs stimulus strength (F2)
E6 defibrillation time series (best protocol)
E7 forced gust cascade (from s2L data)
E8 verification path: short-run illusion vs long-run truth + settle time vs N (F1)
E9 pattern period quantization vs L/D at 3 wind speeds
"""
import numpy as np, sys, json, time
sys.path.insert(0, '/home/user/research/code')
from windfarm_excitable import simulate, spin_pattern
OUT = '/home/user/research'
R = {}
t0 = time.time()

def period_of(pat):
    """smallest p with pat[i]==pat[i%p] for the first 16 chars (period-None if >8)."""
    p = pat[:16]
    for per in range(1, 9):
        if all(p[i] == p[i % per] for i in range(len(p))):
            return per
    return None

# ---------------- E1: wake model sensitivity ----------------
print("E1: Jensen vs Gaussian wake, pattern + power (N=8 settled, U0=3.8)")
e1 = []
for Ld in [2.0, 4.0, 6.0, 8.0, 10.0, 12.0]:
    row = {'Ld': Ld}
    for wk in ['jensen', 'gaussian', 'hybrid']:
        r = simulate(N=8, T=6000, U0=3.8, L_over_D=Ld, wake=wk, sigma_u=0.0)
        sf = spin_pattern(r, warmup_frac=0.7, window_frac=0.25)
        p = r['P_tot'][int(0.85*len(r['t'])):].mean()/1e6
        pat = "".join("1" if f>0.5 else ("h" if f>0.15 else "0") for f in sf)
        row[wk] = (pat, round(p,3), period_of(pat))
    e1.append(row)
    print(f"  L/D={Ld:4.1f}  J={row['jensen']}  G={row['gaussian']}")
R['E1'] = e1

# ---------------- E2: parameter sensitivity ----------------
print("\nE2: tau_r x k grid, period at L/D in {4,8,12} (N=8, T=6000)")
e2 = []
for Ld in [4.0, 8.0, 12.0]:
    for tr in [4.0, 8.0, 12.0, 20.0]:
        for k in [0.03, 0.05, 0.08]:
            r = simulate(N=8, T=6000, U0=3.8, L_over_D=Ld, tau_r=tr, k=k, sigma_u=0.0)
            sf = spin_pattern(r, warmup_frac=0.7, window_frac=0.25)
            pat = "".join("1" if f>0.5 else ("h" if f>0.15 else "0") for f in sf)
            e2.append((Ld, tr, k, pat, period_of(pat)))
print("  periods by (Ld, tau_r, k):")
for Ld in [4.0, 8.0, 12.0]:
    print(f"   L/D={Ld}: " + "  ".join(f"tau{int(a[1])}/k{a[2]}:{a[4]}" for a in e2 if a[0]==Ld))
R['E2'] = e2

# ---------------- E3: multi-seed stochastic ----------------
print("\nE3: 5 seeds, N=16, U0=3.65, sigma=0.15, T=6000 (window 3000-6000)")
e3 = []
for s in [1,2,3,4,5]:
    r = simulate(N=16, T=6000, U0=3.65, sigma_u=0.15, seed=s)
    ups = [(e[0], e[1]) for e in r['events'] if e[2]=='up' and e[0]>3000]
    rate = np.zeros(16)
    for (tt,i) in ups: rate[i]+=1
    rate *= 1000/3000.0
    # cross-corr adjacent (lag up to 300s, step 2s)
    infl = r['inflow']; dt = 0.5; b = infl < 3.5; ns = infl.shape[1]
    def uc(x): return (x[1:]>=3.5)&(x[:-1]<3.5)
    ml=300
    cc=np.zeros(ml//2)
    for i in range(15):
        ui=uc(infl[i,:ns-ml]); uj=uc(infl[i+1,ml:]); n=len(ui)
        cc+=np.array([np.sum(ui[:n-lg]*uj[lg:]) for lg in range(0,ml,2)])
    lags_ = np.arange(0,ml,2)*dt
    peak = float(lags_[np.argmax(cc)])
    # refractory index: fraction of intervals > 3x median (turbine 4)
    b4=infl[4]; u4=np.where((b4[1:]>=3.5)&(b4[:-1]<3.5))[0]; itv=np.diff(u4)*dt
    ref = float(np.mean(itv[itv>1] > 3*np.median(itv[itv>1]))) if len(itv)>10 else None
    e3.append((s, float(rate.mean()), float(rate.std()), float(peak), ref))
    print(f"  seed={s}: mean_rate={rate.mean():.1f} std={rate.std():.1f} /1000s  cc_peak={peak:.0f}s  refr_idx={ref}")
R['E3'] = e3

# ---------------- E4/E5: amplitude sweep (all-or-none + block + speed) ----------------
print("\nE4/E5: gust amplitude sweep at t1, N=24, T=6000")
e4 = []
for A in [0.6, 0.9, 1.2, 2.0, 3.0]:
    r = simulate(N=24, T=6000, U0=3.8, gust_A=A, gust_w=0.8*126, gust_center_t=2000.0, sigma_u=0.0)
    first={}
    for (tt,i,kk) in sorted(r['events']):
        if kk=='up' and tt>2100 and i not in first: first[i]=tt
    xs_=[i for i in sorted(first) if i>0][:10]
    ys_=[first[i] for i in xs_]
    slope = float(np.polyfit(xs_, ys_, 1)[0]) if len(xs_)>=4 else None
    e4.append((A, len(xs_), max(xs_) if xs_ else -1, slope))
    print(f"  A={A}: wave reached {len(xs_)} downstream turbines (deepest t{max(xs_)+1 if xs_ else '-'}), slope={slope if slope is None else round(slope,1)} s/turb (L/U=132.6)")
R['E4'] = e4

# ---------------- E6: defib time series (best protocol) ----------------
print("\nE6: best defib protocol d=480 m=0.2 k=4, save time series")
r6a = simulate(N=24, T=6000, U0=3.8, L_over_D=4.0, sigma_u=0.0)
r6b = simulate(N=24, T=6000, U0=3.8, L_over_D=4.0, sigma_u=0.0,
               yaw_pulses=[(3000.0, 3480.0, 4, 0.2)])
np.save(f'{OUT}/e6_base.npy', np.vstack([r6a['t'], r6a['P_tot']/1e6]))
np.save(f'{OUT}/e6_defib.npy', np.vstack([r6b['t'], r6b['P_tot']/1e6]))
np.save(f'{OUT}/e6_state_base.npy', (r6a['inflow']>=3.5).astype(np.int8))
np.save(f'{OUT}/e6_state_defib.npy', (r6b['inflow']>=3.5).astype(np.int8))
pa = r6a['P_tot'][int(0.2*len(r6a['t'])):3000*2].mean()/1e6
pb = r6b['P_tot'][int(0.2*len(r6b['t'])):3000*2].mean()/1e6
qa = r6b['P_tot'][4200*2:].mean()/1e6
print(f"  baseline pre={pa:.3f}  defib pre={pb:.3f}  defib post={qa:.3f}  gain={100*(qa-pb)/pb:+.1f}%")
# pattern before/after for both
def pat_of(r, t0s, t1s):
    sf = np.mean((r['inflow'][t0s*2:t1s*2] >= 3.5), axis=1)
    return "".join("1" if f>0.5 else ("h" if f>0.15 else "0") for f in sf)
print("  base pattern pre :", pat_of(r6a, 1200, 3000)[:16])
print("  base pattern post:", pat_of(r6a, 4200, 6000)[:16])
print("  defib pattern pre:", pat_of(r6b, 1200, 3000)[:16])
print("  defib pattern post:", pat_of(r6b, 4200, 6000)[:16])
R['E6'] = dict(pre=pb, post=qa, gain_pct=100*(qa-pb)/pb)

# ---------------- E8: verification path + settle time vs N (F1) ----------------
print("\nE8a: short-run illusion: P(t) at L/D=10, N=8, T=1600 vs T=6000")
r8s = simulate(N=8, T=1600, U0=3.8, L_over_D=10.0, sigma_u=0.0)
r8l = simulate(N=8, T=6000, U0=3.8, L_over_D=10.0, sigma_u=0.0)
np.save(f'{OUT}/e8_short.npy', np.vstack([r8s['t'], r8s['P_tot']/1e6]))
np.save(f'{OUT}/e8_long.npy', np.vstack([r8l['t'], r8l['P_tot']/1e6]))
w_short = r8s['P_tot'][int(0.5*len(r8s['t'])):].mean()/1e6
w_long_head = r8l['P_tot'][int(0.5*len(r8l['t'])):int(0.5*len(r8l['t']))+int(800/0.5)].mean()/1e6
w_long_tail = r8l['P_tot'][int(0.85*len(r8l['t'])):].mean()/1e6
print(f"  T=1600 last-50% window: {w_short:.3f} MW   T=6000 same-clock window: {w_long_head:.3f}   T=6000 settled: {w_long_tail:.3f} MW")
print("\nE8b: settle time vs N (F1): L/D=10, measure tail power drift <1e-3 MW over last 500s")
e8b=[]
for N in [8, 12, 16, 24]:
    r = simulate(N=N, T=10000, U0=3.8, L_over_D=10.0, sigma_u=0.0)
    P = r['P_tot']/1e6; n = len(P)
    settle_t = None
    for t in range(1000, n-1000, 200):
        if abs(P[t+1000:].mean()-P[t:t+1000].mean()) < 1e-3 and abs(P[t+1000:].mean()-P[t+1200:t+1700].mean()) < 1e-3:
            settle_t = t*0.5; break
    theory = (N-1)*10*126/3.8
    e8b.append((N, settle_t, theory))
    print(f"  N={N:2d}: settle ~ {settle_t}s   (N-1)*L/U = {theory:.0f}s")
R['E8'] = dict(short=w_short, long_head=w_long_head, long_tail=w_long_tail, settle=e8b)

# ---------------- E9: period quantization vs L/D at 3 wind speeds ----------------
print("\nE9: pattern period vs L/D at U0 in {3.65, 3.80, 3.95}, N=24, T=6000")
e9 = []
for U0 in [3.65, 3.80, 3.95]:
    for Ld in [3.0, 4.0, 5.0, 6.0, 8.0, 10.0]:
        r = simulate(N=24, T=6000, U0=U0, L_over_D=Ld, sigma_u=0.0)
        sf = spin_pattern(r, warmup_frac=0.7, window_frac=0.25)
        pat = "".join("1" if f>0.5 else ("h" if f>0.15 else "0") for f in sf[:24])
        e9.append((U0, Ld, pat, period_of(pat)))
    print(f"  U0={U0}: " + "  ".join(f"{a[1]}:{a[3]}" for a in e9 if a[0]==U0))
R['E9'] = e9

R['elapsed_s'] = round(time.time()-t0, 1)
with open(f'{OUT}/results_experiments.json', 'w') as f:
    json.dump(R, f, indent=1, default=str)
print(f"\nBATTERY DONE in {R['elapsed_s']}s")
