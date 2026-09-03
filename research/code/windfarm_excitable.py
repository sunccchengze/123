"""
Wind turbine row as an excitable medium — core 1-D model (v2, buffer bugs fixed).

Physics:
- N turbines in a straight row, spacing L, rotor diameter D.
- Freestream U0 with optional travelling Gaussian gust packet (speed U0) + OU turbulence.
- Jensen-type wake: deficit fraction at distance x = (CT/4)/(1+k x/D)^2;
  deficit velocity scales with U0. Advection delay tau = x/U0.
- Turbine: cut-in threshold u_cut. CT_des = 0 below cut-in, CT0 in MPPT band,
  pitch-regulated above rated. Rotor inertia: first-order lag tau_r on CT.
- Power: 0 below cut-in, P_rated*(u/u_rated)^3 below rated, P_rated above.

Event: 'up' = upward crossing of u_cut (restart/spin-up = "firing"),
       'down' = downward crossing (stop).
"""
import numpy as np


def simulate(N=24, T=1600.0, dt=0.5,
             U0=3.8, u_cut=3.5, u_rated=12.0,
             CT0=0.8, k=0.05, D=126.0, L_over_D=4.0,
             tau_r=8.0,
             gust_A=0.0, gust_w=None, gust_center_t=600.0,
             sigma_u=0.0, seed=7,
             yaw_pulses=None, P_rated=5.0e6,
             wake='jensen'):
    """wake: 'jensen' (top-hat, 1/(1+kx/D)^2) or 'gaussian'
    (Bastankhah-type single Gaussian, centerline deficit = CT*U0/4,
     width sigma(x) = 0.5*D*(1+2k x/D))."""
    """
    yaw_pulses: list of (t0, t1, k_turb, mult) — during [t0,t1) first k_turb
                turbines have CT_des multiplied by mult (defibrillation protocol).
    """
    rng = np.random.default_rng(seed)
    L = L_over_D * D
    xs = np.arange(N) * L
    if gust_w is None:
        gust_w = 3 * D
    nsteps = int(T / dt)

    def gust(t, x):
        return gust_A * np.exp(-0.5 * ((x - U0 * (t - gust_center_t)) / gust_w) ** 2)

    CT = np.zeros(N)
    CT_abs = np.zeros((nsteps, N))
    inflow_abs = np.zeros((nsteps, N))
    P_tot = np.zeros(nsteps)
    prev_below = np.ones(N, bool)
    events = []

    for step in range(nsteps):
        t = step * dt
        z = rng.normal(0, 1, N) if sigma_u > 0 else np.zeros(N)
        if sigma_u > 0 and N > 1:
            z = 0.7 * z + 0.3 * np.roll(z, 1)

        u_in = np.empty(N)
        for i in range(N):
            u = U0 + gust(t, xs[i]) + sigma_u * z[i]
            for j in range(i):
                dx = xs[i] - xs[j]
                lag = int(round(dx / U0 / dt))
                if step - lag >= 0:
                    cj = CT_abs[step - lag, j]
                    if wake == 'jensen':
                        u -= (cj / 4.0) * U0 / (1.0 + k * dx / D) ** 2
                    elif wake == 'gaussian':
                        # Bastankhah-Porte-Agel axisymmetric Gaussian wake, centerline
                        # deficit (momentum-conserving): dU_c(x) = (CT/4)U0*(sigma0/sigma)^2,
                        # sigma(x) = sigma0 + k x, sigma0 = D/2. Straight row -> downstream
                        # machines sit on the wake centerline.
                        sigma0 = 0.5 * D
                        sig = sigma0 + k * dx
                        u -= (cj / 4.0) * U0 * (sigma0 / sig) ** 2
                    else:  # hybrid: top-hat core up to 4D, gaussian beyond
                        if dx <= 4.0 * D:
                            u -= (cj / 4.0) * U0 / (1.0 + k * dx / D) ** 2
                        else:
                            sig = 0.5 * D * (1.0 + 2.0 * k * dx / D)
                            u -= (cj / 4.0) * U0 * np.exp(-0.5 * (dx / sig) ** 2)
            u_in[i] = u

        CT_des = np.empty(N)
        for i in range(N):
            u = u_in[i]
            if u < u_cut:
                ctd = 0.0
            elif u < u_rated:
                ctd = CT0
            else:
                ctd = CT0 * (u_rated / u) ** 2
            for (t0, t1, kk, mult) in (yaw_pulses or []):
                if t0 <= t < t1 and i < kk:
                    ctd *= mult
            CT_des[i] = ctd

        CT += (CT_des - CT) * (dt / tau_r)
        CT = np.clip(CT, 0.0, None)

        P = np.zeros(N)
        for i in range(N):
            u = max(u_in[i], 0.0)
            if u < u_cut:
                P[i] = 0.0
            elif u < u_rated:
                P[i] = P_rated * (u / u_rated) ** 3
            else:
                P[i] = P_rated
        P_tot[step] = P.sum()

        below = u_in < u_cut
        for i in range(N):
            if prev_below[i] and not below[i]:
                events.append((t, i, 'up'))
            elif (not prev_below[i]) and below[i]:
                events.append((t, i, 'down'))
            prev_below[i] = below[i]

        CT_abs[step] = CT
        inflow_abs[step] = u_in

    tt = np.arange(nsteps) * dt
    return {'t': tt, 'P_tot': P_tot, 'CT': CT_abs.T, 'inflow': inflow_abs.T,
            'events': events, 'xs': xs, 'U0': U0, 'u_cut': u_cut, 'N': N}


def spin_pattern(r, warmup_frac=0.5, window_frac=0.3):
    """Fraction of time each turbine is spinning (CT>0.05) in the final window."""
    nsteps = len(r['t'])
    w0 = int(nsteps * warmup_frac)
    w1 = int(nsteps * (warmup_frac + window_frac))
    return np.mean(r['CT'][:, w0:w1] > 0.05, axis=1)
