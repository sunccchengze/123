# 01 · Discovery and falsification log

## Status of the 2026-08-30 draft hypotheses

This record was corrected on 2026-08-31. It must not be read as support for the former P1/P2 claims. The full reproducible correction is in `research/P1_P2_FORENSIC_STATUS.md` and `research/ws_submodularity/p1_p2_forensic_audit.py`.

| former hypothesis | current status | reason |
|---|---|---|
| H1: yaw objective is submodular | rejected | A simple separable toy model has positive common-beneficiary terms; no general yaw submodularity was established. |
| H2: a C--S sign structure applies to FLORIS GCH | withdrawn | The derivation requires separable kernels and recovery monotonicity. GCH includes secondary steering and yaw-added recovery; a laterally offset FLORIS case violates automatic recovery monotonicity. |
| H3: robust numerical phase flip | withdrawn | At the former $(20,20,20)^\circ$ point, the sign is negative for the old 5-degree mixed difference and positive for refined 1-, 0.5-, and 0.25-degree diagnostics. |
| H4: decoupling law at optimum | withdrawn | A selected local finite-difference pattern is not a general law or contraction result. |
| H5: interaction-energy greedy certificate | withdrawn | A few sampled mixed partials cannot establish the required box supremum. |
| H6: general monotone comparative statics | withdrawn | The claimed global assumptions and validated model scope were not established. |
| H7: ray inverse guarantee | withdrawn as a paper claim | Finite samples do not prove continuous monotonicity or uniqueness; direct yaw/APC tracking precedents exist. See the P3 correction. |
| H8: DJS and signed clustering | withdrawn | The named DJS code is an in-place Gauss--Seidel sweep, not Jacobi; direct clustering/decoupling precedents exist. |

## Retained methodological lesson

A symbolic result can be useful only after its assumptions are tested against the model to which it is applied. For numerical interaction claims, test yaw direction and lateral offset, refine the finite-difference step, retain counterexamples and warnings, and inspect code semantics before labeling an update method. A lookup table of attractive results is not a theory, a certificate, or a submission.
