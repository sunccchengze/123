# Wake-steering research package — current status

**Session:** Arena `01a053b1-123`
**Updated:** 2026-09-01
**Submission status:** **none of the three archived records is currently a Wind Energy Science submission candidate. Do not submit them as-is.**

This repository retains reproducible drafts, code, caches, figures, source checks, and negative findings. It is not evidence that a publishable theorem, controller, or field result has been established. The newest forensic audit overturns the former P1/P2 paper claims; P3 was already downgraded after a separate novelty and evidence-level audit.

> **Author-information reminder:** archived source fields use `Chengze Sun` and `2253710052@stu.xjtu.edu.cn`. The author must independently confirm any future legal/preferred name, affiliation, contact information, scientific result, and journal-policy compliance.

## Record-by-record status

| record | present status | retained reproducible evidence | why it is not a paper candidate |
|---|---|---|---|
| **P1 — interaction structure** | **Non-submission forensic record** | `ws_submodularity/p1_p2_forensic_audit.py` and `expcache/p1_p2_forensic_audit.json` | The claimed GCH model-class inclusion was false; automatic recovery monotonicity fails in a laterally offset GCH test; the former headline mixed-difference sign reverses under step refinement; sampled values cannot yield a global certificate. |
| **P2 — coordinate sweeps and clustering** | **Non-submission forensic record** | same forensic script/cache plus historic code | The function called DJS is an in-place Gauss–Seidel sweep, not a parallel Jacobi implementation; P1 cannot support the claimed bounds; clustering/decoupling has direct prior art and one citation was misattributed. |
| **P3 — static ray inversion** | **Narrow reproducible benchmark record** | `exp_inverse.py`, `ray_monotonicity.json`, `table2_tracking.json`, and `proxy_tracking_benchmark.json` | Direct yaw/APC tracking precedents exist; finite 41/401-point screens are not continuous-monotonicity or unique-inverse proofs; no dynamic/controller/load comparison exists. |

`P1_P2_FORENSIC_STATUS.md` is the authoritative P1/P2 decision record. It preserves exact counterexamples, code-semantics results, sources, and re-entry requirements. `CLAIM_LEDGER_2026-08-31.md` maps each active statement to its evidence class and adjacent sources. P3's separate correction is preserved in `NOVELTY_DOSSIER.md` and `SELF_AUDIT.md`.

The independent 2026-09-01 impact assessment is in `RESEARCH_IMPACT_ASSESSMENT_2026-09-01.md`. It confirms a present submission **no-go**. Its initial C0 question was closed after direct prior-art review; the corresponding source log and final disposition are `novelty_audits/C0_ABSTENTION_RISK_CONTROL_NOVELTY_AUDIT_2026-09-01.md` and `novelty_audits/C0_DISPOSITION_2026-09-01.md`. Neither reinstates any archived record.

## Key negative findings that must not be erased

1. **P1 recovery premise:** in the audited 5D, laterally offset two-turbine FLORIS GCH case, downstream modeled power declines from **1651.808 kW** at 0° upstream yaw to **1605.633 kW** at 5° (a **−46.175 kW** change). Positive yaw does not automatically improve a receiver in arbitrary geometry.
2. **P1 finite-difference stability:** at the former three-turbine `(20°, 20°, 20°)` point, the mixed diagnostic is **−0.215420 kW deg⁻²** at `h=5°`, but **+0.022315 kW deg⁻²** at `h=1°`, converging near **+0.022381 kW deg⁻²** by `h=0.25°`. The old reported phase flip is withdrawn.
3. **P2 semantics:** the historic in-place sweep yields 3295.691 kW versus 3267.736 kW for an actual synchronous-Jacobi first sweep on the three-turbine case, and 10042.514 versus 9927.945 kW on the 3×3 case. A shared final state in those selected runs does not make the old implementation parallel or prove a rate.
4. **P3 evidence level:** the fixed 3×3 ray is sampled nondecreasing at 41 and 401 points only. On nine fixed interior targets (5–99% of observed endpoint gain), Brent uses 7–11 evaluations and has a maximum model residual of **0.00078209 kW**; a five-node proxy slice has **51.89370 kW** maximum residual on those same targets. This is an implementation-specific matched-target residual comparison—not a matched online budget, a control result, or a proof.

## Reproducibility commands

The pinned dependencies are in `ws_submodularity/requirements.txt`. A clean-environment run on 2026-08-31 installed FLORIS 4.6.6, NumPy 2.4.6, SciPy 1.17.1, Matplotlib 3.10.9, and Pillow 12.3.0.

```bash
cd research
python3 -m venv .venv
.venv/bin/python -m pip install -r ws_submodularity/requirements.txt
cd ws_submodularity
../.venv/bin/python p1_p2_forensic_audit.py  # intentionally reproduces P1/P2 failure findings
../.venv/bin/python exp_inverse.py            # P3 finite-grid screens + matched-target records
../.venv/bin/python make_figures2.py          # historic/reproducibility figures; not a claim of validity
```

The audited P1/P2 JSON record generated in a clean environment has SHA-256:

```text
63d6cdfa6b8ce634aae266a2a2e1d881db10c50921898dbe335f9feae52b6850
```

## What a future research programme would need

- **For P1:** a mathematically correct, explicitly scoped theorem; verified derivatives or validated numerical enclosures; predeclared cross-layout/inflow/yaw-sign/model tests; and independent LES/wind-tunnel evidence before any physical claim.
- **For P2:** a correctly implemented and tested update algorithm; matched and repeated performance experiments against current graph-decoupling and serial-refinement work; and a valid global proof or an honestly local numerical result.
- **For P3:** an auditable continuous-monotonicity/uniqueness result for a stated model domain; preregistered cross-condition tests; and fair comparison with dynamic APC baselines including actuators and loads.
- **For every future submission:** a fresh multi-channel novelty audit, an immutable public code/data archive with DOI, official-template compilation, author-owned verification and rewrite, and journal-policy compliance.

## Publishing and authorship boundary

Copernicus's AI policy reviewed on 2026-08-31 permits limited grammar/spelling/readability assistance but prohibits using generative AI to create manuscript text or scientific explanations. The archived drafts received substantive generative-AI assistance. They cannot be submitted to WES unchanged or made compliant through a false declaration. The author must independently reconstruct, verify, and write any future manuscript, or select a venue whose policy permits a transparent disclosure.

The local `article + copernicus_local.sty` PDFs are regression artifacts only; they are not a successful compilation with the official Copernicus class. A GitHub branch is also not a citable permanent archive.

## Important paths

| path | purpose |
|---|---|
| `P1_P2_FORENSIC_STATUS.md` | authoritative P1/P2 hold decision, evidence, sources, and re-entry gates |
| `papers/paper1_interaction_structure.tex` | P1 non-submission forensic source |
| `papers/paper2_djs_clustering.tex` | P2 non-submission forensic source |
| `papers/paper3_power_tracking_inverse.tex` | P3 narrow static benchmark source; not an independent submission candidate |
| `papers/refs.bib` | shared, DOI-checked bibliography |
| `ws_submodularity/p1_p2_forensic_audit.py` | reproducible counterexample, finite-difference, and code-semantics audit |
| `ws_submodularity/expcache/` | machine-readable reproduction caches, including negative findings |
| `NOVELTY_DOSSIER.md`, `SELF_AUDIT.md` | discovery, correction, and evidence-boundary record |
| `RESEARCH_IMPACT_ASSESSMENT_2026-09-01.md` | independent impact/submission no-go review and gated future-research direction |
| `novelty_audits/C0_ABSTENTION_RISK_CONTROL_NOVELTY_AUDIT_2026-09-01.md` | unresolved C0 candidate's source log, direct precedents, and kill criteria |
| `skills/doctoral-research-gatekeeper/SKILL.md` | transparent local supervisor-style gate; not an external human/advisor claim |
