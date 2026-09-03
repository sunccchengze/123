"""ARCHIVED P2 exploratory script; not a Jacobi or performance benchmark.

The function historically called ``djs`` updates its state in place and is a
cyclic Gauss--Seidel coordinate sweep. Its outputs and timing fields are kept
only to reproduce the withdrawn analysis. For the explicit semantic comparison,
run ``p1_p2_forensic_audit.py`` and read ``ARCHIVE_NOTICE.md`` first.
"""

import numpy as np, pathlib, floris, time
from floris import FlorisModel
from scipy.optimize import minimize
pkg = pathlib.Path(floris.__file__).parent
D=126.0
def make(xs,ys,wd=270.0,ti=0.06):
    fm=FlorisModel(str(pkg/"default_inputs.yaml")); fm.set(layout_x=xs,layout_y=ys)
    fm.set(wind_speeds=[8.0],wind_directions=[wd],turbulence_intensities=[ti]); return fm
def power(fm,yaw):
    fm.set(yaw_angles=np.asarray(yaw,dtype=float).reshape(1,-1)); fm.run()
    return float(fm.get_farm_power().sum()/1e3)
def Mij(fm,base,i,j,hh=5.0):
    b=np.array(base,float)
    def P(y): return power(fm,y)
    def d(k):
        v=np.zeros_like(b); v[k]=hh; return v
    if i==j: return (P(b+d(i))+P(b-d(i))-2*P(b))/hh**2
    return (P(b+d(i)+d(j))-P(b+d(i)-d(j))-P(b-d(i)+d(j))+P(b-d(i)-d(j)))/(4*hh**2)

def djs(fm, y0, max_sweeps=8, tol=1e-4, verbose=False):
    """Historical misnamed routine: in-place cyclic Gauss--Seidel grid sweep.

    Retained under its original function name for traceability. It is not a
    frozen-state Jacobi update, does not execute coordinate searches in
    parallel, and should not be used to support convergence or timing claims.
    """
    y = np.array(y0, float); n=len(y)
    hist=[power(fm,y)]
    for s in range(max_sweeps):
        ynew = y.copy()
        for i in range(n):
            best_a, best_p = ynew[i], power(fm,ynew)
            for a in np.arange(0,30.01,1.0):
                ynew[i]=a; p=power(fm,ynew)
                if p>best_p+1e-12: best_p, best_a = p, a
            ynew[i]=best_a
        hist.append(power(fm,ynew))
        y=ynew
        if verbose: print(f"  sweep {s}: P={hist[-1]:.2f}")
        if abs(hist[-1]-hist[-2]) < tol: break
    return y, hist

def slsqp(fm, n):
    def f(yaw):
        fm.set(yaw_angles=np.asarray(yaw,dtype=float).reshape(1,-1)); fm.run()
        return -float(fm.get_farm_power().sum())
    best=None
    for x0 in [np.zeros(n), np.full(n,15.0), np.full(n,25.0)]:
        res=minimize(f,x0,bounds=[(0,30)]*n,method="SLSQP",options={"maxiter":300,"ftol":1e-9})
        if best is None or res.fun<best.fun: best=res
    return best.x

# --- Historical in-place coordinate-sweep reproduction (not a DJS/Jacobi benchmark) ---
xs=[]; ys=[]
for row in range(3):
    for col in range(3):
        xs.append(row*5*D); ys.append((col-1)*3*D)
xs4=[]; ys4=[]
for row in range(4):
    for col in range(4):
        xs4.append(row*5*D); ys4.append((col-1.5)*3*D)
cases=[("3-chain",[0,630,1260],[0,0,0]),("3x3",xs,ys),("4x4",xs4,ys4)]
rng=np.random.default_rng(3)
for k in range(6):
    cases.append((f"rand6_{k}",(rng.uniform(0,7,6)*D).tolist(),(rng.uniform(-2.5,2.5,6)*D).tolist()))
print("=== HISTORICAL IN-PLACE GAUSS--SEIDEL SWEEP vs SLSQP (NOT A FAIR BENCHMARK) ===")
rows=[]
for name,xs_,ys_ in cases:
    fm=make(xs_,ys_)
    n=len(xs_)
    p0=power(fm,np.zeros(n))
    t0=time.time(); y_opt=slsqp(fm,n); t_slsqp=time.time()-t0
    P_opt=power(fm,y_opt)
    t0=time.time(); y_djs,hist=djs(fm,np.zeros(n)); t_djs=time.time()-t0
    P_djs=power(fm,y_djs)
    gap=(P_opt-P_djs)/P_opt*100
    sweeps=len(hist)-1
    rows.append((name,(P_opt/p0-1)*100, gap, sweeps, t_djs, t_slsqp))
    print(f"{name:9s} opt_gain={rows[-1][1]:+6.2f}%  DJS_gap={gap:+.4f}%  sweeps={sweeps}  t_djs={t_djs:.1f}s t_slsqp={t_slsqp:.1f}s")
print()
print("=== Sign-matrix clustering on 5x5 (25 turbines, 5D x 3D) ===")
xs5=[]; ys5=[]
for row in range(5):
    for col in range(5):
        xs5.append(row*5*D); ys5.append((col-2)*3*D)
fm5=make(xs5,ys5); n=25
# sign matrix at origin
M=np.array([[Mij(fm5,[0]*n,i,j) for j in range(n)] for i in range(n)])
A=np.abs((M+M.T)/2); A[np.diag_indices(n)]=0
tau=0.05
W=(A>tau).astype(float)
# connected components
seen=set(); comps=[]
for i in range(n):
    if i in seen: continue
    stack=[i]; comp=[]; seen.add(i)
    while stack:
        v=stack.pop(); comp.append(v)
        for u in np.where(W[v]>0)[0]:
            if u not in seen:
                seen.add(u); stack.append(u)
    comps.append(sorted(comp))
print("clusters (tau=0.05):", comps)
# Historical sequential per-cluster SLSQP reproduction; it is not a measured parallel run.
def cluster_opt(clusters):
    y=np.zeros(n)
    def f(yaw):
        fm5.set(yaw_angles=np.asarray(yaw,dtype=float).reshape(1,-1)); fm5.run()
        return -float(fm5.get_farm_power().sum())
    for c in clusters:
        idx=np.array(c)
        def fc(yc):
            yy=y.copy(); yy[idx]=yc
            return f(yy)
        res=minimize(fc, y[idx], bounds=[(0,30)]*len(c), method="SLSQP", options={"maxiter":200})
        y[idx]=res.x
    return y
def centralized():
    def f(yaw):
        fm5.set(yaw_angles=np.asarray(yaw,dtype=float).reshape(1,-1)); fm5.run()
        return -float(fm5.get_farm_power().sum())
    return minimize(f,np.zeros(n),bounds=[(0,30)]*n,method="SLSQP",options={"maxiter":400,"ftol":1e-9}).x
p0=power(fm5,np.zeros(n))
t0=time.time(); y_c=centralized(); t_c=time.time()-t0
t0=time.time(); y_k=cluster_opt(comps); t_k=time.time()-t0
print(f"5x5: centralized gain={(power(fm5,y_c)/p0-1)*100:+.2f}% ({t_c:.0f}s) | clustered gain={(power(fm5,y_k)/p0-1)*100:+.2f}% ({t_k:.0f}s) | gap={(power(fm5,y_c)-power(fm5,y_k))/power(fm5,y_c)*100:+.3f}%")
