# Theory-status record for interaction-structure experiments

**Current status (2026-08-31): no P1 theorem, law, certificate, or FLORIS-GCH interaction result is established by this repository.**

This file replaces an earlier statement that presented a complement–substitute decomposition, a phase boundary, a decoupling law, a greedy interaction-energy bound, and monotone comparative statics as established results. Those statements were withdrawn after the reproducible forensic audit in `p1_p2_forensic_audit.py`. See `../P1_P2_FORENSIC_STATUS.md` for the full reasoning and source links.

## What the former derivation actually assumed

A conditional symbolic exercise can start from a deliberately restricted map such as

\[
P(\gamma)=\sum_k p_k(\gamma_k)\,\phi(v_k(\gamma)),\qquad
v_k=1-\sum_{i\prec k}w_{ik}(\gamma_i),
\]

with a fixed directed acyclic graph, `C²` separable kernels, nonnegative normalized velocities, a declared angle unit, and explicitly checked sign conditions. Under those assumptions, one can calculate individual mixed derivatives. The calculation needs pair orientation, complete direct terms consistent with mixed-partial symmetry, and the exact curvature of `phi`; convexity alone does not establish every proposed sign under sum-of-squares superposition.

That is a conditional result about the declared mathematical map. It is **not** a result about FLORIS GCH unless a separate proof shows that all GCH dependencies lie in the map.

## Why the former FLORIS interpretation failed

FLORIS GCH includes yaw-added recovery and secondary steering. The latter allows upstream yaw to alter downstream effective yaw/wake behavior, breaking the old single-source-kernel interpretation. In the archived two-turbine, 5D-streamwise, `−1D`-offset GCH case, increasing upstream yaw from 0° to 5° changes downstream modeled power by −46.175 kW. Thus `−∂w_ij/∂γ_i ≥ 0` is not automatic for arbitrary geometry and a chosen positive yaw direction.

At the old three-turbine `(20°,20°,20°)` headline state, the central mixed-difference diagnostic is −0.215420 kW deg⁻² at `h=5°`, −0.248412 at `2.5°`, and +0.022315, +0.022367, +0.022381 at `1°`, `0.5°`, and `0.25°`. The coarse sign is not a validated local Hessian sign or phase transition.

## Claims that remain unavailable

- no proof that GCH satisfies the old separable deficit model;
- no universal recovery-monotonicity theorem;
- no validated complement/substitute sign rule, phase boundary, or AEP inheritance claim for the experiments;
- no law that optima are interactionally decoupled;
- no global bound on greedy gap, cluster loss, or Jacobi contraction from sampled derivatives;
- no global comparative-static or inverse-map theorem.

## Admission criteria for future theory

A future theorem would need a fully specified model and exact hypotheses, a complete independently checked proof, orientation/unit consistency, and a clearly defended scope. If it is to support a wake-model statement, it also needs model-specific derivative/dependency verification. If it is to support a global numerical bound, the relevant derivative envelope must be analytically or validation-numerically enclosed over the stated domain rather than sampled at a few points. Counterexamples, finite-difference refinements, and model warnings must be retained.
