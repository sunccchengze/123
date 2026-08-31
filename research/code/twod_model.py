"""
2-D wind farm grid extension (F5 test).
M rows x N columns, wind along +x or -x (switchable in time).
Cluster-wake (top-hat) model: deficit from turbine (m',n') at along-wind distance x
(positive = upwind of target): (CT/4)*U0/(1+k x/D)^2 * overlap,
overlap = max(0, 1 - dy/w(x)), dy = lateral offset, w(x) = D (1 + k x/D)
(Frandsen-style overlapping top-hats).
F5a: fixed wind direction -> spatial pattern?
F5b1: fixed wind, two initial conditions -> same settled state? (predict YES:
      coupling graph is a DAG for fixed direction -> unique steady state)
F5b2: cycling wind direction (+x 400s / -x 400s ...) -> coupling graph acquires a
      cycle in time -> predict SUSTAINED dynamics (structural theorem converse).
"""
import numpy as np, json
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

def simulate_2d(M=4, N=8, Lr_D=3.0, Lc_D=4.0, T=6000.0, dt=0.5,
                U0=3.8, u_cut=3.5, u_rated=12.0, CT0=0.8, k=0.05, D=126.0,
                tau_r=8.0, P_rated=5.0e6, sigma_u=0.0, seed=7,
                dir_schedule=None, init_pattern=None):
    rng = np.random.default_rng(seed)
    Lr = Lr_D * D; Lc = Lc_D * D
    nsteps = int(T/dt)
    maxlag = int(np.ceil((N-1)*Lc/U0/dt)) + 3
    CT = np.zeros((M,N))
    if init_pattern is not None:
        CT = np.where(np.array(init_pattern) > 0.5, CT0, 0.0)
    CT_buf = np.zeros((maxlag, M, N))
    for s in range(maxlag):
        CT_buf[s] = CT
    P_tot = np.zeros(nsteps)
    spin = np.zeros((nsteps, M, N))
    for step in range(nsteps):
        t = step*dt
        d = 1
        if dir_schedule is not None:
            d = 1
            for (t0, dd) in dir_schedule:
                if t >= t0: d = dd
        z = rng.normal(0,1,(M,N)) if sigma_u>0 else np.zeros((M,N))
        u_in = np.empty((M,N))
        for m in range(M):
            for n in range(N):
                u = U0 + sigma_u*z[m,n]
                for mp in range(M):
                    for np_ in range(N):
                        if mp==m and np_==n: continue
                        dx = (n-np_)*Lc*d
                        if dx <= 0: continue
                        lag = int(round(dx/U0/dt))
                        if lag >= maxlag: continue
                        dy = abs(m-mp)*Lr
                        w = D*(1.0 + k*dx/D)
                        overlap = 1.0 - dy/w
                        if overlap <= 0: continue
                        cj = CT_buf[(step - lag) % maxlag][mp, np_]
                        u -= (cj/4.0)*U0/(1.0 + k*dx/D)**2 * overlap
                u_in[m,n] = max(u, 0.0)
        ctd = np.where(u_in < u_cut, 0.0, CT0)  # all-or-none, same as 1-D core model
        CT += (ctd-CT)*(dt/tau_r); CT = np.clip(CT,0,None)
        P = np.where(u_in<u_cut, 0.0, P_rated*np.minimum(1.0,(u_in/u_rated)**3))
        P_tot[step] = P.sum()
        spin[step] = (u_in>=u_cut).astype(float)
        CT_buf[step % maxlag] = CT
    return {'t': np.arange(nsteps)*dt, 'P_tot': P_tot, 'spin': spin, 'CT': CT,
            'M': M, 'N': N, 'U0': U0}

def pattern_str(r):
    f = np.mean(r['spin'][int(0.8*len(r['t'])):], axis=0)
    return "".join("".join("1" if v>0.5 else ("h" if v>0.15 else "0") for v in row) + "\n" for row in f)

def main():
    OUT='/home/user/research'
    res={}
    print("F5a: 2-D array 4x8, Lr=3D, Lc=4D, U0=3.8, fixed +x wind, T=6000 (settled)")
    rA = simulate_2d(M=4, N=8, Lc_D=4.0, Lr_D=3.0, T=6000)
    print(pattern_str(rA))
    res['F5a_pattern'] = pattern_str(rA)
    res['F5a_power'] = float(rA['P_tot'][int(0.85*len(rA['t'])):].mean()/1e6)

    print("\nF5b1: fixed wind, two different initial conditions -> same settled state?")
    rB1 = simulate_2d(M=4, N=8, Lc_D=4.0, Lr_D=3.0, T=6000)
    rB2 = simulate_2d(M=4, N=8, Lc_D=4.0, Lr_D=3.0, T=6000,
                      init_pattern=[[1,0,1,0,1,0,1,0]]*4)
    p1 = float(rB1['P_tot'][int(0.85*len(rB1['t'])):].mean()/1e6)
    p2 = float(rB2['P_tot'][int(0.85*len(rB2['t'])):].mean()/1e6)
    same = bool(abs(rB1['spin'][-200:,:,:].mean() - rB2['spin'][-200:,:,:].mean()) < 1e-3)
    print(f"  IC1 (all stopped): P={p1:.4f} MW\n  IC2 (seeded checker): P={p2:.4f} MW  -> same settled state: {same}")
    res['F5b1'] = dict(p1=p1, p2=p2, same=same)

    print("\nF5b2: cycling wind direction (+x 400s / -x 400s ...) -> sustained dynamics?")
    sched = [(t0, +1 if (int(t0)//400)%2==0 else -1) for t0 in range(0, 6000, 400)]
    rC = simulate_2d(M=4, N=8, Lc_D=4.0, Lr_D=3.0, T=6000, dir_schedule=sched)
    P = rC['P_tot']/1e6
    x = P[6000:] - P[6000:].mean()
    ac = np.correlate(x, x, 'full')[len(x)-1:] / (np.sum(x*x)+1e-12)
    pl = int(ac[1:].argmax())
    print(f"  t>3000: power range={P[6000:].max()-P[6000:].min():.3f} MW, autocorr peak lag={pl*0.5:.0f}s (value={ac[pl]:.2f})")
    res['F5b2'] = dict(range=float(P[6000:].max()-P[6000:].min()), ac_peak_lag=float(pl*0.5), ac_val=float(ac[pl]))
    np.save(f'{OUT}/f5b2_P.npy', P)
    np.save(f'{OUT}/f5a_spin.npy', rA['spin'])
    with open(f'{OUT}/results_2d.json','w') as f:
        json.dump(res, f, indent=1, default=str)
    print("\nF5 DONE")

if __name__ == '__main__':
    main()
