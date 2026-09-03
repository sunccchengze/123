# Non-submission research record: forensic audit of interaction-structure claims in a static wake model

**Status:** **Withdrawn as a research-paper candidate. Do not submit to Wind Energy Science.**
**Author on the archived source:** Chengze Sun
**Correspondence:** 2253710052@stu.xjtu.edu.cn

## Abstract

This non-submission record supersedes an earlier draft that claimed a complement–substitute decomposition, a decoupling law, and a greedy certificate for yaw optimization. A falsification-oriented audit found that its mathematical scope and numerical evidence did not support those claims. The derivation assumed separable deficit kernels and recovery monotonicity, whereas the FLORIS Gauss–curl hybrid (GCH) model used for numerical illustrations includes yaw-added recovery and secondary steering. In a reproducible two-turbine, laterally offset GCH case, increasing positive upstream yaw from 0° to 5° lowers downstream power by 46.175 kW; recovery monotonicity is therefore not automatic for arbitrary geometry. At the former headline three-turbine point, the mixed finite difference changes from −0.215420 kW deg⁻² at a 5° step to +0.022315 kW deg⁻² at a 1° step, so the reported phase flip is not a verified local-Hessian result. Sampled derivatives also do not establish the box supremum needed by the former interaction-energy bound. This record preserves the falsifications and describes what a future study would need; it does not report a new physical law, controller, or submission-ready result.

## What was withdrawn

1. **Broad model-family claim.** The former analytic identity applied only to a separable, directed deficit map with an assumed local recovery-monotonicity condition. It did **not** contain FLORIS GCH as a special case. GCH includes yaw-added recovery and secondary steering, so downstream wake behavior can depend on upstream yaw states. The former statement that these effects change only magnitudes rather than sign structure was false.
2. **Arbitrary-pair formula.** The direct substitution term was orientation-specific but was written for arbitrary `i != j`, despite symmetry of mixed partials. Any repaired proposition must specify ordered pairs or include both directed terms. Analytic derivatives must use radians; historic finite differences were in kW deg⁻².
3. **Phase flip.** The central finite-difference sign at `(20°, 20°, 20°)` reverses under refinement:

   | step | diagnostic M₁₂ (kW deg⁻²) |
   |---:|---:|
   | 5° | −0.215420 |
   | 2.5° | −0.248412 |
   | 1° | +0.022315 |
   | 0.5° | +0.022367 |
   | 0.25° | +0.022381 |

   The old coarse result cannot be used as a local Hessian sign or phase boundary.
4. **Decoupling law and greedy certificate.** A finite selection of Hessian ratios cannot establish a law at optima. Sampling a few mixed partials cannot establish the yaw-box supremum required for a global greedy or clustering bound. All `theorem`, `law`, `guarantee`, `certificate`, and `provably safe` claims in the former P1 are withdrawn.
5. **Experimental claim.** A proposed wind-tunnel appendix was not an experiment or preregistration. It must not be described as either.

## Reproducible falsification evidence

`../ws_submodularity/p1_p2_forensic_audit.py` recreates the audit using FLORIS 4.6.6, NREL-5MW default inputs, 8 m s⁻¹, TI 0.06, and wind direction 270°. Its machine-readable output is `../ws_submodularity/expcache/p1_p2_forensic_audit.json`.

For two turbines at 5D streamwise spacing and −1D receiver offset, with downstream yaw fixed at zero:

| upstream yaw | downstream modeled power (kW) |
|---:|---:|
| 0° | 1651.808 |
| 1° | 1643.087 |
| 5° | 1605.633 |

The 0°→5° change is −46.175 kW. This is a model-scoped counterexample to automatic recovery monotonicity, not a universal claim about physical farms.

## Requirements before reopening the topic

A future study would need a correctly scoped theorem with declared angle units, pair ordering, differentiability, and exact sign assumptions; validated derivative calculations; predeclared cross-layout/model/inflow/yaw-sign tests; independent high-fidelity or experimental evidence for any physical claim; and a fresh multi-channel novelty audit. It must separate a conditional toy-model identity from behavior in GCH, LES, wind-tunnel, or field measurements.

The former prose received substantive generative-AI assistance. Under Copernicus policy reviewed on 2026-08-31, it cannot be submitted to WES as-is. Any future author must independently reconstruct, verify, and write a compliant manuscript.

See `../P1_P2_FORENSIC_STATUS.md` for the complete decision record and sources.
