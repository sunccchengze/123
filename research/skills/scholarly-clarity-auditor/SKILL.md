---
name: scholarly-clarity-auditor
description: |
  Human-centered scientific-prose audit for drafts whose technical claims have
  changed during validation. Detects inflated novelty, evidence-category drift,
  robotic boilerplate, overloaded sentences, and citations that do not support
  the adjacent claim. It never disguises AI-generated writing or replaces an
  author's independent verification.
triggers:
  - humanize academic prose
  - scholarly clarity audit
  - claim-to-evidence review
---

# Scholarly Clarity Auditor

## Purpose

Use this audit after technical edits and before submission. The goal is readable,
precise scholarly prose: not a cosmetic "humanizer" score and never a way to
circumvent an author's, journal's, or disclosure obligations.

## Workflow

1. **Make a claim ledger.** For each abstract conclusion, contribution bullet,
   figure caption, and conclusion sentence, classify the statement as one of:
   mathematical proof, conditional proposition, numerical observation,
   benchmark result, interpretation, or future work. Remove a claim or relabel
   it if its evidence class is unclear.
2. **Check the nearby citation.** Verify that each citation supports the exact
   verb and scope next to it. Cite substantive predecessors even when they
   narrow the paper's novelty; do not cite an unrelated title as a shield.
3. **Read aloud for an informed colleague.** Split stacked clauses, replace
   generic transitions with concrete subjects and verbs, define a term on first
   use, and vary sentence rhythm. Preserve all qualifiers that protect validity.
4. **Run the red-flag pass.** Search for absolute or sales-like language:
   `first`, `novel operating mode`, `solved`, `guarantee`, `certificate`,
   `proves`, `exact`, `state of the art`, `all`, `always`, and `never`.
   Every retained occurrence needs a theorem, a stated condition, or a source.
5. **Perform the adversarial read.** Ask what an APC specialist, numerical
   analyst, experimentalist, and editor could each object to. Put the answer in
   the limitations or delete the claim.
6. **Author and policy check.** The named author must independently verify
   technical content and independently write/rewrite prose as required by the
   target journal. Do not treat this audit as evidence of authorship or policy
   compliance.

## Completion record

Record the red-flag search, citation checks, unresolved risks, and exact files
reviewed in `SELF_AUDIT.md`. A draft passes only when its language and evidence
classes agree; passing does not establish publication readiness.
