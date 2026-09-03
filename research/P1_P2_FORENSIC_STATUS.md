# P1/P2 forensic status — submission hold

**Date:** 2026-08-31
**Scope:** the former P1 interaction-structure draft and P2 coordinate-sweep/clustering draft
**Decision:** **neither draft is a Wind Energy Science submission candidate. Do not submit either one in its former form.**

This record supersedes the optimistic status statements in earlier project notes. It is a correction, not a claim that a new scientific result has been obtained.

## Why the hold was triggered

### 1. The P1 model-class claim is too broad

The old P1 proof assumes a directed, separable deficit map: each deficit kernel at receiver \(j\) depends only on the source turbine's own yaw, and it also assumes local recovery monotonicity \( -\partial w_{ij}/\partial\gamma_i\geq0 \). That is a conditional toy-model proposition, not a property of all FLORIS GCH runs.

In particular, GCH explicitly includes yaw-added recovery and **secondary steering**, under which the wake of a downstream turbine is altered by an upstream yaw state. King et al. (2021) describe that effective-yaw mechanism; it violates the simple single-source-kernel interpretation used in the old derivation. The old assertion that GCH was a special case, and that secondary steering changed only magnitudes rather than the sign structure, must be withdrawn. See [King et al. 2021](https://doi.org/10.5194/wes-6-701-2021) and the independent sensitivity discussion in [Gori et al. 2023](https://doi.org/10.5194/wes-8-1425-2023).

The displayed formula also used an orientation-specific direct-substitution term while declaring it for arbitrary \(i\ne j\). Since a mixed partial is symmetric, any repaired proposition must either order the pair explicitly or include both directed cases. All analytic yaw derivatives must also specify radians; the old numerical diagnostics were reported in kW deg\(^{-2}\).

### 2. A reproducible FLORIS counterexample defeats automatic recovery monotonicity

`ws_submodularity/p1_p2_forensic_audit.py` evaluates the historical FLORIS 4.6.6 setup with two turbines separated by 5D and a downstream receiver at lateral offset \(-1D\). Holding the downstream yaw at zero, increasing the upstream yaw from \(0^\circ\) to \(5^\circ\) lowers the downstream power from **1651.808 kW** to **1605.633 kW** (\(\Delta=-46.175\) kW).

This is not a claim about every physical wind farm. It is enough to show that one-sided yaw and arbitrary geometry do not automatically satisfy the recovery-monotonicity premise. The original universal/model-family wording was therefore invalid.

### 3. P1's headline finite-difference sign is not stable under refinement

At the former three-turbine-chain point \((20^\circ,20^\circ,20^\circ)\), the old P1 draft reported the \(h=5^\circ\) central mixed difference \(M_{12}=-0.215420\) kW deg\(^{-2}\) as a complement-to-substitute phase flip. The same reproducible calculation gives:

| central-difference step | reported diagnostic \(M_{12}\) (kW deg\(^{-2}\)) |
|---:|---:|
| \(5^\circ\) | \(-0.215420\) |
| \(2.5^\circ\) | \(-0.248412\) |
| \(1^\circ\) | \(+0.022315\) |
| \(0.5^\circ\) | \(+0.022367\) |
| \(0.25^\circ\) | \(+0.022381\) |

The coarse and refined values have opposite signs. A coarse finite difference cannot be presented as a verified local Hessian sign, a phase boundary, or empirical validation of the analytic decomposition at that state.

### 4. The old “certificate” was not a certificate

Theorem 2 required a supremum of mixed derivatives over a box. The experiment sampled the origin and four random points. Such samples can be a heuristic envelope but cannot certify a box supremum, a greedy gap, or a cluster-decoupling loss. The accompanying proof also did not supply a validated global derivative enclosure. Consequently all words such as *guarantee*, *certificate*, *brackets every gap*, and *provably safe* are withdrawn.

The “decoupling law” was a selected-set numerical pattern, not a theorem. It was based on the same coarse finite differences and a local reference optimizer. It cannot be used to infer general separability or a Jacobi contraction factor.

### 5. P2's implementation was not the method its text described

The function `exp_djs.py:djs` updates `ynew` in place: the line search for coordinate \(i+1\) sees the already changed coordinate \(i\). It is a cyclic Gauss–Seidel coordinate sweep, not a frozen-state, parallel Jacobi sweep. The audit reproduces both semantics:

| layout | old in-place first-sweep power (kW) | true synchronous-Jacobi first-sweep power (kW) |
|---|---:|---:|
| 3-turbine chain | 3295.691 | 3267.736 |
| 3×3 layout | 10042.514 | 9927.945 |

They happen to reach the same displayed integer-grid state after three sweeps in these two cases. That coincidence does **not** make the historical implementation parallel, prove convergence, or substantiate a critical-path speed claim. No multi-process execution was measured.

### 6. P2's novelty and attribution need correction

The former P2 misattributed a weighted-graph wake-decoupling method to Kuo et al. (2020), whose cited paper is a random-search yaw optimizer. Direct antecedents that must be handled before any new P2 research claim include:

- Shu, Song, and Hoon Joo (2022), *Decentralised optimisation for large offshore wind farms using a sparsified wake directed graph*, Applied Energy 306, 117986, [doi:10.1016/j.apenergy.2021.117986](https://doi.org/10.1016/j.apenergy.2021.117986): wake-digraph sparsification, clusters, and decentralised optimization;
- Li et al. (2025), *Weighted graph wake decoupling (WGWD) method for efficient optimal active yaw control of wake-effect mitigation in large wind farm*, International Journal of Green Energy 22, 2826–2841, [doi:10.1080/15435075.2025.2472291](https://doi.org/10.1080/15435075.2025.2472291): weighted graph decoupling and parallel subproblems;
- Tu et al. (2026), *Global optimization of wake steering for large-scale wind farms using generalized serial refinement method*, Applied Energy 406, 127259, [doi:10.1016/j.apenergy.2025.127259](https://doi.org/10.1016/j.apenergy.2025.127259): a current direct precedent in the serial-refinement optimizer space.

These results do not prove that every possible interaction-aware method lacks novelty. They do invalidate “first decentralised clustering,” “first optimizer with a mechanism,” and similar broad claims in the old P2 draft.

## Reproducibility record

The falsification-oriented evidence is retained rather than hidden:

- script: `ws_submodularity/p1_p2_forensic_audit.py`;
- machine-readable record: `ws_submodularity/expcache/p1_p2_forensic_audit.json`;
- environment: Python 3.11, `floris==4.6.6`, `numpy==2.4.6`, `scipy==1.17.1`, `matplotlib==3.10.9`, `Pillow==12.3.0`;
- record SHA-256 after the clean-environment run: `63d6cdfa6b8ce634aae266a2a2e1d881db10c50921898dbe335f9feae52b6850`.

## What would be required before reopening either topic

### P1

1. State and prove a mathematically correct result for a **clearly defined** model, including pair orientation, angle units, differentiability, and all conditions needed for the sign conclusion.
2. Do not call FLORIS GCH a special case unless every relevant dependence, including secondary steering and yaw-added recovery, is covered by the theorem.
3. Use analytic derivatives, automatic differentiation with verified regularity, or validated numerical bounds before making local-Hessian, phase, or global-envelope claims.
4. Test predeclared layouts, inflows, yaw signs, wake models, discretisation refinements, and uncertainty cases; include counterexamples rather than filtering them.
5. Obtain independent LES/wind-tunnel evidence if the paper makes physical rather than conditional-model claims. A prospective appendix is not a preregistration and cannot be described as one.

### P2

1. Decide whether the method is a genuine synchronous Jacobi method, a cyclic coordinate sweep, or a different algorithm; implement exactly that method and archive a tested parallel implementation.
2. Compare against proper contemporary antecedents and baselines under matched stopping tolerances, model-call budgets, hardware, inflow cases, yaw-rate/load constraints, and repeated timing runs.
3. Derive a valid guarantee with global/validated derivative bounds, or describe all interaction calculations as local numerical diagnostics rather than certificates.
4. Conduct a fresh multi-channel novelty audit only after a distinct, validated method exists.

## Publishing and authorship boundary

The old P1/P2 prose received substantive generative-AI assistance in this workflow. Copernicus policy reviewed on 2026-08-31 prohibits using generative AI to create manuscript text or scientific explanations. These records therefore cannot be submitted to WES as-is even after mathematical repair. The author must independently reconstruct, verify, and write any future submission and comply with the journal's current policy.
