"""
Third system for the universality paper: thermostatic heater chain.
A fluid flows at speed U through N heating zones. Each zone has a thermostat:
heater turns ON when local inflow temperature T_in < T_th (threshold), OFF above.
Heater output Q relaxes with time constant tau_h (slow recovery). Heat added by
upstream heaters is advected downstream with delay tau = x/U (inhibitory coupling:
upstream heating suppresses downstream firing) — exactly isomorphic to the
turbine row with flipped signs (u_in <-> T_in, u_cut <-> T_th, CT <-> Q).

Expected (from the universality theorem): discrete on/off pattern selection,
quantized total-heat steps vs spacing, local cold pulse -> regenerative
downstream trigger wave at speed U, NO self-sustained oscillation (feedforward).
"""
import numpy as np, sys, json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def simulate_heaters(N=24, T=4000.0, dt=0.5,
                     T0=97.0, T_th=100.0, dT_heat=25.0,
                     k=0.05, D=1.0, L_over_D=4.0,
                     tau_h=8.0,
                     cold_pulse_A=0.0, cold_pulse_w=0.8, cold_center_t=1500.0,
                     sigma_T=0.0, seed=5):
    """T0: base inflow temperature (deg C). T_th: thermostat threshold.
    Heater ON when T_in < T_th. Q_des = 1 when ON else 0, relaxation tau_h.
    Temperature deficit contribution of heater j at distance dx: dT_heat*Q_j/(1+k dx/D)^2.
    cold_pulse: travelling cold packet (like a gust) lowering T0 temporarily.
    """
    rng = np.random.default_rng(seed)
    L = L_over_D * D
    xs = np.arange(N) * L
    nsteps = int(T / dt)
    U = 1.0  # advective speed (nondimensional: units of D per time)
    U = L_over_D * D / 504.0  # keep advection delay comparable to turbine case: L=4D -> tau~?; simpler: U in m/s with D=126 scale
    U = 3.8  # m/s, D=126 m scale for direct comparability
    D = 126.0
    L = L_over_D * D
    xs = np.arange(N) * L

    Q = np.zeros(N)
    Q_abs = np.zeros((nsteps, N))
    Tin_abs = np.zeros((nsteps, N))
    events = []
    prev_on = np.zeros(N, bool)

    for step in range(nsteps):
        t = step * dt
        cold = cold_pulse_A * np.exp(-0.5 * ((xs - U * (t - cold_center_t)) / (cold_pulse_w * D)) ** 2)
        z = rng.normal(0, 1, N) if sigma_T > 0 else np.zeros(N)

        Tin = np.empty(N)
        for i in range(N):
            T = T0 + cold_pulse_A * np.exp(-0.5 * ((xs[i] - U * (t - cold_center_t)) / (cold_pulse_w * D)) ** 2) + sigma_T * z[i]
            for j in range(i):
                dx = xs[i] - xs[j]
                lag = int(round(dx / U / dt))
                if step - lag >= 0:
                    T += 0.25 * dT_heat * Q_abs[step - lag, j] / (1.0 + k * dx / D) ** 2
            Tin[i] = T

        Qdes = np.where(Tin < T_th, 1.0, 0.0)
        Q += (Qdes - Q) * (dt / tau_h)
        Q = np.clip(Q, 0, None)

        on = Tin < T_th
        for i in range(N):
            if prev_on[i] and not on[i]:
                events.append((t, i, 'off'))
            elif (not prev_on[i]) and on[i]:
                events.append((t, i, 'on'))
            prev_on[i] = on[i]

        Q_abs[step] = Q
        Tin_abs[step] = Tin

    return {'t': np.arange(nsteps) * dt, 'Q': Q_abs.T, 'Tin': Tin_abs.T, 'events': events, 'xs': xs, 'U': U, 'N': N}


OUT = '/home/user/research'
results = {}

# ---- 1) pattern selection & quantized heat steps (N=8 settled + N=24 phase diagram) ----
print("Heater chain: total heating vs L/D (N=8, settled, T0=T_th=100C, dT=25C)")
heatC = []
for Ld in [2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0]:
    r = simulate_heaters(N=8, T=6000, L_over_D=Ld)
    j = int(0.85 * len(r['t']))
    p = r['Q'][:, j:].mean() * 1.0  # fraction of max heating
    w = r['Q'][:, j:] > 0.05
    pat = "".join("1" if w[i].mean() > 0.5 else ("h" if w[i].mean() > 0.15 else "0") for i in range(8))
    heatC.append((Ld, p, pat))
    print(f"  L/D={Ld:4.1f}  heating={p:.3f}  pat={pat}")

# ---- 2) cold pulse -> trigger wave ----
print("\nCold pulse (A=-25C at zone 1, width 0.8D) -> heater-firing wave:")
rA = simulate_heaters(N=24, T=6000, cold_pulse_A=-25.0, cold_pulse_w=0.8, cold_center_t=1500.0)
rAb = simulate_heaters(N=24, T=6000, cold_pulse_A=0.0)
def first_after(r, t0, t1):
    f = {}
    for (tt, i, k) in sorted(r['events']):
        if k == 'on' and t0 <= tt <= t1 and i not in f:
            f[i] = tt
    return f
fA = first_after(rA, 1650, 5500)
fAb = first_after(rAb, 1650, 5500)
print("   zone  pulse   baseline")
for i in range(24):
    a = fA.get(i); b = fAb.get(i)
    print(f"   z{i+1:2d}  {a if a is None else round(a)}   {b if b is None else round(b)}")
xs_ = [i + 1 for i in sorted(fA) if i > 0][:10]
ys_ = [fA[i] for i in sorted(fA) if i > 0][:10]
if len(xs_) >= 4:
    coef = np.polyfit(xs_, ys_, 1)
    print(f"\n  wave leading edge slope={coef[0]:.1f} s/zone vs L/U={4*126/3.8:.1f} s -> speed={3.8*coef[0]/(4*126/3.8)*3.8 if False else 3.8*(4*126)/ (4*126) /1 * ( (4*126)/coef[0] )/3.8:.2f} U")
def cnt(r, t0, t1):
    return len([e for e in r['events'] if e[2] == 'on' and t0 <= e[0] <= t1])
print(f"  firing count [1650,3500]: pulse={cnt(rA, 1650, 3500)}, baseline={cnt(rAb, 1650, 3500)}")

# ---- 3) figure: heater raster + power steps side by side with turbine ----
tA = rA['t']
state = (rA['Tin'] < 100.0).astype(float)  # 1 = heater ON (T_th=100)
i0, i1 = int(1000/0.5), int(4000/0.5)
fig, ax = plt.subplots(figsize=(9.5, 6.5))
ax.imshow(state[:, i0:i1].T, aspect='auto', origin='lower', extent=[tA[i0], tA[i1], 0.5, 24.5],
          cmap=matplotlib.colors.ListedColormap(['#e8e8e8', '#c33d1f']), vmin=0, vmax=1)
ax.axvline(1500, color='navy', ls='--', lw=1.2)
ax.text(1515, 1.0, 'cold pulse at zone 1\n(gone by ~1560 s)', color='navy', fontsize=9)
ax.set_ylabel('heating zone (1 = upstream)')
ax.set_xlabel('time (s)')
ax.set_title('Thermostatic heater chain: a local cold pulse launches a regenerative\nheater-firing wave downstream (red = heater ON)', fontsize=12)
plt.tight_layout(); plt.savefig(f'{OUT}/fig6_heater_wave.png'); plt.close()
results['heatC'] = heatC
with open(f'{OUT}/results_v4.json', 'w') as f:
    json.dump(results, f, indent=1, default=str)
print("\nDONE third system.")
