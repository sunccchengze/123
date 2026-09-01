# IDEATION — candidate-question register

**Updated:** 2026-09-01
**Rule:** an idea is not a contribution until it survives falsification. A literature search can bound what was searched; it cannot prove that the world contains no predecessor. Any substantive direct predecessor requires abandonment or a specific, defensible narrowing.

## Closed / held lines

| historical line | current status | reason |
|---|---|---|
| P1: yaw submodularity, complement–substitute structure, phase law, greedy certificate | **closed as formulated** | The separable/recovery-monotone premises do not automatically hold for FLORIS GCH; a lateral-offset counterexample violates automatic recovery monotonicity; the headline finite-difference sign reverses under refinement; sampled derivatives are not global bounds. |
| P2: “Decoupled Jacobi Sweeps,” signed clustering, certificate | **closed as formulated** | Historic code is cyclic in-place Gauss–Seidel, not synchronous Jacobi; certificate assumptions fail; direct graph-decoupling/cluster/refinement precedents exist. |
| P3: static ray inverse as a power-tracking novelty | **held / not a paper candidate** | Direct yaw/APC tracking precedents exist; finite ray samples do not prove continuous monotonicity or unique inversion; dynamic and load-aware baseline comparison is absent. |
| “A proposed appendix is a preregistration or experiment” | **prohibited** | A future plan is neither a completed experiment nor a preregistration. |

The evidence is retained in `P1_P2_FORENSIC_STATUS.md`, `SELF_AUDIT.md`, `NOVELTY_DOSSIER.md`, and `ws_submodularity/`.

## Background observations — not explanations

The source project contains static FLORIS outputs such as two-turbine yaw gains, a 3×3 yaw pattern, POD concentration, and PPO errors. These can motivate questions, but they are neither theory nor field evidence. In particular, “greedy performed well” does not imply submodularity, separability, or a certificate; a low-rank projection does not imply a low-rank mechanism; and an endpoint-bracketed scalar response does not establish a unique inverse.

## Conditional future candidates

These are questions to audit—not current claims or planned papers.

### Q1 — Validated local sensitivity atlas for explicitly scoped wake models

- **Question:** Can a defined model configuration admit a validated-numerics map of local yaw sensitivities and non-smooth/boundary regions, with all signs reported as local/model-scoped rather than physical laws?
- **Falsifiers:** discontinuities that defeat the proposed validation, no practically useful robust region, or direct prior work already providing the same certified atlas.
- **Minimum evidence:** exact configuration/dependency statement; interval or other validated derivative bounds; refinement convergence; negative controls; cross-model and uncertainty tests; closest-source comparison.
- **Not allowed:** calling local signs complements/substitutes, claiming a global optimizer guarantee, or transferring results to field behavior without further evidence.

### Q2 — Semantic and reproducibility audit of parallel wake-steering optimizers

- **Question:** Can published/open implementations be classified reproducibly by actual update semantics, synchronization, model-call budgets, and hardware behavior, and does that audit identify a meaningful reproducibility gap?
- **Falsifiers:** the audit merely repeats existing benchmark taxonomy or cannot access enough implementations for an honest comparison.
- **Minimum evidence:** author-approved code access or transparent reimplementations; tested Jacobi/Gauss–Seidel definitions; matched workloads; repeated timings; objective/unit checks; explicit scope and ethics review.
- **Novelty risk:** high. Existing decentralized, WGWD, serial-refinement, coordinate-search, and benchmark literature must be read before any claim.

### Q3 — Dynamic yaw/APC benchmark extension with controls and loads

- **Question:** In a defined simulation or experimental setting, is there a reproducible difference between a constrained static set-point scheduler and published dynamic APC approaches when actuator dynamics, yaw-rate limits, load proxies, and wind variation are matched?
- **Falsifiers:** no access to a credible dynamic/load model; baselines outperform or remove any claimed distinction; direct prior work already answers the exact protocol.
- **Minimum evidence:** preregistered protocol; dynamic inflow/actuator/load model; contemporary APC baselines; uncertainty/seed sweeps; no claim of field deployment without field evidence.
- **Novelty risk:** very high because direct work by Starke, Oudich, Sterle, and Tamaro already occupies yaw/APC power tracking.

### Q4 — Low-rank response observation as a reproducibility question

- **Question:** Under fixed yaw-grid/model/inflow protocols, how stable are POD spectra and subspace angles across layouts, model classes, and uncertainty? Can an observed low-rank approximation be separated from sampling or layout artifacts?
- **Falsifiers:** spectra/subspaces lack stability or matched prior work fully covers the exact analysis.
- **Minimum evidence:** out-of-sample error, subspace-angle statistics, cross-layout/model tests, grid-resolution sweep, code/data archive, and a novelty audit against reduced-order/HDMR/active-subspace literature.
- **Not allowed:** inferring a new physical mechanism merely from two dominant modes.

### Q5 — Mathematical serial-wake map only after independent symbolic audit

- **Question:** Does a fully specified idealized serial wake recursion have a nontrivial provable property that is mathematically distinct from known recurrence or optimization results?
- **Falsifiers:** algebraic reduction to known results, triviality, or a prior theorem.
- **Minimum evidence:** exact definitions, independent proof check, OEIS/literature search if a sequence or constant is central, and no unsupported claim of engineering relevance.

### C0 — Calibrated abstention for harmful dynamic wake steering

- **Status:** **closed as formulated; not a candidate.** The initial audit and final disposition are `novelty_audits/C0_ABSTENTION_RISK_CONTROL_NOVELTY_AUDIT_2026-09-01.md` and `novelty_audits/C0_DISPOSITION_2026-09-01.md`.
- **Reason for closure:** Becker & van Wingerden (2026) directly studies risk-averse, loss-avoiding wake-steering setpoints under uncertain time-varying wind direction; Xu et al. (2025/2026, preprint) directly supplies the generic selective-abstention + conformal-risk-control mechanism. Combining their labels is not a contribution.
- **Retained lesson only:** a future project would need a materially different, precisely stated scientific capability and a new hostile audit before it can become a candidate. No amount of static FLORIS testing, terminology change, or generic conformal wrapping reopens C0.

## Common protocol before any work begins

1. Record queries, dates, databases, source pages/DOIs, and closest predecessors.
2. State variable units, model dependencies, physical/model domain, assumptions, and explicit falsifiers.
3. Use a versioned script and cache raw outputs, including failures and warnings.
4. Test numerical refinement and deliberately adverse/negative-control cases.
5. Separate proof, conditional proposition, numerical screen, benchmark observation, and interpretation in every result table.
6. Update the audit records when a claim narrows, fails, or survives.
7. Do not draft a journal manuscript until the named author has independently verified and authored the science under the target venue’s current policy.
