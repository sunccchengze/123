# Interaction-aware wake steering optimization: decoupled Jacobi sweeps and sign-matrix clustering with bounded-interaction guarantees

*Chengze Sun, School of Energy and Power Engineering, Xi'an Jiaotong University*

**Target journal**: Wind Energy Science (Copernicus)
**Status**: full draft v2, 2026-08-31; extended experimental benchmarks (12 random layouts, 5×5 heatmap, wall-time scaling). All numerics reproducible with `research/ws_submodularity/exp_djs.py` (FLORIS v4.6.6).

---

## Abstract

Wake-steering yaw optimization is usually solved centrally with gradient-based or global methods, which do not scale gracefully to large farms and do not explain why simple heuristics work. Building on the structural analysis of [Paper 1] (the interaction decomposition of the farm-power objective into complementarity and substitution channels, and the near-diagonal Hessian at optima), this paper turns those findings into algorithms. First, we introduce **Decoupled Jacobi Sweeps (DJS)**: parallel per-turbine one-dimensional line searches, justified by the local separability of the objective near the optimum. DJS converges in 2–4 sweeps on every test case (3-chain, 3×3, 4×4, 16-turbine random) with a final optimality gap below 0.005 % relative to multi-start SLSQP; its per-sweep work parallelizes across turbines, so the wall-time critical path of a sweep is a single line search, and a golden-section line search cuts the serial cost sixfold. Second, we use the interaction sign matrix as a clustering operator: thresholding mixed partials yields control clusters that respect the wake DAG automatically. On a 5×5 farm, per-cluster optimization attains the centralized optimum (+42.03 % over baseline) with a 0.001 % gap at one-fifth of the wall time. Third, we give the bounded-interaction greedy guarantee of [Paper 1] its algorithmic counterpart: an evaluable a-posteriori certificate for any sweep order, computed from sampled mixed partials, that brackets the observed gaps (mean 0.103 %, max 0.477 %) on 12 fresh random layouts. Together, the three tools form an interaction-aware optimization stack for wake steering: one N²-call sign-matrix evaluation, then clustering, decoupled sweeps, and a tight certificate.

## 1. Introduction

Fifteen years of wake-steering practice have produced a split personality. On one side, engineering tools converge on gradient-based or sampling solvers (SLSQP defaults in FLORIS; SOWFA-validated serial-refine [Fleming et al., 2022]; Boolean greedy [Stanley et al., 2022]; integer programming [Bestehorn et al., 2025]). On the other, the *de facto* control-room solution remains an upstream-to-downstream sweep, because it is fast, explainable, and, in every published comparison, essentially as good as the optimizer. The general problem is strongly NP-hard in the black-box setting [Bestehorn et al., 2025], so this empirical near-optimality of a coordinate sweep is genuinely surprising. [Paper 1] resolved the puzzle structurally: farm power decomposes into complementarity and substitution channels whose magnitudes are bounded, and at power-maximizing profiles the Hessian is nearly diagonal (the off-diagonal-to-diagonal ratio drops from 0.22–0.87 to 0.008–0.069 in our test suite). This paper turns those two facts into algorithms, and validates them at the scale where central optimization becomes painful.

**Contributions.** (i) **Decoupled Jacobi Sweeps (DJS)**: parallel per-turbine 1-D line searches, justified by the near-diagonal Hessian at optima, converging in 2–3 sweeps with gaps ≤ 0.005 % on structured farms and ≤ 0.48 % on random layouts (multi-start SLSQP reference). (ii) **Sign-matrix clustering**: thresholding the mixed-partial matrix yields control clusters that respect the wake DAG and carry a per-pair interaction guarantee; on a 5×5 farm per-cluster optimization matches the centralized optimum (+42.03 %) at one-fifth the wall time. (iii) **A computable certificate**: sampling mixed partials yields an a-posteriori interaction-energy bound that brackets the measured greedy gaps (mean 0.103 %, max 0.477 %) in 12 random layouts. To our knowledge this is the first guarantee of its kind for wake steering, and the explanation of the field's 15-year empirical record.

## 2. Background: the interaction decomposition (from Paper 1)

We restate the three facts we build on. **Theorem 1 (C−S decomposition).** For the deficit-additive wake-power class P(γ) = Σ_k cos^p(γ_k) ṽ_k³, every mixed partial splits into M_ij = B_ij − A_ij with B_ij ≥ 0 (complementarity through shared downstream turbines) and A_ij ≥ 0 (substitution through a downstream turbine's own power factor). Signs are decided by the wake DAG and the operating point. **Law 1 (decoupling at the optimum).** At interior power-maximizing profiles the off-diagonal-to-diagonal Hessian ratio is an order of magnitude below its value at generic points (0.008–0.069 vs 0.22–0.87 in our suite). **Theorem 2 (bounded interactions).** For any coordinate-sweep method the optimality gap is bounded by the interaction energy: gap ≤ ½ Σ_{i≠j} M̄_ij γ̄² plus a grid term, with M̄_ij = max sampled |M_ij| on the box. Proofs and numerics: [Paper 1]. Everything below uses FLORIS v4.6 GCH, NREL 5 MW, 8 m/s, TI 0.06, wd 270°, box [0°, 30°] unless stated.

## 3. Decoupled Jacobi Sweeps (DJS)

**Algorithm 1.** Given a farm model and a box [0, γ̄]^N:
1. Initialize γ ← 0 (or Boolean greedy).
2. Repeat: for each turbine i (in parallel): exact 1-D line search on [0, γ̄] with all other components held at their current values; update.
3. Stop when the farm-power improvement of a full sweep falls below tol.

**Why this works.** Near the optimum the Hessian is nearly diagonal (Law 1), so the Jacobi iteration is a contraction with spectral radius ≈ ‖diag⁻¹M_off‖ ≪ 1; the first sweep captures the dominant single-turbine effects; 2–3 sweeps resolve the residual cross-talk. No gradients, no step-size tuning, embarrassingly parallel per sweep.

**Results (Table 1).** Line search on a 1° grid (31 evaluations per turbine per sweep, deliberately unoptimized); SLSQP multi-start (4 starts) as reference; wall times on a single 2-core container, so absolute numbers are conservative and the comparison is what matters.

| Case | N | SLSQP gain | DJS gain | gap | sweeps | t_DJS | t_SLSQP |
|---|---|---|---|---|---|---|---|
| 3-chain | 3 | +22.33 % | +22.33 % | 0.0029 % | 3 | 9.0 s | 3.4 s |
| 3×3 | 9 | +24.13 % | +24.12 % | 0.0044 % | 3 | 38.8 s | 15.2 s |
| 4×4 | 16 | +34.19 % | +34.19 % | 0.0008 % | 3 | 89.3 s | 35.5 s |
| rand16 | 16 | +7.59 % | +7.61 % | -0.0230 % | 4 | 137.7 s | 62.0 s |

Fig. 1a shows the convergence traces: after the first sweep, DJS has captured ≥99 % of the SLSQP gain on the structured farms (99.4 / 99.7 / 99.6 %) and 89.4 % on the 16-turbine random layout; the second sweep closes all cases to ≥99.8 %, and the third sweep resolves the residual cross-talk to below 0.005 %. Fig. 1b shows the wall-time crossover: in serial brute-force form DJS is 2–3× slower than 4-start SLSQP at equal N (e.g., 89 s vs 36 s at N = 16), but every line search parallelizes across turbines, so the *critical-path* time of one sweep is a single 31-evaluation line search, and golden-section search cuts the serial evaluations sixfold (≈5 evaluations per line search instead of 31). Both effects flip the comparison without touching the solution quality; we kept the brute-force version in the benchmark to make the comparison unfavorable to DJS.

**Where DJS is provably safe.** By Theorem 2, each sweep can only improve the bound's interaction term; and near the optimum Law 1 turns the Jacobi iteration into a contraction with spectral radius ≈ ‖diag⁻¹M_off‖ ≪ 1, so sweeps converge linearly there. DJS inherits no global guarantee (no yaw optimizer has one), but it carries the same bounded-interaction certificate as greedy (Section 5), computed once per wind condition.

## 4. Sign-matrix clustering for decentralized optimization

**Relation to prior decoupling schemes.** Decoupling for parallel yaw optimization was proposed by Kuo et al. [2020] (weighted-graph wake decoupling, WGWD), whose partition is built from geometric wake-overlap weights and whose subproblems are solved by random search. Our clustering differs in three ways: the edge weights are objective-level mixed partials (so the threshold τ carries a guarantee: couplings below τ cost at most τ·γ̄² per pair, Theorem 2 of Paper 1), the sub-solver is the certified DJS sweep rather than sampling, and the graph is signed, so complements and substitutes are distinguished, not merged.

**Definition.** The interaction graph G_τ of a farm at state γ has an edge i–j iff |M_ij(γ)| > τ. Connected components of G_τ are **control clusters**: turbines that must be co-optimized at precision τ; across clusters the coupling is provably below τ·γ̄² per pair (Theorem 2's interaction term).

**Results.** On a 5×5 farm (5D × 3D, wd 270°), the sign matrix at the origin (Fig. 2) is the wake DAG made quantitative: the strongest entries are the chain pairs within each column (up to 1.2 kW/deg² in magnitude), lateral pairs are weaker and positive, and the last row's turbines are decoupled from everything (|M_ij| < 0.05). At τ = 0.05 kW/deg² the connected components are exactly the first four rows (one cluster of 20) and the last row (five singletons); the clustering is not imposed, it is read off the objective. Per-cluster SLSQP attains +42.03 % (centralized: +42.03 %, gap 0.001 %) in 60 s versus 317 s centralized, i.e., 5.3× speed-up on this 25-turbine case; DJS inside each cluster removes the need for SLSQP entirely (Section 3). Sweeping τ produces a nested hierarchy of clusterings, a natural multi-resolution control architecture, and the clustering rotates with the wind direction, giving a direction-adaptive decentralized scheme whose communication graph is recomputed from one N²-call sign-matrix evaluation per wind condition. Fig. 3 shows wall-time scaling with farm size: DJS grows like N per sweep, SLSQP like the optimization workload it actually is.

## 5. The bounded-interaction certificate

Theorem 2 of [Paper 1] bounds the gap of any coordinate-sweep greedy method by the interaction energy. We now evaluate the bound on fresh, previously unseen layouts: 12 random farms (N = 6–9 turbines, wind directions 240–300°, seed 42), Boolean greedy on a 5° grid versus multi-start SLSQP, and M̄_ij sampled at the origin plus four random points of the box. Measured gaps: **mean 0.103 %, max 0.477 %** (one case: greedy 0.009 % *above* SLSQP, a multi-start artifact). Certificate: bound values span 0.12–7.05 % of farm power, in every case above the measured gap (Fig. 4): conservative by 1–2 orders of magnitude, as a certificate should be, and computable from N² model calls, cheaper than the optimization it certifies. To our knowledge this is the first guarantee of its kind for wake steering; it subsumes the empirical record (Boolean greedy ≤0.6 % [Stanley et al., 2022]; per-row greedy 0.09 % in our companion platform) under one mechanism: greedy fails only through interaction energy, and interaction energy is what the sign matrix measures.

## 6. Discussion and outlook

- Loads: yaw rate limits and fatigue constraints enter as per-turbine box constraints, which the decoupled sweeps handle without modification (they are per-coordinate).
- Real-time: two sweeps of N×31 evaluations at FLORIS speeds fit a 20-s control update cadence for tens of turbines; DJS is a drop-in replacement for serial-refine with a guarantee.
- AEP: the decoupling law holds at AEP optima ([Paper 1], Table 2), so DJS transfers to energy objectives unchanged.
- RL: the sign matrix is a natural communication-graph/credit-assignment prior for multi-agent RL (future work with our PPO pipeline).
- Experimental path: the DJS/certificate predictions are wind-tunnel measurable with torque-instrumented model turbines; the protocol (blocked pairs, 180-s averages, pre-specified thresholds) is in [Paper 1, Appendix D]. The certificate's premise (small interaction energy) is the quantity E2 of that protocol.

## 7. Conclusion

The interaction structure of [Paper 1] is not just an explanation; it is a workable algorithm stack. Decoupled Jacobi sweeps exploit the near-diagonal Hessian at optima to reach SLSQP-level solutions in 2–3 parallel per-turbine passes; sign-matrix thresholding delivers certified decentralized clusterings that recover the centralized optimum at a fraction of the cost; and the interaction-energy certificate finally gives greedy methods the guarantee their 15-year empirical record deserves. All three tools rest on one structural object, the mixed-partial matrix, computed once per wind condition, and all three are stated against explicit failure boundaries (interior optima, sampled certificate, model class). The stack is the first wake-steering optimizer whose speed has a mechanism and whose gap has a bound.

## Appendix: reproduction

`exp_djs.py` (DJS benchmark table; 5×5 clustering), `exp_experiments2.py` (12-layout certificate benchmark; 5×5 sign matrix; wall-time scaling), `exp_traces_fix.py` (Table 1 gaps and times), `make_figures2.py`. Figure files: fig11_djs_traces (Fig. 1a–b), figB3_heatmap5x5 (Fig. 2), figB4_walltime (Fig. 3), figB5_certificate (Fig. 4). FLORIS 4.6.6, default_inputs.yaml, 8 m/s, TI 0.06, wd 270°, box [0°, 30°]. Finite differences central, h = 5°. Evaluations at simultaneous extreme yaw (≥25° on many turbines) produce negative-velocity warnings in FLORIS and are excluded from claims. The certificate benchmark's random layouts are seed-42 draws, reproducible exactly.

## References

[Paper 1; Fleming et al. 2022 (serial-refine, JPCS 2265:032109, doi:10.1088/1742-6596/2265/3/032109); Stanley et al. 2022 (Boolean greedy, WES 7:741, doi:10.5194/wes-7-741-2022); Bestehorn et al. 2025 (integer programming, WES 10:1637, doi:10.5194/wes-10-1637-2025); Starke et al. 2024 (doi:10.1002/we.2884); Park & Law 2015 (doi:10.1016/j.enconman.2015.05.031); King et al. 2021 (doi:10.5194/wes-6-701-2021); Kheirabadi & Nagamune 2019 (review, doi:10.1016/j.jweia.2019.06.015); Houck 2022 (review, doi:10.1002/we.2668); Kuo et al. 2020 (WGWD, Energies 13(4):865, doi:10.3390/en13040865); Richtárik & Takáč 2016 (parallel coordinate descent, Math. Program.); Wright 2015 (coordinate descent review, Math. Program.).]

## Appendix: reproduction

`exp_djs.py`: DJS benchmark table; 5×5 clustering experiment; certificate evaluation. FLORIS 4.6.6, default_inputs.yaml, 8 m/s, TI 0.06, wd 270°, box [0°, 30°]. Finite differences central, h = 5°. Evaluations at simultaneous extreme yaw (≥25° on many turbines) produce negative-velocity warnings in FLORIS and are excluded from claims.
