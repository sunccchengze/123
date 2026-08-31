"""
Characterization v2 — long runs (T=6000s) to separate true steady states from
initial-condition transients. Also maps the (U0, L/D) phase diagram.
"""
import numpy as np, sys, json
sys.path.insert(0, '/home/user/research/code')
from windfarm_excitable import simulate, spin_pattern

OUT = '/home/user/research'
results = {}

# ---------- S1-LONG: steady patterns, long run ----------
print("S1-LONG: steady patterns (T=6000s)")
rows = []
for Ld in [2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0]:
    r = simulate(N=24, T=6000, U0=3.8, L_over_D=Ld, sigma_u=0.0, gust_A=0.0, dt=0.5)
    sf = spin_pattern(r, warmup_frac=0.7, window_frac=0.25)
    pat = "".join("1" if f > 0.5 else ("h" if f > 0.15 else "0") for f in sf)
    p = r['P_tot'][int(0.85*len(r['t'])):].mean()/1e6
    # check settle: compare two late windows
    w1 = r['P_tot'][int(0.75*len(r['t'])):int(0.85*len(r['t']))].mean()/1e6
    w2 = p
    rows.append(dict(Ld=Ld, pat=pat, power=p, settle=w2-w1, spinfracs=np.round(sf,2).tolist()))
    print(f"  L/D={Ld:4.1f}  {pat}  P={p:.3f}MW  settle={w2-w1:+.4f}")
results['S1'] = rows

# ---------- S2-LONG: gust cascade with long run ----------
print("\nS2-LONG: gust A=+0.8, T=6000, gust center at t1 t=2400")
r = simulate(N=24, T=6000, U0=3.8, gust_A=0.8, gust_center_t=2400.0, sigma_u=0.0, dt=0.5)
np.save(f'{OUT}/s2L_inflow.npy', r['inflow']); np.save(f'{OUT}/s2L_CT.npy', r['CT']); np.save(f'{OUT}/s2L_t.npy', r['t'])
# firing events
ev = r['events']
t0, t1 = 2200, 4200
ups = [(e[0], e[1]) for e in ev if e[2]=='up' and t0 <= e[0] <= t1]
print("  firing events (t, turbine) in [2200,4200]:")
for (tt, i) in ups:
    print(f"    t={tt:7.1f}  t{i+1:2d}")
# baseline (no gust) same window for comparison
rb = simulate(N=24, T=6000, U0=3.8, sigma_u=0.0, dt=0.5)
np.save(f'{OUT}/s2L_base_inflow.npy', rb['inflow']); np.save(f'{OUT}/s2L_base_CT.npy', rb['CT'])
upb = [(e[0], e[1]) for e in rb['events'] if e[2]=='up' and t0 <= e[0] <= t1]
print(f"  baseline (no gust) firing events in same window: {len(upb)}")
for (tt, i) in upb[:40]:
    print(f"    t={tt:7.1f}  t{i+1:2d}")

# ---------- S3-LONG: phase diagram (U0, L/D) ----------
print("\nS3: phase diagram (U0 x L/D), T=6000")
grid = []
for U0 in [3.55, 3.60, 3.65, 3.70, 3.75, 3.80, 3.85, 3.90, 3.95, 4.00, 4.10, 4.30]:
    row = []
    for Ld in [3.0, 4.0, 5.0, 6.0, 8.0, 10.0]:
        r = simulate(N=24, T=6000, U0=U0, L_over_D=Ld, sigma_u=0.0, gust_A=0.0, dt=0.5)
        sf = spin_pattern(r, warmup_frac=0.7, window_frac=0.25)
        pat = "".join("1" if f > 0.5 else ("h" if f > 0.15 else "0") for f in sf)
        # extract period of leading pattern: find repeating unit in first 12 chars
        lead = pat[:12]
        p = r['P_tot'][int(0.85*len(r['t'])):].mean()/1e6
        row.append((Ld, pat[:8], p))
    grid.append((U0, row))
    print(f"  U0={U0:.2f}: " + " | ".join(f"{a}:{b}({c:.2f})" for a,b,c in row))
results['S3'] = grid

# ---------- S4-LONG: defibrillation long-run, grid scan ----------
print("\nS4-LONG: defibrillation grid scan (T=6000, pulse at t=3000)")
best = None
scan = []
for dur in [30, 60, 120, 240, 480]:
    for mult in [0.0, 0.2, 0.5]:
        for kk in [1, 2, 4, 8]:
            r = simulate(N=24, T=6000, U0=3.8, sigma_u=0.0, gust_A=0.0, dt=0.5,
                         yaw_pulses=[(3000.0, 3000.0+dur, kk, mult)])
            p_after = r['P_tot'][int(4200/0.5):].mean()/1e6
            p_before = r['P_tot'][int(1500/0.5):int(2800/0.5)].mean()/1e6
            sf = spin_pattern(r, warmup_frac=0.75, window_frac=0.2)
            pat = "".join("1" if f > 0.5 else ("h" if f > 0.15 else "0") for f in sf)
            scan.append(dict(dur=dur, mult=mult, kk=kk, p_before=p_before, p_after=p_after,
                             gain=p_after-p_before, pat=pat))
            tag = ""
            if best is None or p_after > best[1]:
                best = ((dur, mult, kk), p_after, pat)
            if p_after-p_before > 0.02:
                tag = "  <-- gain"
            print(f"  dur={dur:4d} mult={mult:.1f} k={kk}: before={p_before:.3f} after={p_after:.3f} gain={p_after-p_before:+.3f}{tag}  {pat}")
results['S4'] = scan
results['S4_best'] = best
np.save(f'{OUT}/s4_scan.npy', np.array([(s['dur'], s['mult'], s['kk'], s['p_before'], s['p_after']) for s in scan]))

with open(f'{OUT}/results_v2.json', 'w') as f:
    json.dump(results, f, indent=1, default=str)
print("\nDONE. best defib:", best)
