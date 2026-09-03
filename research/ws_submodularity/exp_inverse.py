"""Reproduce and archive the wake-steering ray-inversion benchmark.

The exact ray inversion and five-node proxy baseline are deliberately scored on
the same nine targets.  In addition to their matched-target caches, the script
records a 41-point operational monotonicity screen and a denser 401-point
retrospective diagnostic.  A finite grid is evidence for the test case, not a
proof of continuous monotonicity or an inverse-map guarantee.

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


def trace_record(ts: np.ndarray, values: np.ndarray, profile_deg: np.ndarray) -> dict:
    """Return raw trace values plus only finite-grid monotonicity diagnostics."""
    increments = np.diff(values)
    maximum_index = int(np.argmax(values))
    return {
        "profile_deg": [float(value) for value in profile_deg],
        "sample_t": [float(value) for value in ts],
        "power_kW": [float(value) for value in values],
        "sample_count": int(len(ts)),
        "monotone_nondecreasing_at_samples": bool(np.all(increments >= -1e-9)),
        "minimum_adjacent_increment_kW": float(np.min(increments)),
        "maximum_power_kW": float(values[maximum_index]),
        "maximum_power_at_t": float(ts[maximum_index]),
    }


print("=== Ray-response monotonicity screens ===")
ts = np.linspace(0.0, 1.0, 41)

# Two turbines: the 30-degree ray deliberately overshoots the 5D optimum.
fm2 = make([0.0, 5.0 * D_ROTOR], [0.0, 0.0])
profile2 = np.asarray([30.0, 0.0])
p2 = np.asarray([power(fm2, profile2 * t) for t in ts])
trace2 = trace_record(ts, p2, profile2)
print(
    "2T ray [30,0]t: sampled-nondecreasing=%s; min adjacent increment=%.6f kW"
    % (trace2["monotone_nondecreasing_at_samples"], trace2["minimum_adjacent_increment_kW"])
)

fm3 = make([0.0, 5.0 * D_ROTOR, 10.0 * D_ROTOR], [0.0, 0.0, 0.0])
profile3 = np.asarray([30.0, 22.6, 0.0])
p3 = np.asarray([power(fm3, profile3 * t) for t in ts])
trace3 = trace_record(ts, p3, profile3)
print(
    "3-chain ray [30,22.6,0]t: sampled-nondecreasing=%s; Pmax=%.2f kW at t=%.3f"
    % (
        trace3["monotone_nondecreasing_at_samples"],
        trace3["maximum_power_kW"],
        trace3["maximum_power_at_t"],
    )
)

x9 = [row * 5.0 * D_ROTOR for row in range(3) for _ in range(3)]
y9 = [(column - 1) * 3.0 * D_ROTOR for _ in range(3) for column in range(3)]
fm9 = make(x9, y9)
profile9 = np.asarray([30.0, 30.0, 30.0, 20.0, 20.0, 20.0, 0.0, 0.0, 0.0])


def ray_power(t: float) -> float:
    return power(fm9, profile9 * t)


p9 = np.asarray([ray_power(t) for t in ts])
trace9 = trace_record(ts, p9, profile9)
print(
    "3x3 ray [30,30,30,20,20,20,0,0,0]t: sampled-nondecreasing=%s; Pmax=%.2f kW at t=%.3f"
    % (
        trace9["monotone_nondecreasing_at_samples"],
        trace9["maximum_power_kW"],
        trace9["maximum_power_at_t"],
    )
)

# This retrospective dense check strengthens the numerical diagnostic for the
# reported condition, but deliberately remains labelled as a finite-grid check.
dense_ts = np.linspace(0.0, 1.0, 401)
dense_p9 = np.asarray([ray_power(t) for t in dense_ts])
dense_trace9 = trace_record(dense_ts, dense_p9, profile9)
print(
    "3x3 retrospective 401-point screen: sampled-nondecreasing=%s; min adjacent increment=%.6f kW"
    % (
        dense_trace9["monotone_nondecreasing_at_samples"],
        dense_trace9["minimum_adjacent_increment_kW"],
    )
)

conditions = {
    "floris_version": floris.__version__,
    "wind_speed_m_per_s": 8.0,
    "wind_direction_deg": 270.0,
    "turbulence_intensity": 0.06,
    "layout": "3x3, 5D streamwise by 3D lateral",
    "profile_deg": profile9.tolist(),
}
(CACHE / "ray_monotonicity.json").write_text(
    json.dumps(
        {
            "schema_version": 1,
            "conditions": conditions,
            "operational_41_point_screen": {
                "interpretation": (
                    "Finite-grid empirical screen only; it does not establish continuous "
                    "monotonicity or a formal inverse-map guarantee."
                ),
                "traces": {
                    "two_turbine_30_0": trace2,
                    "three_turbine_30_22p6_0": trace3,
                    "three_by_three_30_30_30_20_20_20_0_0_0": trace9,
                },
            },
            "retrospective_401_point_three_by_three_screen": {
                "interpretation": (
                    "Denser finite-grid diagnostic for the one reported condition; still not "
                    "a continuous monotonicity proof."
                ),
                "trace": dense_trace9,
            },
        },
        indent=2,
    )
)

print()
print("=== Matched-target exact inverse and five-node proxy ===")
p0 = float(p9[0])
pmax = float(p9[-1])
# This explicit protocol is used by Table 2, Figure C3, and Figure C4: nine
# equally spaced interior targets, from 5% through 99% of the observed ray gain.
target_lower_fraction = 0.05
target_upper_fraction = 0.99
targets = np.linspace(
    p0 + target_lower_fraction * (pmax - p0),
    p0 + target_upper_fraction * (pmax - p0),
    9,
)


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
    print(
        "  exact: P*=%8.2f kW -> t*=%.4f, error=%.2e kW, calls=%d"
        % (target, t_star, error, tracker.calls)
    )

# The browser implementation uses a bilinear proxy. Along one fixed profile ray
# its one-dimensional slice is the following five-node piecewise-linear
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
print(
    "  proxy: maximum error = %.4f kW (%.4f %% of Pmax) over the same nine targets"
    % (proxy_max_error, proxy_max_pct)
)

(CACHE / "table2_tracking.json").write_text(json.dumps(exact_records, indent=2))
(CACHE / "proxy_tracking_benchmark.json").write_text(
    json.dumps(
        {
            "conditions": conditions,
            "target_protocol": {
                "count": 9,
                "lower_fraction_of_observed_ray_gain": target_lower_fraction,
                "upper_fraction_of_observed_ray_gain": target_upper_fraction,
                "description": "Nine equally spaced interior targets from 5% through 99% of the observed ray gain.",
            },
            "protocol": (
                "Five-node piecewise-linear slice of the browser bilinear proxy, "
                "inverted by first-ascending-interval reverse search; evaluated on "
                "the same nine targets as table2_tracking.json."
            ),
            "grid_t": grid_t.tolist(),
            "grid_power_kW": grid_power.tolist(),
            "targets_kW": targets.tolist(),
            "errors_kW": [float(error) for error in proxy_errors],
            "P0_kW": p0,
            "Pmax_kW": pmax,
            "max_error_kW": proxy_max_error,
            "max_error_pct_of_Pmax": proxy_max_pct,
        },
        indent=2,
    )
)
print(
    "Wrote expcache/ray_monotonicity.json, table2_tracking.json, and "
    "proxy_tracking_benchmark.json"
)
