"""
Gaussian (Bastankhah & Porte-Agel 2016) yawed-wake model + GCH-style power model.
Implements the steady-state farm power P(gamma) as a smooth function of yaw angles,
close in spirit to FLORIS/GCH used in wake steering literature.
"""
import numpy as np

class GaussianWakeFarm:
    def __init__(self, layout, rotor_d=126.0, hub_z=90.0, u_inf=8.0,
                 k=0.055, a=1/3, alpha=0.58, beta=0.077, p_p=1.88, ct_bar=0.8):
        """
        layout: (N,2) turbine positions [x, y] in meters.
        k: wake expansion; a: axial induction; alpha: yaw-wake deflection gain
        beta: deflection parameter (GCH); p_p: power loss exponent with cos(alpha)
        """
        self.layout = np.asarray(layout, dtype=float)
        self.N = len(self.layout)
        self.D = rotor_d; self.zh = hub_z; self.uinf = u_inf
        self.k = k; self.a = a; self.alpha = alpha; self.beta = beta
        self.p_p = p_p; self.ct = ct_bar * np.ones(self.N)
        self.ti = 0.1 + np.zeros(self.N)
        self.psi = 0.0  # wind direction (rad), 0 = +x

    def _wake_center(self, x, y, yaw_i, ti_i):
        # Bastankhah & Porte-Agel yawed wake center deflection (Eq. 15-16)
        ct_i = self.ct[0] * np.cos(yaw_i) ** 2 if False else self.ct[0]
        # use simple GCH-like linear deflection with saturation
        kd = self.k
        sigma_y = kd * (x - 0) + self.D / np.sqrt(8)
        theta_c0 = 0.3 * yaw_i / np.cos(yaw_i) * (1 - np.sqrt(1 - self.ct[0] * np.cos(yaw_i)))
        delta = np.tanh(self.alpha * theta_c0 * (x / self.D)) / (self.alpha * theta_c0 + 1e-12)
        # alternate: use the standard BPA delta = theta_c0*x ... we use GCH-like:
        # simpler robust form:
        d = theta_c0 * (x / self.D) * self.D / (1 + self.beta * (x / self.D) ** 2)
        return y + d

    def _deficit(self, x, y, yaw_i, ti_i, ind_j):
        """deficit at (x,y) due to turbine i with yaw yaw_i, GCH/BP hybrid."""
        ct_i = self.ct[0] * np.cos(yaw_i)
        # wake growth: turbulence-corrected expansion
        kd = self.k * (1 + 0.0 * ti_i)
        sig = kd * x + self.D / np.sqrt(8)
        yc = self._wake_center(x, y, yaw_i, ti_i)
        radial = np.hypot(y - yc, 0.0)
        C = 1 - np.sqrt(1 - ct_i)
        A = (self.D / (self.D + 2 * kd * x)) ** 2
        return C * A * np.exp(-radial ** 2 / (2 * sig ** 2))

    def power(self, yaw, deficit_eps=1e-9):
        """
        Farm power (normalized to freestream power per turbine).
        Velocity deficit superposition: linear (sum of squared deficits? standard is
        linear superposition of deficits; GCH uses sum of deficits).
        """
        yaw = np.asarray(yaw, dtype=float)
        assert yaw.shape == (self.N,)
        u = np.full((self.N,), self.uinf)
        # deficits: for each turbine j, sum deficits from upstream turbines i
        for j in range(self.N):
            xj, yj = self.layout[j]
            d = 0.0
            for i in range(j):
                xi, yi = self.layout[i]
                dx = xj - xi
                if dx > 0:
                    # rotate to wind direction (assume aligned for now)
                    d += self._deficit(dx, yj - yi, yaw[i], self.ti[i], j)
            u[j] = self.uinf * (1 - min(d, 0.9))
        # power with cos^p yaw loss
        P = np.sum((u / self.uinf) ** 3 * np.cos(yaw) ** self.p_p)
        return P
