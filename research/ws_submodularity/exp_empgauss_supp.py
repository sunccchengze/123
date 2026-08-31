import numpy as np, pathlib, floris, json
from floris import FlorisModel
pkg = pathlib.Path(floris.__file__).parent
D = 126.0
OUT = pathlib.Path("expcache")
MODEL = dict(velocity_model="empirical_gauss", deflection_model="empirical_gauss",
             turbulence_model="wake_induced_mixing", combination_model="sosfs")
PARAMS = dict(
 wake_velocity_parameters=dict(empirical_gauss=dict(wake_expansion_rates=[0.023,0.008], breakpoints_D=[10], sigma_0_D=0.28, smoothing_length_D=2.0, mixing_gain_velocity=2.0)),
 wake_deflection_parameters=dict(empirical_gauss=dict(horizontal_deflection_gain_D=2.0, vertical_deflection_gain_D=-1.0, mixing_gain_deflection=0.0, yaw_added_mixing_gain=0.0)),
 wake_turbulence_parameters=dict(wake_induced_mixing=dict(atmospheric_ti_gain=0.0)),
)
def make(xs, ys, wd=270.0, ti=0.06, ws=8.0):
    fm = FlorisModel(str(pkg/"default_inputs.yaml"))
    fm.set_param(["wake","model_strings"], MODEL)
    fm.set_param(["wake","enable_secondary_steering"], False)
    fm.set_param(["wake","enable_transverse_velocities"], False)
    for k, v in PARAMS.items():
        fm.set_param(["wake", k], v)
    fm.set(layout_x=xs, layout_y=ys)
    fm.set(wind_speeds=[ws], wind_directions=[wd], turbulence_intensities=[ti])
    return fm
def power(fm, yaw):
    fm.set(yaw_angles=np.asarray(yaw, dtype=float).reshape(1,-1)); fm.run()
    return float(fm.get_farm_power().sum()/1e3)
def Mij(fm, base, i, j, hh=5.0):
    b = np.array(base, float)
    def P(y): return power(fm, y)
    def d(k):
        v = np.zeros_like(b); v[k] = hh; return v
    if i == j: return (P(b+d(i))+P(b-d(i))-2*P(b))/hh**2
    return (P(b+d(i)+d(j))-P(b+d(i)-d(j))-P(b-d(i)+d(j))+P(b-d(i)-d(j)))/(4*hh**2)
def hessian(fm, base, hh=5.0):
    n=len(base); H=np.zeros((n,n))
    for i in range(n):
        H[i,i]=Mij(fm,base,i,i,hh)
        for j in range(i+1,n):
            H[i,j]=H[j,i]=Mij(fm,base,i,j,hh)
    return H
def od_ratio(H):
    off=H-np.diag(np.diag(H))
    return float(np.linalg.norm(off)/np.linalg.norm(np.diag(H)))
def djs(fm, y0, max_sweeps=6):
    y=np.array(y0,float); n=len(y); best=power(fm,y)
    for s in range(max_sweeps):
        ynew=y.copy()
        for i in range(n):
            ba,bp=ynew[i],power(fm,ynew)
            for a in np.arange(0,30.01,1.0):
                ynew[i]=a; p=power(fm,ynew)
                if p>bp+1e-12: bp,ba=p,a
            ynew[i]=ba
        pnew=power(fm,ynew)
        if abs(pnew-best)<1e-4: best=pnew; y=ynew; break
        best=pnew; y=ynew
    return y,best
res={}
# 1. power curve + cos^p fit
fm=make([0,630],[0,0])
gs=np.arange(0,31,1.0); P=np.array([power(fm,[g,0]) for g in gs])
mask=(gs>0)&(P>0); c=np.cos(np.deg2rad(gs[mask])); lr=np.log(P[mask]/P[0])
pfit=float(np.sum(np.log(c)*lr)/np.sum(np.log(c)**2))
r2=float(1-np.sum((lr-pfit*np.log(c))**2)/np.sum((lr-lr.mean())**2))
res["curve"]=dict(gs=gs.tolist(), P=P.tolist(), pfit=pfit, r2=r2)
print(f"empgauss curve: pfit={pfit:.3f} R2={r2:.5f}")
# 2. 3-chain flips
fm=make([0,630,1260],[0,0,0])
pts={"origin":[0,0,0],"mid":[20,20,20],"near_opt":[30,20,0]}
res["flip"]={k:[Mij(fm,pt,0,1),Mij(fm,pt,0,2),Mij(fm,pt,1,2)] for k,pt in pts.items()}
print("empgauss flips:", {k:[round(x,3) for x in v] for k,v in res["flip"].items()})
# 3. 3x3 sign matrices + djs
x9=[r*5*D for r in range(3) for c in range(3)]; y9=[(c-1)*3*D for r in range(3) for c in range(3)]
fm=make(x9,y9)
H0=hessian(fm,np.zeros(9)); yopt,popt=djs(fm,np.zeros(9)); Hstar=hessian(fm,yopt)
pbase=power(fm,np.zeros(9))
res["grid3x3"]=dict(H0=H0.tolist(),Hstar=Hstar.tolist(),yopt=yopt.tolist(),gain=(popt/pbase-1)*100,od0=od_ratio(H0),odst=od_ratio(Hstar))
print(f"empgauss 3x3: gain={res['grid3x3']['gain']:+.2f}% od {res['grid3x3']['od0']:.3f}->{res['grid3x3']['odst']:.3f} y*={np.round(yopt,1)}")
json.dump(res, open(OUT/"exp_empgauss_supp.json","w"))
print("SAVED", OUT/"exp_empgauss_supp.json")
