---
name: doctoral-research-gatekeeper
description: |
  A transparent, supervisor-style research gate for deciding whether an
  engineering research project is a valid paper candidate, a useful research
  record, or a topic to abandon. It prioritizes falsification, consequence,
  novelty, theory, validation, reproducibility, and publication ethics over
  polish or aspirational impact claims.
triggers:
  - evaluate research impact
  - doctoral supervisor review
  - is this paper publishable
  - transform paper into high impact research
  - submission go no-go
---

# Doctoral Research Gatekeeper

> This is a local workflow, not a claim of supervision by a human doctoral
> advisor or of access to an external “Supervisor-Skills” package.

## Purpose

A strong paper is not defined by confident prose, a large simulated gain, or a
new acronym. It changes a well-defined scientific or operational decision, and
its central claim survives efforts to falsify it. Academic attention cannot be
guaranteed; the correct goal is a contribution that would withstand expert
scrutiny and be worth independent reuse.

## The seven gates

### G0 — Claim integrity

Create a claim ledger for each conclusion. Classify it as proof, conditional
proposition, numerical observation, benchmark result, interpretation, or future
work. A paper fails G0 if its strongest sentence has no source, proof, raw
output, or scope statement.

### G1 — Consequence before novelty

State the decision that changes if the result is true. Quantify the relevant
failure cost, uncertainty, constraints, and stakeholders. “An optimizer gives a
larger FLORIS number” is not a sufficient consequence. A candidate should make
an engineering, physical, mathematical, or measurement decision better than the
closest alternative.

### G2 — Novelty under hostile search

Search close terminology, older terminology, methods, code, patents where
relevant, citations of the closest papers, and sources in relevant languages.
Read primary sources rather than snippets. A zero-hit query means only that the
query had no hit. If a direct predecessor exists, abandon the broad claim or
write down a narrow, testable distinction and search again after the method is
fixed.

### G3 — Mathematical and computational validity

State domains, units, ordering conventions, regularity, dependencies, and
algorithm semantics. Test counterexamples, resolution/step convergence, and
boundary behavior. A finite grid does not prove continuity, uniqueness, a global
bound, convergence, or a certificate. A code label does not define an algorithm.

### G4 — Validation ladder

Match validation to the claim:

| claim level | minimum credible evidence |
|---|---|
| conditional mathematical result | complete proof checked independently; explicit model scope |
| engineering-model observation | versioned configuration, negative controls, refinement, cross-model tests |
| dynamic controller | actuators, delays, time-varying inflow, repeated trials, matched baselines |
| load/safety claim | credible structural/load model plus uncertainty and constraint treatment |
| deployability/physical claim | independent LES, wind-tunnel, field evidence, or a clearly stated limitation |

A lower rung may motivate the next rung but cannot replace it.

### G5 — Fair comparison and reproducibility

Predeclare primary metric, data splits or scenarios, stopping rules, tuning
budgets, hardware, seeds, exclusions, and statistical summaries. Compare against
the strongest relevant current baselines, not only a weak local implementation.
Archive code, raw/reduced data, environments, provenance, and negative runs in a
permanent repository before claiming reproducibility.

### G6 — Authorship and publication eligibility

The author must independently understand, verify, and write any submission. Read
the current venue policy directly. AI assistance, data permissions, authorship,
conflicts, and archival claims are hard gates—not afterthoughts.

## Red-team panel

Before advancing a candidate, write answers from five adverse reviewers:

1. **Domain scientist:** Is the mechanism physical or merely behavior of a
   chosen surrogate?
2. **Numerical analyst:** Does the evidence support the stated derivative,
   optimum, rate, or bound?
3. **Control engineer:** Are sensing, dynamics, actuation, constraints, and
   safety represented?
4. **Experimentalist/data scientist:** Is there a credible measurement design,
   calibration, uncertainty treatment, and counterfactual?
5. **Editor/reviewer:** What exactly is new relative to the closest three
   papers, and could another group independently reuse it?

An unanswered objection is a work package, not a limitation sentence that can be
hidden at the end.

## Impact classification

Do not promise a “sensation.” Assign one of these current statuses instead:

- **Archive only:** a useful record or negative result but no validated central
  contribution.
- **Question candidate:** a consequential and falsifiable question whose novelty
  is unresolved.
- **Research candidate:** an explicit contribution has passed G0–G3 and has a
  credible G4–G5 plan.
- **Submission candidate:** all seven gates have evidence; independent author
  verification and venue compliance are complete.

## Completion record

For every gate review, store the status, evidence links, direct predecessors,
failed hypotheses, unresolved external resources, kill criteria, and the exact
next experiment or proof. Never replace a failed gate with stronger adjectives.
