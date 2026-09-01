"""Falsification-oriented audit of the P1/P2 research drafts.

This script deliberately records evidence *against* broad claims made in the
archived P1/P2 drafts.  It is not an optimizer benchmark and does not certify
any controller.  It checks three separate issues under the documented FLORIS
4.6.6 setup:

1. A positive yaw change can deepen a wake at a laterally offset receiver, so
   recovery monotonicity is not a property of arbitrary FLORIS layouts.
2. The reported P1 mixed partial at one key operating point changes sign as the
   finite-difference step is refined.  A coarse finite difference is therefore
   not evidence for a local Hessian sign there.
3. The previous ``DJS'' implementation updates `ynew` in place.  Its measured
   traces are cyclic Gauss--Seidel coordinate sweeps, not the synchronous
   Jacobi method described in P2.  A separate frozen-state implementation is
   included only to make the distinction reproducible.

Run from this directory after installing requirements.txt:
    python p1_p2_forensic_audit.py

It writes expcache/p1_p2_forensic_audit.json.  Numerical results are scoped to
one engineering wake model and must not be extrapolated to physical turbines.
"""

from __future__ import annotations

import json
import pathlib
from typing import Callable

import floris
import numpy as np
from floris import FlorisModel
from floris.logging_manager import configure_console_log

# This audit intentionally explores some configurations that expose weaknesses
# in the old claims.  Suppress FLORIS's repetitive warning stream so the JSON
# record and the substantive outcomes remain readable.
configure_console_log(False)

ROOT = pathlib.Path(__file__).resolve().parent
CACHE = ROOT / "expcache"
CACHE.mkdir(exist_ok=True)
PACKAGE = pathlib.Path(floris.__file__).parent
D_ROTOR = 126.0


def make(layout_x: list[float], layout_y: list[float]) -> FlorisModel:
    """Build the fixed FLORIS configuration used in the historical P1/P2 runs."""
    model = FlorisModel(str(PACKAGE / "default_inputs.yaml"))
    model.set(
        layout_x=layout_x,
        layout_y=layout_y,
        wind_speeds=[8.0],
        wind_directions=[270.0],
        turbulence_intensities=[0.06],
    )
    return model


def turbine_powers_kW(model: FlorisModel, yaw_deg: np.ndarray) -> np.ndarray:
    model.set(yaw_angles=np.asarray(yaw_deg, dtype=float).reshape(1, -1))
    model.run()
    return np.asarray(model.get_turbine_powers(), dtype=float).reshape(-1) / 1e3


def farm_power_kW(model: FlorisModel, yaw_deg: np.ndarray) -> float:
    return float(turbine_powers_kW(model, yaw_deg).sum())


def mixed_partial_kW_per_deg2(
    model: FlorisModel, base_deg: np.ndarray, i: int, j: int, step_deg: float
) -> float:
    """Central finite-difference diagnostic, not a derivative certificate."""
    base = np.asarray(base_deg, dtype=float)
    e_i = np.zeros_like(base)
    e_j = np.zeros_like(base)
    e_i[i] = step_deg
    e_j[j] = step_deg
    return float(
        (
            farm_power_kW(model, base + e_i + e_j)
            - farm_power_kW(model, base + e_i - e_j)
            - farm_power_kW(model, base - e_i + e_j)
            + farm_power_kW(model, base - e_i - e_j)
        )
        / (4.0 * step_deg**2)
    )


def coordinate_argmax(
    model: FlorisModel, state_deg: np.ndarray, coordinate: int
) -> float:
    """Return the best integer-degree coordinate value against a frozen state."""
    candidates = np.arange(0.0, 31.0, 1.0)
    values = []
    for candidate in candidates:
        trial = state_deg.copy()
        trial[coordinate] = candidate
        values.append(farm_power_kW(model, trial))
    return float(candidates[int(np.argmax(values))])


def legacy_in_place_sweep(model: FlorisModel, state_deg: np.ndarray) -> np.ndarray:
    """Reproduce exp_djs.py's historical in-place update semantics exactly."""
    updated = np.asarray(state_deg, dtype=float).copy()
    for coordinate in range(updated.size):
        updated[coordinate] = coordinate_argmax(model, updated, coordinate)
    return updated


def synchronous_jacobi_sweep(model: FlorisModel, state_deg: np.ndarray) -> np.ndarray:
    """A true Jacobi sweep: every one-dimensional search sees the same state."""
    frozen = np.asarray(state_deg, dtype=float).copy()
    updated = frozen.copy()
    for coordinate in range(frozen.size):
        updated[coordinate] = coordinate_argmax(model, frozen, coordinate)
    return updated


def trace_coordinate_method(
    layout_x: list[float], layout_y: list[float], update: Callable[[FlorisModel, np.ndarray], np.ndarray]
) -> dict:
    model = make(layout_x, layout_y)
    state = np.zeros(len(layout_x))
    powers = [farm_power_kW(model, state)]
    states = [state.tolist()]
    for _ in range(3):
        state = update(model, state)
        powers.append(farm_power_kW(model, state))
        states.append(state.tolist())
    return {
        "power_kW": powers,
        "increments_kW": [later - earlier for earlier, later in zip(powers, powers[1:])],
        "yaw_states_deg": states,
    }


# 1. Recovery monotonicity fails for an allowed positive yaw direction if a
# downstream rotor lies on the side into which the wake is displaced.
receiver_offset_D = -1.0
recovery_model = make([0.0, 5.0 * D_ROTOR], [0.0, receiver_offset_D * D_ROTOR])
recovery_angles = [0.0, 1.0, 5.0]
recovery_powers = {
    str(int(angle)): turbine_powers_kW(recovery_model, np.array([angle, 0.0])).tolist()
    for angle in recovery_angles
}
downstream_powers = {key: value[1] for key, value in recovery_powers.items()}

# 2. The h=5 degree diagnostic used in the old manuscript identifies the
# opposite sign from the refined local diagnostics at the cited (20,20,20)
# point.  Store all tested steps rather than selecting the convenient one.
fd_model = make([0.0, 5.0 * D_ROTOR, 10.0 * D_ROTOR], [0.0, 0.0, 0.0])
fd_base = np.array([20.0, 20.0, 20.0])
fd_steps = [5.0, 2.5, 1.0, 0.5, 0.25]
fd_values = {
    f"{step:g}": mixed_partial_kW_per_deg2(fd_model, fd_base, 0, 1, step)
    for step in fd_steps
}

# 3. Compare actual historical in-place semantics against a true synchronous
# implementation on two simple layouts.  Equality of a final state, if it
# occurs, does not make the historical code parallel or establish convergence.
layouts = {
    "three_turbine_chain": {
        "layout_x_m": [0.0, 5.0 * D_ROTOR, 10.0 * D_ROTOR],
        "layout_y_m": [0.0, 0.0, 0.0],
    },
    "three_by_three": {
        "layout_x_m": [row * 5.0 * D_ROTOR for row in range(3) for _ in range(3)],
        "layout_y_m": [(column - 1) * 3.0 * D_ROTOR for _ in range(3) for column in range(3)],
    },
}
coordinate_audit = {}
for name, layout in layouts.items():
    legacy = trace_coordinate_method(
        layout["layout_x_m"], layout["layout_y_m"], legacy_in_place_sweep
    )
    jacobi = trace_coordinate_method(
        layout["layout_x_m"], layout["layout_y_m"], synchronous_jacobi_sweep
    )
    coordinate_audit[name] = {
        "layout": layout,
        "historical_in_place_coordinate_sweep": legacy,
        "synchronous_jacobi_coordinate_sweep": jacobi,
        "final_states_equal_after_three_sweeps": bool(
            np.allclose(legacy["yaw_states_deg"][-1], jacobi["yaw_states_deg"][-1])
        ),
    }

record = {
    "schema_version": 1,
    "purpose": "Forensic falsification audit for archived P1/P2 claims; not a performance benchmark.",
    "environment": {
        "floris_version": floris.__version__,
        "wind_speed_m_per_s": 8.0,
        "wind_direction_deg": 270.0,
        "turbulence_intensity": 0.06,
        "turbine": "NREL-5MW from FLORIS default_inputs.yaml",
        "yaw_box_deg": [0.0, 30.0],
    },
    "recovery_monotonicity_counterexample": {
        "layout": {
            "two_turbines": True,
            "streamwise_spacing_D": 5.0,
            "receiver_lateral_offset_D": receiver_offset_D,
        },
        "upstream_yaw_deg": recovery_angles,
        "per_turbine_power_kW": recovery_powers,
        "downstream_power_kW": downstream_powers,
        "downstream_change_0_to_1deg_kW": downstream_powers["1"] - downstream_powers["0"],
        "downstream_change_0_to_5deg_kW": downstream_powers["5"] - downstream_powers["0"],
        "interpretation": (
            "At this laterally offset receiver, positive upstream yaw lowers downstream power. "
            "Thus recovery monotonicity is not automatic for arbitrary layouts or a one-sided yaw box."
        ),
    },
    "finite_difference_stability": {
        "layout": "three-turbine inline chain at 5D spacing",
        "base_yaw_deg": fd_base.tolist(),
        "pair_zero_based": [0, 1],
        "central_mixed_partial_kW_per_deg2_by_step_deg": fd_values,
        "coarse_step_sign": "positive" if fd_values["5"] > 0.0 else "negative",
        "one_degree_step_sign": "positive" if fd_values["1"] > 0.0 else "negative",
        "interpretation": (
            "The h=5 degree and h=1 degree diagnostics have opposite signs at this state. "
            "The coarse difference cannot be reported as a verified local Hessian sign or phase flip."
        ),
    },
    "coordinate_update_semantics": {
        "historical_source": "exp_djs.py:djs",
        "historical_semantics": (
            "Each coordinate search evaluates and mutates ynew after preceding coordinates have changed; "
            "this is an in-place cyclic (Gauss--Seidel) coordinate sweep, not a frozen-state Jacobi update."
        ),
        "comparison": coordinate_audit,
        "interpretation": (
            "The comparison is a code-semantics check only. It neither proves convergence nor supplies a "
            "parallel wall-clock result for either method."
        ),
    },
    "scope": (
        "All values are deterministic outputs of one FLORIS engineering-model configuration. They demonstrate "
        "that the broad P1/P2 assertions need withdrawal or a new validation programme; they do not establish "
        "a physical counterexample for real wind farms."
    ),
}

# Guard the two intentional audit findings so an accidental configuration drift
# cannot silently turn this file into a claim of support for the old drafts.
assert record["recovery_monotonicity_counterexample"]["downstream_change_0_to_5deg_kW"] < 0.0
assert record["finite_difference_stability"]["coarse_step_sign"] != record["finite_difference_stability"]["one_degree_step_sign"]

output = CACHE / "p1_p2_forensic_audit.json"
output.write_text(json.dumps(record, indent=2) + "\n")
print(f"Wrote {output.relative_to(ROOT)}")
print(
    "Recovery counterexample downstream ΔP(0→5°): "
    f"{record['recovery_monotonicity_counterexample']['downstream_change_0_to_5deg_kW']:.6f} kW"
)
print(
    "Mixed-partial h=5° / h=1°: "
    f"{fd_values['5']:+.6f} / {fd_values['1']:+.6f} kW deg^-2"
)
