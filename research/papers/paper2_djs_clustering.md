# Non-submission research record: forensic audit of coordinate-sweep and clustering claims for wake steering

**Status:** **Withdrawn as a research-paper candidate. Do not submit to Wind Energy Science.**
**Author on the archived source:** Chengze Sun
**Correspondence:** 2253710052@stu.xjtu.edu.cn

## Abstract

This non-submission record supersedes an earlier draft that presented Decoupled Jacobi Sweeps, interaction-matrix clustering, and an interaction-energy certificate for wake steering. A code-semantics and prior-art audit found that the proposed evidence did not support those claims. The function labeled DJS mutates its coordinate vector in place: every later one-dimensional search sees earlier updates. It is therefore a cyclic Gauss–Seidel coordinate sweep, not the frozen-state parallel Jacobi method described in the draft. In the archived FLORIS 4.6.6 examples, its first-sweep power differs from a true synchronous implementation by 27.955 kW for a three-turbine chain and 114.569 kW for a 3×3 layout, even though the two methods happen to share an integer-grid final state after three sweeps in those selected cases. This coincidence does not establish convergence, parallel execution, or a wall-clock advantage. The claimed certificate depended on an invalidated P1 derivative envelope: mixed partials sampled at a few states cannot bound the entire yaw box. Finally, wake-graph sparsification, decentralized clustering, and parallel subproblems have direct prior art. This record withdraws the old novelty and guarantee claims and lists the conditions required before a new algorithmic study can be assessed.

## Audit findings

### The method was not Jacobi

The implementation in `../ws_submodularity/exp_djs.py` changes `ynew` immediately after each coordinate search. Later searches are therefore conditioned on earlier changes, which makes it a cyclic Gauss–Seidel sweep. A true Jacobi method must freeze the pre-sweep vector while all coordinate subproblems are evaluated and then apply the selected values together.

The forensic script reproduces both semantics with the same historical FLORIS condition:

| layout | old in-place first sweep (kW) | synchronous Jacobi first sweep (kW) |
|---|---:|---:|
| 3-turbine chain | 3295.691 | 3267.736 |
| 3×3 layout | 10042.514 | 9927.945 |

Both reach the same displayed integer-grid state after three sweeps in these two selected examples. That does not demonstrate equivalence, convergence, a Jacobi contraction, parallel computation, or a speed result.

### The certificate and clustering guarantees were unsupported

The former P2 inherited a supposed global interaction-energy envelope from P1. P1 has been withdrawn: its central mixed difference reverses sign as the finite-difference step is refined, and its broad separable-kernel/GCH claim was false. Even independently, a few sampled mixed partials do not establish a supremum over the yaw box. A thresholded local matrix is only a local diagnostic; it cannot certify the coupling after yaw changes, under new inflows, or in a different wake model.

### The novelty and citation framing were wrong

The old draft incorrectly described Kuo et al. (2020) random search as a weighted-graph wake-decoupling method. Direct antecedents include:

- Shu, Song, and Hoon Joo (2022), **Decentralised optimisation for large offshore wind farms using a sparsified wake directed graph**, *Applied Energy* 306, 117986, doi:[10.1016/j.apenergy.2021.117986](https://doi.org/10.1016/j.apenergy.2021.117986);
- Li et al. (2025), **Weighted graph wake decoupling (WGWD) method for efficient optimal active yaw control of wake-effect mitigation in large wind farm**, *International Journal of Green Energy* 22, 2826–2841, doi:[10.1080/15435075.2025.2472291](https://doi.org/10.1080/15435075.2025.2472291);
- Tu et al. (2026), **Global optimization of wake steering for large-scale wind farms using generalized serial refinement method**, *Applied Energy* 406, 127259, doi:[10.1016/j.apenergy.2025.127259](https://doi.org/10.1016/j.apenergy.2025.127259).

These precedents invalidate the former broad `first decentralized clustering`, `first optimizer with a mechanism`, and similar claims. They do not rule out every future interaction-aware method, but any new proposal needs a fresh post-method novelty audit.

## Requirements before a new P2-like study

1. Specify and implement the actual update method, synchronization, stopping rule, and parallel execution; archive tests for those semantics.
2. Develop a contribution that remains distinct after comparison with graph sparsification, weighted-graph decoupling, serial-refinement, coordinate-search, and contemporary yaw optimizers.
3. Use matched solver budgets, tolerances, hardware, repeated timing runs, layouts, inflows, uncertainty, yaw-rate limits, and loads.
4. Derive a valid theorem with verified global hypotheses, or call interaction quantities local numerical diagnostics—not certificates.
5. Independently rewrite, verify, and audit the work before considering any journal submission.

The reproducible audit is `../ws_submodularity/p1_p2_forensic_audit.py`, which writes `../ws_submodularity/expcache/p1_p2_forensic_audit.json`. See `../P1_P2_FORENSIC_STATUS.md` for the full audit and publishing boundary.
