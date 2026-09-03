"""
Analytic 3-chain: serial turbines, deficit-additive Gaussian kernel, linear-superposition.
P = cos^p(g1) + cos^p(g2)(1-w12)^3 + cos^p(g3)(1-w13-w23)^3
M12 = d^2P/dg1 dg2 = C - S
  C = 6 cos^p(g3) (1-w13-w23) s13 s23        (complementarity via shared T3)
  S = 3 p sin(g2) cos^{p-1}(g2) (1-w12)^2 s12 (substitution via T2 power weight)
with s_ij = -dw_ij/dg_i > 0, w_ij = A(dx) * exp(-delta^2/(2 sigma^2)), delta = theta_c0 * dx
A(dx) = (D/(D+2k dx))^2 * (1 - sqrt(1 - Ct cos(g)))
theta_c0 = 0.3 g / cos(g) * (1 - sqrt(1 - Ct cos(g)))
"""
import numpy as np

D = 126.0; k = 0.055; Ct = 0.8; p = 1.88

def A(dx):
    return (D/(D+2*k*dx))**2 * (1-np.sqrt(1-Ct))

def theta_c0(g):
    g = np.asarray(g, dtype=float)
    eps = 1e-6
    return 0.3*g/np.cos(g+eps) * (1-np.sqrt(1-Ct*np.cos(g)))

def delta(dx, g):
    return theta_c0(g)*dx

def sigma(dx):
    return k*dx + D/np.sqrt(8)

def w(dx, g):
    return A(dx)*np.exp(-delta(dx,g)**2/(2*sigma(dx)**2))

def s(dx, g):
    """-dw/dg"""
    d_ = delta(dx,g); sg = sigma(dx)
    dA = A(dx) * (Ct*np.sin(g))/(2*np.sqrt(1-Ct*np.cos(g))) * -1  # d/dg of (1-sqrt(1-Ct cos g))
    # careful: A0(dx) includes (1-sqrt(1-Ct)) constant... redefine:
    return 0.0  # placeholder, computed numerically below

def s_num(dx, g, h=1e-3):
    return -(w(dx, g+h)-w(dx, g-h))/(2*h)

def M12(dx, g1, g2, g3):
    """3-chain mixed partial via the C-S formula."""
    w12 = w(dx,g1); w13 = w(2*dx,g1); w23 = w(dx,g2)
    s12 = s_num(dx,g1); s13 = s_num(2*dx,g1); s23 = s_num(dx,g2)
    C = 6*np.cos(g3)**p * (1-w13-w23) * s13*s23
    S = 3*p*np.sin(g2)*np.cos(g2)**(p-1) * (1-w12)**2 * s12
    return C-S, C, S

print("Analytic 3-chain: M12 = C - S  (gamma in degrees)")
for g2,g3 in [(20,20),(20,0),(0,0),(30,30),(30,0),(10,10),(15,15)]:
    m,c,ss = M12(5*D, np.deg2rad(20), np.deg2rad(g2), np.deg2rad(g3))
    print(f"  (g1=20, g2={g2}, g3={g3}): M12={m:+.4f} (C={c:.4f}, S={ss:.4f})")

# Phase boundary scan: where does M12=0 in (g2,g3) at g1=20, spacing 5D
print("\nPhase scan: sign(M12) over (g2,g3) grid, g1=20deg, 5D:")
for g3 in [0,10,20,30]:
    row = []
    for g2 in [5,10,15,20,25,30]:
        m,_,_ = M12(5*D, np.deg2rad(20), np.deg2rad(g2), np.deg2rad(g3))
        row.append("+" if m>1e-6 else ("-" if m<-1e-6 else "0"))
    print(f"  g3={g3:2d}: " + " ".join(f"{x}" for x in row))

# spacing dependence of the boundary: for g3=20, find g2 where M12=0 for s=4..8D
print("\nBoundary g2* (M12=0, g1=20, g3=20) vs spacing:")
for s in [3,4,5,6,7,8]:
    g2s = np.linspace(0.5, 35, 400)
    vals = [M12(s*D, np.deg2rad(20), np.deg2rad(g2), np.deg2rad(20))[0] for g2 in g2s]
    sign = np.sign(vals)
    cross = np.where(np.diff(sign)!=0)[0]
    if len(cross): print(f"  {s}D: boundary g2*~{g2s[cross[0]]:.1f} deg")
    else: print(f"  {s}D: no flip ({'all +' if vals[-1]>0 else 'all -'})")
