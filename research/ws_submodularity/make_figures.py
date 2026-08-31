import numpy as np, pathlib, floris, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from floris import FlorisModel
from scipy.optimize import minimize
pkg = pathlib.Path(floris.__file__).parent
D=126.0
def make(layout_x, layout_y, wd=270.0, ti=0.06):
    fm = FlorisModel(str(pkg/"default_inputs.yaml"))
    fm.set(layout_x=layout_x, layout_y=layout_y)
    fm.set(wind_speeds=[8.0], wind_directions=[wd], turbulence_intensities=[ti])
    return fm
def power(fm, yaw):  # kW
    fm.set(yaw_angles=np.asarray(yaw, dtype=float).reshape(1,-1)); fm.run()
    return float(fm.get_farm_power().sum()/1e3)
def Mij(fm, base, i, j, hh=5.0):  # central, kW/deg^2
    b=np.array(base,float)
    def P(y): return power(fm,y)
    def d(k):
        v=np.zeros_like(b); v[k]=hh; return v
    if i==j:
        return (P(b+d(i))+P(b-d(i))-2*P(b))/hh**2
    return (P(b+d(i)+d(j))-P(b+d(i)-d(j))-P(b-d(i)+d(j))+P(b-d(i)-d(j)))/(4*hh**2)

xs=[]; ys=[]
for row in range(3):
    for col in range(3):
        xs.append(row*5*D); ys.append((col-1)*3*D)

# ---- Fig 2: sign matrices (central diff) ----
def signmat(fm, base, hh=5.0):
    n=len(base); M=np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            M[i,j]=Mij(fm,base,i,j,hh)
    return M
fm=make(xs,ys,wd=270.0)
M0=signmat(fm,[0]*9); Mopt=signmat(fm,[30,30,30,20,20,20,0,0,0])
fm300=make(xs,ys,wd=300.0); M300=signmat(fm300,[0]*9)
fig,axes=plt.subplots(1,3,figsize=(15,4.6))
for ax,M,tt in [(axes[0],M0,"wd=270°, γ=0"),(axes[1],Mopt,"wd=270°, at optimum"),(axes[2],M300,"wd=300°, γ=0")]:
    im=ax.imshow(M,cmap="RdBu_r",vmin=-0.6,vmax=0.6)
    ax.set_title(tt, fontsize=11)
    ax.set_xticks(range(9)); ax.set_yticks(range(9))
    ax.set_xticklabels([f"T{i+1}" for i in range(9)], fontsize=7)
    ax.set_yticklabels([f"T{i+1}" for i in range(9)], fontsize=7)
    for i in range(9):
        for j in range(9):
            ax.text(j,i,f"{M[i,j]:+.2f}", ha="center", va="center", fontsize=6.2)
plt.colorbar(im, ax=axes, fraction=0.02, label=r"$\partial^2 P/\partial\gamma_i\partial\gamma_j$ (kW/deg$^2$)")
plt.suptitle("Interaction sign matrices of the 3×3 farm (FLORIS v4.6 GCH, central differences h=5°)")
plt.tight_layout(); plt.savefig("fig2_signmatrices.png", dpi=150); plt.close()
print("fig2 done")

# ---- Fig 1: 3-chain phase map (central) ----
fm3=make([0,630,1260],[0,0,0])
gs=[0,5,10,15,20,25]
ph=np.zeros((len(gs),len(gs)))
for a,g2 in enumerate(gs):
    for b,g3 in enumerate(gs):
        ph[b,a]=Mij(fm3,[20,g2,g3],0,1)
fig,ax=plt.subplots(figsize=(5.6,4.6))
im=ax.imshow(ph,cmap="RdBu_r",vmin=-0.7,vmax=0.7,origin="lower",extent=[-2.5,27.5,-2.5,27.5])
ax.set_xlabel(r"$\gamma_2$ (deg)"); ax.set_ylabel(r"$\gamma_3$ (deg)")
ax.set_title(r"sign($\partial^2P/\partial\gamma_1\partial\gamma_2$), $\gamma_1=20°$ — 3-turbine chain")
for a,g2 in enumerate(gs):
    for b,g3 in enumerate(gs):
        ax.text(g2,g3,f"{ph[b,a]:+.1f}",ha="center",va="center",fontsize=7)
ax.axhline(0,color="k",lw=0.3); ax.axvline(0,color="k",lw=0.3)
plt.colorbar(im,ax=ax,fraction=0.046,label="kW/deg$^2$")
plt.tight_layout(); plt.savefig("fig1_phasemap.png", dpi=150); plt.close()
print("fig1 done")

# ---- Fig 3: od/diag contrast ----
cases = ["3x3\nwd270","3x3\nwd300","3-chain","4x4","AEP\n12dir"]
opt=[0.023,0.022,0.030,0.055,0.068]; zero=[0.360,0.266,0.349,0.521,0.966]
x=np.arange(len(cases)); w=0.38
fig,ax=plt.subplots(figsize=(6.6,4.0))
ax.bar(x-w/2,opt,w,label="at optimum",color="#2c7fb8")
ax.bar(x+w/2,zero,w,label="at γ=0 (baseline)",color="#d95f02")
ax.set_yscale("log"); ax.set_xticks(x); ax.set_xticklabels(cases)
ax.set_ylabel(r"$\|M_{off}\|/\|\mathrm{diag}(M)\|$ (log)")
ax.set_title("Decoupling at the optimum (Law 1)")
ax.legend(); plt.tight_layout(); plt.savefig("fig3_decoupling.png", dpi=150); plt.close()
print("fig3 done")

# ---- Fig 4: TI comparative statics ----
fm2=make([0,630],[0,0])
tis=[0.03,0.05,0.07,0.09,0.12,0.15]; g1s=[]; gains=[]
for ti in tis:
    fm2.set(turbulence_intensities=[ti])
    def f(g):
        fm2.set(yaw_angles=np.asarray([g[0],0.0],dtype=float).reshape(1,-1)); fm2.run()
        return -power(fm2,[g[0],0.0])
    res=minimize(f,[20.0],bounds=[(0,35)],method="SLSQP")
    g=res.x[0]; p0=power(fm2,[0,0]); p1=power(fm2,[g,0])
    g1s.append(g); gains.append((p1/p0-1)*100)
fig,ax1=plt.subplots(figsize=(6.0,4.2))
ax1.plot(tis,g1s,"o-",color="#2c7fb8"); ax1.set_xlabel("turbulence intensity"); ax1.set_ylabel(r"optimal $\gamma_1^*$ (deg)",color="#2c7fb8")
ax1.tick_params(axis="y",labelcolor="#2c7fb8")
ax2=ax1.twinx(); ax2.plot(tis,gains,"s--",color="#d95f02"); ax2.set_ylabel("power gain (%)",color="#d95f02"); ax2.tick_params(axis="y",labelcolor="#d95f02")
ax1.set_title("Two turbines, 5D: monotone comparative statics in TI")
plt.tight_layout(); plt.savefig("fig4_ti_sweep.png", dpi=150); plt.close()
print("fig4 done")

# ---- Fig 5: 4x4 optimal profile ----
y4=np.load("fig_cache_y4x4.npy").reshape(4,4)
fig,ax=plt.subplots(figsize=(5.2,4.4))
im=ax.imshow(y4,cmap="YlGnBu",vmin=0,vmax=30)
ax.set_title("4×4 optimal yaw profile (SLSQP, +34.19%)")
ax.set_xticks(range(4)); ax.set_yticks(range(4))
ax.set_xticklabels([f"col{i+1}" for i in range(4)]); ax.set_yticklabels([f"row{i+1}" for i in range(4)])
for i in range(4):
    for j in range(4):
        ax.text(j,i,f"{y4[i,j]:.0f}",ha="center",va="center",fontsize=11)
plt.colorbar(im,ax=ax,fraction=0.046,label="yaw (deg)")
plt.tight_layout(); plt.savefig("fig5_y4x4.png", dpi=150); plt.close()
print("fig5 done")

# ---- Fig 6: greedy gaps (hardcoded from exp_robustness.py run, 12 layouts) ----
gaps=[0.148,0.001,0.001,0.205,0.007,0.545,0.002,0.033,-0.015,0.254,-0.009,-0.939]
fig,ax=plt.subplots(figsize=(6.6,3.4))
ax.bar(range(12),gaps,color="#7fcdbb")
ax.axhline(0,color="k",lw=0.6)
ax.set_xlabel("random 6-turbine layout (trial)"); ax.set_ylabel("SLSQP − greedy gap (%)")
ax.set_title("Upstream→downstream greedy vs multi-start SLSQP: gap distribution (mean +0.019%)")
plt.tight_layout(); plt.savefig("fig6_greedygaps.png", dpi=150); plt.close()
print("fig6 done")
print("ALL FIGURES DONE")
