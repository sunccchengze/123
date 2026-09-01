---
name: interaction-structure-miner
description: |
  A falsification-first workflow for examining second-order interactions in
  engineering objective functions. It helps formulate conditional derivative
  identities, test their assumptions, and archive counterexamples. It does not
  infer strategic complements, substitutes, decoupling, or optimizer guarantees
  from topology or finite differences alone.
triggers:
  - interaction structure
  - complements substitutes
  - sign matrix
  - decoupling at the optimum
  - mixed partial decomposition
  - novelty audit
---

# Interaction Structure Miner — falsification-first edition

> Before interpreting a mixed partial, ask whether the model, derivative, unit,
> and operating point actually justify the interpretation.

## Purpose

Use this workflow to investigate whether a scientific or engineering objective
has meaningful pairwise interactions. It can produce a **conditional** analytic
identity for a deliberately specified model and can organize numerical
experiments. It cannot turn a finite grid, a Hessian estimate, or a graph
picture into a theorem, a physical law, a global optimizer guarantee, or a
novelty claim.

The previous P1/P2 use of this skill overreached. The corrective record is
`research/P1_P2_FORENSIC_STATUS.md` and the reproducible test is
`research/ws_submodularity/p1_p2_forensic_audit.py`.

## Mandatory gate 0: declare the exact mathematical object

Before differentiating, record all of the following:

1. **Variables and units.** State whether angles are in radians or degrees. A
   derivative formula for `sin(gamma)` is a radian formula; a degree-scaled
   finite difference has different units.
2. **Model dependency graph.** Write every dependence explicitly. Do not assume
   a wake deficit at receiver `j` is only `w_ij(gamma_i)` when the model has
   secondary steering, yaw-added recovery, turbulence feedback, effective yaw,
   dynamic states, or a changing wind direction.
3. **Regularity domain.** Prove or check differentiability on the region in
   question. Engineering wake maps can be nonsmooth or discontinuous near wake
   overlap boundaries and validity warnings.
4. **Local sign assumptions.** Recovery monotonicity
   `-partial w_ij / partial gamma_i >= 0` is an assumption to test, not a
   consequence of choosing a positive yaw angle. Test laterally offset and
   wrong-way configurations as well as aligned cases.
5. **Pair orientation.** If a direct term applies only to an upstream-to-
   downstream relation, define an ordered pair. Mixed partials themselves are
   symmetric, so an expression announced for arbitrary unordered pairs must
   respect that symmetry.

If any item is absent, stop. Label the output a hypothesis or a local numerical
screen rather than a structural result.

## Conditional analytic exercise

For the intentionally restricted map

`P(gamma) = sum_k p_k(gamma_k) phi(v_k(gamma))`,
`v_k = 1 - sum_{i precedes k} w_ik(gamma_i)`,

with a fixed DAG, separable `C^2` kernels, and explicitly checked sign
conditions, differentiate symbolically. For a pair that is **ordered** as
`i precedes j`, separate:

- terms through receivers downstream of both variables;
- the direct effect through receiver `j` and its own power factor; and
- all residual terms if the assumed separability is relaxed.

For sum-of-squares superposition, do not infer a positive common-beneficiary
term merely from convexity of `phi`: the velocity has a negative cross
curvature, so the full inequality must be derived for the exact `phi` and
parameter domain. Do not extrapolate such an identity to FLORIS GCH, LES, or a
field farm without a model-by-model dependency proof.

## Numerical screening protocol

A screen can be useful if it is described honestly.

1. **Refine finite differences.** Report values for several steps, e.g. 5, 2.5,
   1, 0.5, and 0.25 degrees. If signs or material magnitudes do not stabilize,
   withdraw the local derivative interpretation. Never cherry-pick the coarse
   step.
2. **Include negative controls.** Test a laterally offset/wrong-way case, an
   aligned case, and a known failure or warning region. Archive all outputs.
3. **Separate evidence classes.** A Hessian estimate is a numerical diagnostic;
   it is not an analytic mixed partial unless convergence and regularity have
   been demonstrated. A finite grid cannot prove continuous monotonicity,
   strictness, a global supremum, or an inverse-map property.
4. **Do not hide model warnings.** Treat negative rotor velocities, clipping,
   solver warnings, or discontinuities as failed/excluded cases with reasons,
   not as data to silently remove.
5. **Freeze all protocols before comparison.** Record layout, inflow, yaw signs,
   models, code version, mesh/step sizes, seeds, stopping rules, and exact
   objective units in a machine-readable cache.

## Algorithmic claims require a separate proof and implementation audit

- A sampled maximum of `|M_ij|` is not a global supremum. It cannot certify a
  greedy gap, cross-cluster loss, or Jacobi contraction without validated global
  bounds.
- Inspect update semantics, not names. In-place coordinate updates are
  Gauss--Seidel; a Jacobi step evaluates all subproblems against a frozen
  iterate and commits them together.
- Measure actual parallel execution with matched numerical tolerances and
  hardware. Projected parallel speed is not a benchmark result.
- Test against appropriate contemporary methods, multiple starts, multiple
  layouts/inflows, uncertainty, actuator constraints, loads, and a reference
  whose limitations are stated.

## Novelty audit

Only begin a novelty claim after the mathematics and implementation survive the
above gates. Search web, scholarly indices, repositories/code, and relevant
languages. Treat a direct predecessor as a reason to narrow or abandon a claim,
not as a citation to mention while retaining `first` language. Record queries,
dates, source URLs/DOIs, and the exact distinction.

## Completion record

A completed audit must state:

- every assumption that was verified, unverified, or falsified;
- all finite-difference refinement values and counterexamples;
- the exact evidence class for every retained conclusion;
- predecessor literature and remaining novelty uncertainty; and
- what would be required for a proof, high-fidelity validation, or submission.

A passing numerical screen is never publication readiness by itself.
