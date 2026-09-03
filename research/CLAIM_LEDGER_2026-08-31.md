# Claim ledger — forensic correction round

**Audit date:** 2026-08-31
**Purpose:** Apply the `scholarly-clarity-auditor` workflow to the active research records after the P1/P2 forensic run. This is an evidence map, not a declaration of publication readiness.

## Evidence classes

| label | meaning |
|---|---|
| **Conditional proposition** | A standard or derived statement that is valid only after its listed hypotheses are independently verified. |
| **Model-scoped numerical observation** | Deterministic output from a stated FLORIS configuration; not a physical or global conclusion. |
| **Code-semantics finding** | Result obtained by inspecting/replicating update behavior; not a convergence or performance theorem. |
| **Literature/metadata finding** | Claim about a source verified against a primary source or DOI metadata on the audit date. |
| **Editorial fact** | Record or policy boundary that constrains use of the materials. |

## P1 ledger

| active statement | evidence class and source | required boundary | disposition |
|---|---|---|---|
| The old separable-kernel derivation did not automatically cover FLORIS GCH. | Literature/model-scope finding: King et al. (2021), [doi:10.5194/wes-6-701-2021](https://doi.org/10.5194/wes-6-701-2021), describes yaw-added recovery and secondary steering. | Does not say no restricted separable model can be studied. | Retained as a correction. |
| Positive upstream yaw can lower a laterally offset receiver’s FLORIS power. | Model-scoped numerical observation: `ws_submodularity/p1_p2_forensic_audit.py`; cache SHA-256 `63d6cdfa6b8ce634aae266a2a2e1d881db10c50921898dbe335f9feae52b6850`. At 5D/−1D, receiver change is −46.17498450511289 kW from 0° to 5°. | One FLORIS 4.6.6 engineering-model configuration; not a general physical-farm claim. | Retained as a counterexample to automatic premise. |
| The former `(20°,20°,20°)` sign flip is not a verified local-Hessian result. | Model-scoped numerical observation in the same cache: `h=5°` gives −0.2154202323 kW deg⁻²; `h=1°` gives +0.0223148977 kW deg⁻²; refined steps remain positive. | No derivative or phase-boundary conclusion follows from the screen. | Retained as a withdrawal basis. |
| A sampled interaction maximum does not certify a yaw-box bound. | Conditional logical finding: the previous bound requires a supremum over its stated box, while the old protocol sampled finitely many states. | A future result requires analytic or validated numerical enclosure over the declared domain. | Retained as a withdrawal basis. |

## P2 ledger

| active statement | evidence class and source | required boundary | disposition |
|---|---|---|---|
| Historical `djs` is a cyclic in-place Gauss–Seidel sweep, not frozen-state Jacobi. | Code-semantics finding: `exp_djs.py:djs`; independently reproduced by the forensic script. | This does not make Gauss–Seidel invalid; it invalidates calling this implementation Jacobi or parallel. | Retained as a correction. |
| The first-sweep traces differ under actual synchronous Jacobi. | Model-scoped code-semantics observation in forensic cache: 3-chain 3295.691 vs 3267.736 kW; 3×3 10042.514 vs 9927.945 kW. | Same final integer-grid state after selected sweeps is not equivalence, convergence, rate, or runtime evidence. | Retained as a correction. |
| Wake-digraph clustering/decoupling and serial refinement have direct antecedents. | Literature/metadata finding: Shu et al. (2022), [10.1016/j.apenergy.2021.117986](https://doi.org/10.1016/j.apenergy.2021.117986); Li et al. (2025), [10.1080/15435075.2025.2472291](https://doi.org/10.1080/15435075.2025.2472291); Tu et al. (2026), [10.1016/j.apenergy.2025.127259](https://doi.org/10.1016/j.apenergy.2025.127259). | A distinct future method could still be assessed only after direct comparison and a new audit. | Retained; broad `first` claims withdrawn. |
| Kuo et al. (2020) is not the WGWD reference. | Literature/metadata finding: its shared bibliography title is *Wind Farm Yaw Optimization via Random Search Algorithm*. | Do not reuse it as support for weighted graph wake decoupling. | Retained as citation correction. |

## P3 ledger

| active statement | evidence class and source | required boundary | disposition |
|---|---|---|---|
| A continuous scalar response has at least one endpoint-bracketed root; strict increase gives uniqueness. | Conditional proposition (intermediate-value and injectivity facts). | The 41- and 401-node traces do not verify continuity, strict increase, a derivative lower bound, or unique inversion. | Retained only with conditions. |
| The selected 3×3 ray is non-decreasing at 41 and 401 samples; Brent residual and five-node proxy residual are as recorded. | Model-scoped numerical/benchmark observation: `ray_monotonicity.json`, `table2_tracking.json`, `proxy_tracking_benchmark.json`. | The nine targets are interior targets; this is not dynamic tracking, an online-budget comparison, or a controller result. | Retained as a static benchmark record. |
| Direct yaw/APC tracking and reserve antecedents exist. | Literature/metadata finding: Starke et al. (2023), [10.23919/ACC55779.2023.10156444](https://doi.org/10.23919/ACC55779.2023.10156444); Oudich et al. (2023), [10.1002/we.2845](https://doi.org/10.1002/we.2845); Sterle et al. (2024), [10.1088/1742-6596/2767/3/032005](https://doi.org/10.1088/1742-6596/2767/3/032005); Tamaro et al. (2025, 2026), [10.5194/wes-10-2705-2025](https://doi.org/10.5194/wes-10-2705-2025) and [10.5194/wes-11-1607-2026](https://doi.org/10.5194/wes-11-1607-2026). | No `first yaw power tracking` or dynamic performance claim remains. | Retained as citation correction. |

## Citation-adjacency review

- `paper1_interaction_structure.tex`: King et al. is adjacent to the GCH secondary-steering scope statement; Gori et al. is adjacent to model/implementation sensitivity; Fleming et al. is adjacent to fixed-angle beneficial/detrimental experimental context.
- `paper2_djs_clustering.tex`: Wright and Richtárik–Takáč are adjacent to the generic coordinate-method caveat; Shu, Li, and Tu are adjacent to the specific prior-art correction; Gori is adjacent to the static-model sensitivity caveat.
- `paper3_power_tracking_inverse.tex`: Oudich, Starke, Sterle, and Tamaro are adjacent to their respective APC/yaw-tracking context, not used to imply performance of the static benchmark.

## Red-flag review

The active P1/P2 source records intentionally retain terms such as `certificate`, `guarantee`, `theorem`, and `Jacobi` only to say that earlier uses are withdrawn. P3 uses `unique`, `inverse`, and `monotonicity` only inside explicitly conditional statements or limitation language. No active record retains a `first`, `proven`, `publication-ready`, global-performance, or physical-law claim.

## Editorial gate

The official Copernicus AI policy was rechecked on 2026-08-31: [AI policy](https://publications.copernicus.org/for_authors/ai_policy.html). It permits assistive grammar/readability uses but says generative AI must not be used for manuscript text or interpretations. Because the archived prose received substantive generative-AI assistance, these materials are not WES-submission prose. This is an editorial fact independent of the scientific defects.

## Remaining risks and next gate

1. The literature audit is date- and query-bounded; it must be rerun after any genuinely new method or theorem exists.
2. No official Copernicus-class compile or permanent DOI archive has been completed.
3. No field, wind-tunnel, LES, dynamic-control, actuator, or load result establishes the retired P1/P2/P3 research claims.
4. Any future manuscript requires independent author reconstruction, proof checking, protocol setting, source reading, and writing.
