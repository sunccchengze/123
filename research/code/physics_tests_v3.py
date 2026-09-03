"""
Critical physics tests after long-run correction:
A: local stimulus -> self-sustaining wave? (excitable-wave test)
B: stochastic (realistic TI) excitable firing: stats, propagation, refractory
C: short-row (N=8, fully settled) power vs L/D: clean non-monotonicity test
"""
import numpy as np, sys, json
sys.path.insert(0, '/home/user/research/code')
from windfarm_excitable import simulate, spin_pattern
OUT = '/home/user/research'
res = {}

# ---------- A: local stimulus -> self-sustaining wave? ----------
print("="*60, "\nA: local stimulus (narrow gust hitting only t1), then removed")
# narrow gust (width 0.8D) centered on t1 at t=2000, amplitude large enough to fire t1
# after it passes, does a firing wave continue down the row?
rA = simulate(N=24, T=6000, U0=3.8, gust_A=2.0, gust_w=0.8*126, gust_center_t=2000.0, sigma_u=0.0)
# baseline for comparison
rAb = simulate(N=24, T=6000, U0=3.8, sigma_u=0.0)
def ev_in(r, t0, t1):
    return [(e[0], e[1]) for e in r['events'] if e[2]=='up' and t0<=e[0]<=t1]
upsA = ev_in(rA, 1900, 4000)
upsAb = ev_in(rAb, 1900, 4000)
print("  baseline firings 1900-4000 (no stimulus):", len(upsAb))
print("  stimulus firings 1900-4000:")
for (tt,i) in upsA:
    print(f"     t={tt:7.1f}  t{i+1:2d}")
# How far does the wave go after gust leaves t1 (gust center at t1 at 2000, width 0.8D -> gone by ~2050)?
after = [ (tt,i) for (tt,i) in upsA if tt>2100 ]
maxidx = max([i for (tt,i) in after], default=-1)
print(f"  -> after stimulus gone (t>2100): {len(after)} firings, deepest turbine reached: t{maxidx+1}")
np.save(f'{OUT}/A_inflow.npy', rA['inflow']); np.save(f'{OUT}/A_CT.npy', rA['CT']); np.save(f'{OUT}/A_t.npy', rA['t'])
res['A'] = dict(after_firings=len(after), deepest=maxidx+1)

# ---------- B: stochastic excitable regime (realistic) ----------
print("="*60, "\nB: stochastic regime (sigma_u=0.15 m/s ~ 4% TI at 3.8), U0=3.65")
rB = simulate(N=16, T=8000, U0=3.65, sigma_u=0.15, seed=11)
upB = [(e[0], e[1]) for e in rB['events'] if e[2]=='up' and e[0]>3000]
downB = [(e[0], e[1]) for e in rB['events'] if e[2]=='down' and e[0]>3000]
print(f"  total restarts t>3000: {len(upB)}, stops: {len(downB)}")
# firing rate per turbine
rate = np.zeros(16)
for (tt,i) in upB: rate[i]+=1
Tobs = 5000.0
print("  firing rate per turbine (per 1000s):", np.round(rate*1000/Tobs,2))
# refractory: inter-event interval for the most active turbine
act = int(np.argmax(rate))
itv = np.diff(sorted([tt for (tt,i) in upB if i==act]))
print(f"  most active turbine t{act+1}: n={len(itv)}, min inter-firing={itv.min():.1f}s (refractory lower bound), mean={itv.mean():.1f}s")
# propagation: for each firing at (t,i), does t i+1 fire within [t, t+L/U+tau]?
L = 4.0*126; tau_ad = L/3.65
prop=0; tot=0
evs = sorted([(tt,i) for (tt,i) in upB])
for k,(tt,i) in enumerate(evs):
    if i<15:
        # find next firing at i+1 after tt
        cand=[ (t2,i2) for (t2,i2) in evs if i2==i+1 and t2>=tt and t2<=tt+tau_ad+30]
        if cand:
            tot+=1; prop+=1
print(f"  propagation: {prop}/{tot} firings followed by downstream firing within advection window")
np.save(f'{OUT}/B_inflow.npy', rB['inflow']); np.save(f'{OUT}/B_CT.npy', rB['CT']); np.save(f'{OUT}/B_t.npy', rB['t']); np.save(f'{OUT}/B_events.npy', np.array(upB, dtype=object))
res['B'] = dict(restarts=len(upB), rate=np.round(rate*1000/Tobs,2).tolist(),
                refractory_min=float(itv.min()) if len(itv) else None,
                prop=prop, tot=tot)

# ---------- C: short row N=8, settled, power vs L/D ----------
print("="*60, "\nC: short row N=8 (fully settled by T=6000), power vs L/D at U0=3.8")
powC=[]
for Ld in [2.0,2.5,3.0,3.5,4.0,5.0,6.0,8.0,10.0,12.0]:
    rC = simulate(N=8, T=6000, U0=3.8, L_over_D=Ld, sigma_u=0.0)
    sf = spin_pattern(rC, warmup_frac=0.7, window_frac=0.25)
    p = rC['P_tot'][int(0.85*len(rC['t'])):].mean()/1e6
    settle = rC['P_tot'][int(0.85*len(rC['t'])):].mean() - rC['P_tot'][int(0.75*len(rC['t'])):int(0.85*len(rC['t']))].mean()
    pat = "".join("1" if f>0.5 else ("h" if f>0.15 else "0") for f in sf)
    powC.append((Ld, p, settle, pat))
    print(f"  L/D={Ld:4.1f}  P={p:.3f}MW  settle={settle:+.4f}  pat={pat}")
res['C'] = powC
np.save(f'{OUT}/C_pow.npy', np.array([(a,b) for a,b,_,_ in powC]))

with open(f'{OUT}/results_v3.json','w') as f:
    json.dump(res, f, indent=1, default=str)
print("\nDONE v3.")
