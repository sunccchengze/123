"""Reproduce the wake-steering inverse benchmark and archive its inputs.

The exact ray inversion and the five-node proxy baseline are deliberately
scored on the same nine targets.  The script writes the two JSON caches used by
Paper 3 and Figure C4, so the reported comparison cannot silently drift to a
different target set.

Environment: Python 3.11, FLORIS 4.6.6, SciPy.
"""
from __future__ import annotations

import json
from pathlib import Path

import floris
import numpy as np
from floris import FlorisModel
from scipy.optimize import brentq

ROOT = Path(__file__).parent
CACHE = ROOT / "expcache"
D_ROTOR = 126.0


def make(layout_x, layout_y, wd: float = 270.0, ti: float = 0.06) -> FlorisModel:
    package = Path(floris.__file__).parent
    fm = FlorisModel(str(package / "default_inputs.yaml"))
    fm.set(layout_x=layout_x, layout_y=layout_y)
    fm.set(wind_speeds=[8.0], wind_directions=[wd], turbulence_intensities=[ti])
    return fm


def power(fm: FlorisModel, yaw) -> float:
    fm.set(yaw_angles=np.asarray(yaw, dtype=float).reshape(1, -1))
    fm.run()
    return float(fm.get_farm_power().sum() / 1e3)


print("=== Ray response monotonicity ===")
ts = np.linspace(0.0, 1.0, 41)

# Two turbines: the 30-degree ray deliberately overshoots the 5D optimum.
fm2 = make([0.0, 5.0 * D_ROTOR], [0.0, 0.0])
p2 = np.asarray([power(fm2, [30.0 * t, 0.0]) for t in ts])
print(
    "2T ray (30t, 0): P(0)=%.2f P(30)=%.2f monotone-nondecreasing=%s"
    % (p2[0], p2[-1], bool(np.all(np.diff(p2) >= -1e-9)))
)

fm3 = make([0.0, 5.0 * D_ROTOR, 10.0 * D_ROTOR], [0.0, 0.0, 0.0])
p3 = np.asarray([power(fm3, [30.0 * t, 22.6 * t, 0.0]) for t in ts])
print(
    "3-chain ray [30,22.6,0]t: monotone=%s P_max=%.2f at t=%.3f"
    % (bool(np.all(np.diff(p3) >= -1e-9)), p3.max(), ts[p3.argmax()])
)

x9 = [row * 5.0 * D_ROTOR for row in range(3) for _ in range(3)]
y9 = [(column - 1) * 3.0 * D_ROTOR for _ in range(3) for column in range(3)]
fm9 = make(x9, y9)
profile = np.asarray([30.0, 30.0, 30.0, 20.0, 20.0, 20.0, 0.0, 0.0, 0.0])


def ray_power(t: float) -> float:
    return power(fm9, profile * t)

p9 = np.asarray([ray_power(t) for t in ts])
print(
    "3x3 ray [30,30,30,20,20,20,0,0,0]t: monotone=%s P_max=%.2f at t=%.3f"
    % (bool(np.all(np.diff(p9) >= -1e-9)), p9.max(), ts[p9.argmax()])
)

print()
print("=== Matched-target exact inverse and five-node proxy ===")
p0 = float(p9[0])
pmax = float(p9.max())
# This is the explicit nine-target protocol used in Table 2, Figure C3, and
# Figure C4: 5% through 99% of the observed attainable ray range.
targets = np.linspace(p0 + 0.05 * (pmax - p0), pmax - 0.01 * (pmax - p0), 9)


class Tracker:
    def __init__(self, target: float):
        self.target = target
        self.calls = 0

    def residual(self, t: float) -> float:
        self.calls += 1
        return ray_power(t) - self.target


exact_records = []
for target in targets:
    tracker = Tracker(float(target))
    t_star = brentq(tracker.residual, 0.0, 1.0, xtol=1e-6, rtol=1e-6)
    error = abs(ray_power(t_star) - target)
    exact_records.append(
        {
            "target": float(target),
            "tstar": float(t_star),
            "err": float(error),
            "calls": int(tracker.calls),
        }
    )
    print("  exact: P*=%8.2f kW -> t*=%.4f, error=%.2e kW, calls=%d" % (target, t_star, error, tracker.calls))

# The browser implementation uses a bilinear proxy.  Along one fixed profile
# ray its one-dimensional slice is the following five-node piecewise-linear
# interpolant, inverted by its first ascending interval (reverse search).
grid_t = np.asarray([0.0, 0.25, 0.5, 0.75, 1.0])
grid_power = np.asarray([ray_power(t) for t in grid_t])


def proxy_inverse(target: float) -> float:
    for ta, tb, pa, pb in zip(grid_t[:-1], grid_t[1:], grid_power[:-1], grid_power[1:]):
        if pa <= target <= pb:
            return float(ta + (target - pa) / (pb - pa) * (tb - ta))
    raise ValueError(f"target outside proxy range: {target}")


proxy_errors = []
for target in targets:
    t_proxy = proxy_inverse(float(target))
    proxy_errors.append(abs(ray_power(t_proxy) - target))

proxy_max_error = float(max(proxy_errors))
proxy_max_pct = float(proxy_max_error / pmax * 100.0)
print("  proxy: maximum error = %.4f kW (%.4f %% of Pmax) over the same nine targets" % (proxy_max_error, proxy_max_pct))

conditions = {
    "floris_version": floris.__version__,
    "wind_speed_m_per_s": 8.0,
    "wind_direction_deg": 270.0,
    "turbulence_intensity": 0.06,
    "layout": "3x3, 5D streamwise by 3D lateral",
    "profile_deg": profile.tolist(),
}
(CACHE / "table2_tracking.json").write_text(json.dumps(exact_records, indent=2))
(CACHE / "proxy_tracking_benchmark.json").write_text(
    json.dumps(
        {
            "conditions": conditions,
            "protocol": (
                "Five-node piecewise-linear slice of the browser bilinear proxy, "
                "inverted by first-ascending-interval reverse search; evaluated on "
                "the same nine targets as table2_tracking.json."
            ),
            "grid_t": grid_t.tolist(),
            "grid_power_kW": grid_power.tolist(),
            "targets_kW": targets.tolist(),
            "errors_kW": [float(error) for error in proxy_errors],
            "Pmax_kW": pmax,
            "max_error_kW": proxy_max_error,
            "max_error_pct_of_Pmax": proxy_max_pct,
        },
        indent=2,
    )
)
print("Wrote expcache/table2_tracking.json and expcache/proxy_tracking_benchmark.json")
