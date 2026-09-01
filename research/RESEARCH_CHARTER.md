# RESEARCH_CHARTER — research-quality and integrity charter

**Updated:** 2026-09-01
**Working branch:** `arena/01a053b1-123`
**Research owner and final scientific decision-maker:** Chengze Sun

## Current reality

The original goal was to find a research point with no substantive predecessor and turn it into several top-journal papers. The stricter interpretation is now explicit: no finite web search can prove a global absence of literature, and a phrase-level zero hit is not novelty. A candidate survives only if it remains meaningfully distinct after direct source reading, theory audit, implementation audit, and appropriate experiment. A substantive predecessor requires the claim to be abandoned or narrowed to a demonstrably distinct subproblem.

As of this update, P1, P2, and P3 are **not** WES submission candidates. P1/P2 were withdrawn by the forensic audit in `P1_P2_FORENSIC_STATUS.md`; P3 was downgraded in `SELF_AUDIT.md` audit point #8 and `NOVELTY_DOSSIER.md`. The provisional C0 dynamic risk/abstention idea was also closed after direct prior-art review in `novelty_audits/C0_DISPOSITION_2026-09-01.md`. Negative findings remain part of the research record.

## Non-negotiable standards

1. **Novelty is a falsifiable hypothesis.** Before a `first`, `new`, or `unexplored` statement, search web and scholarly indices in relevant languages, DOI metadata, repositories/code if relevant, and close disciplinary vocabulary. Preserve query/date/result/source records. Report only bounded statements such as “no direct predecessor was located in the stated audit,” never a universal absence claim.
2. **Evidence precedes narrative.** Every numerical, theoretical, algorithmic, or experimental statement needs a versioned source, reproducible protocol, inputs, units, outputs, and a description of its evidence level. Retain failed runs, counterexamples, warnings, and changes of mind.
3. **Assumptions are results to test.** State model domain, variable units, ordering conventions, differentiability, dependencies, and boundary conditions before deriving formulas. Do not transfer a toy-model theorem to FLORIS, LES, a wind tunnel, or a field farm without a separate scope argument.
4. **Finite computation has finite reach.** Grids and finite differences are screens, not proofs of continuous monotonicity, uniqueness, global extrema, derivative bounds, convergence, or certificates. Run step-refinement, model-boundary, and negative-control checks; use analytic proof or validated numerics for global claims.
5. **Algorithm names must match code.** Inspect update semantics, synchronization, objective units, stopping rules, hardware, and actual parallel execution. Fair performance claims require matched budgets/tolerances/constraints, repeated timings, meaningful baselines, and scope limits.
6. **Use skills as audits, not rhetorical polish.** Consult relevant research and clarity skills before work. A humanization/clarity check may identify jargon, overclaiming, and readability problems; it may not hide AI authorship or turn an unsupported result into a manuscript.
7. **Publishing integrity.** The author must independently verify, reconstruct, and write any future manuscript. The Copernicus policy reviewed on 2026-08-31 prohibits generative AI from creating manuscript text or scientific explanations. AI-assisted archival records in this repository must not be submitted as WES prose. No false disclosure, false preregistration, false field validation, or false permanent-archive claim is acceptable.
8. **Milestones are auditable.** Update `SELF_AUDIT.md`, `NOVELTY_DOSSIER.md`, `SUMMARY.md`, and any candidate-specific audit when a material conclusion changes. Commit each coherent completed change on the session branch. Do not push while GitHub authorization is unavailable or the user has asked not to push.

## Required research gate for a future candidate

1. Define a testable question, explicit falsifiers, model/physical scope, and decision relevance.
2. Perform and archive a multi-channel novelty audit, including direct reading of closest sources.
3. Construct a minimal formal model; identify assumptions that must be proved or experimentally tested.
4. Implement a versioned, reproducible experiment with negative controls and uncertainty/model sensitivity.
5. Validate all claimed derivative, optimization, or causal inferences at the evidence level actually available.
6. Compare fairly against current direct baselines under a preregistered or otherwise fixed protocol.
7. Independently reassess novelty after the final method exists.
8. Only then evaluate whether an independently authored, policy-compliant manuscript is viable.

## Available local resources

- Python 3.11, FLORIS-based reproducibility code, and the pinned environment under `ws_submodularity/`;
- web search, Crossref, OpenAlex/arXiv where accessible, DOI/source-page checking, and GitHub code search;
- research skills under `research/skills/`, including the transparent local `doctoral-research-gatekeeper` review gate and the corrected falsification-first interaction-structure workflow;
- source, cache, and audit records retained under `research/`.

Resource availability is not evidence. Each claim remains responsible for its own validation and scope.
