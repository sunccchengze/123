# Archive notice for historical P1/P2 materials

**Status:** The historical P1/P2 scripts, caches, PNGs, and figure generators in this directory are retained for reproducibility and forensic inspection. They are **not** evidence of submission-ready P1/P2 results and must not be reused as support for a theorem, interaction law, phase boundary, greedy certificate, clustering certificate, Jacobi convergence claim, parallel implementation, runtime advantage, or first-of-kind claim.

## Why the original interpretation was withdrawn

- The old analytic P1 map assumed separable source kernels and recovery monotonicity. FLORIS GCH includes secondary steering and yaw-added recovery, and an audited laterally offset case violates automatic recovery monotonicity.
- The old `h=5°` headline mixed finite difference reverses sign at refined steps, so the displayed phase figures are not verified local-Hessian evidence.
- Finite samples cannot establish the yaw-box derivative supremum used by the historic bounds.
- Code called “DJS” changes its state in place and is a cyclic Gauss–Seidel coordinate sweep—not the frozen-state parallel Jacobi method claimed in the original narrative.
- Direct graph sparsification, weighted graph wake decoupling, and serial-refinement antecedents make broad P2 novelty claims untenable.

The falsification-focused replacement is `p1_p2_forensic_audit.py`, which writes `expcache/p1_p2_forensic_audit.json`. The full decision, DOI-verified sources, and re-entry conditions are in `../P1_P2_FORENSIC_STATUS.md`. `THEORY.md` is now a theory-status record, not an established theorem.

## Use of historical outputs

The images beginning `fig1` through `figB5`, and caches such as `exp_p1.json`, `exp_p2.json`, and `decoupling_table.json`, preserve the old explorations. Their captions/titles may contain withdrawn language because changing a raster image would destroy its historical provenance. Read this notice alongside every such file. New work must use a new protocol, new cache namespace, explicit evidence labels, and a fresh novelty audit.

P3 files are separate and carry their own evidence boundary; they remain a narrow static benchmark record rather than a paper candidate.
