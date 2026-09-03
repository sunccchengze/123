"""ARCHIVED figure-cache generator for withdrawn P1/P2 interpretations.

Do not treat its finite-grid phase/certificate-related output as evidence of a
theorem or a global bound. See ARCHIVE_NOTICE.md.
"""

import numpy as np, pathlib, floris
from floris import FlorisModel
from scipy.optimize import minimize
pkg = pathlib.Path(floris.__file__).parent
D=126.0
def make(layout_x, layout_y, wd=270.0, ti=0.06):
    fm = FlorisModel(str(pkg/"default_inputs.yaml"))
    fm.set(layout_x=layout_x, layout_y=layout_y)
    fm.set(wind_speeds=[8.0], wind_directions=[wd], turbulence_intensities=[ti])
    return fm
def power(fm, yaw):
    fm.set(yaw_angles=np.asarray(yaw, dtype=float).reshape(1,-1)); fm.run()
    return float(fm.get_farm_power().sum())
def mixed2(fm, base, i, j, hh=5.0):
    b=np.array(base,float)
    def P(y): return power(fm,y)
    def d(k):
        v=np.zeros_like(b); v[k]=hh; return v
    return (P(b+d(i)+d(j))-P(b+d(i))-P(b+d(j))+P(b))/hh**2

# --- 3x3 sign matrices (origin / optimum / wd300 origin) ---
xs=[]; ys=[]
for row in range(3):
    for col in range(3):
        xs.append(row*5*D); ys.append((col-1)*3*D)
def signmat(fm, base):
    n=len(base); M=np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            M[i,j]=mixed2(fm, base, i, j)
    return M
fm=make(xs,ys,wd=270.0)
M_origin = signmat(fm,[0]*9)
M_opt    = signmat(fm,[30,30,30,20,20,20,0,0,0])
fm300=make(xs,ys,wd=300.0)
M_300    = signmat(fm300,[0]*9)
np.savez("fig_cache_signmats.npz", origin=M_origin, opt=M_opt, wd300=M_300)
print("sign matrices cached")

# --- 3-chain phase map (robust region g<=25) ---
fm3=make([0,630,1260],[0,0,0])
def M12(g1,g2,g3,hh=5.0):
    b=np.array([g1,g2,g3],float); d1=np.array([hh,0,0]); d2=np.array([0,hh,0])
    P=lambda y: power(fm3,y)
    return (P(b+d1+d2)-P(b+d1-d2)-P(b-d1+d2)+P(b-d1-d2))/(4*hh**2)
gs=[0,5,10,15,20,25]
ph=np.zeros((len(gs),len(gs)))
for a,g2 in enumerate(gs):
    for b,g3 in enumerate(gs):
        ph[b,a]=M12(20,g2,g3)
np.savez("fig_cache_phasemap.npz", ph=ph, gs=gs)
print("phase map cached")
print(ph.round(1))

# --- 4x4 optimum ---
xs4=[]; ys4=[]
for row in range(4):
    for col in range(4):
        xs4.append(row*5*D); ys4.append((col-1.5)*3*D)
fm4=make(xs4,ys4)
n=16
def f4(yaw):
    fm4.set(yaw_angles=np.asarray(yaw,dtype=float).reshape(1,-1)); fm4.run()
    return -float(fm4.get_farm_power().sum())
best=None
for x0 in [np.zeros(n), np.full(n,20.0)]:
    res=minimize(f4,x0,bounds=[(0,30)]*n,method="SLSQP",options={"maxiter":400,"ftol":1e-9})
    if best is None or res.fun<best.fun: best=res
np.save("fig_cache_y4x4.npy", best.x)
print("4x4 ystar cached:", np.round(best.x.reshape(4,4),1))
