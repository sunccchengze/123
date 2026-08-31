# The interaction structure of wake-steering objectives: strategic complements, substitutes, and decoupling at the optimum

*Chengze Sun, School of Energy and Power Engineering, Xi'an Jiaotong University*

**Target journal**: Wind Energy Science (Copernicus)
**Status**: full draft v2, 2026-08-31; experimental section (§9), 12 figures, pre-registration protocol (Appendix D). All numerics reproducible with the scripts in `research/ws_submodularity/` (FLORIS v4.6.6).

---

## Abstract

Wake steering increases wind-farm power by yawing upstream turbines so that their wakes deflect away from downstream rows, and the field has accumulated a puzzle: sequential "greedy" heuristics, which sweep turbines from upstream to downstream, recover 99.4–99.9 % of the gains of continuous optimization, yet no approximation guarantee exists and the general yaw problem is strongly NP-hard. Fifteen years of serial-refine and Boolean-greedy practice have produced no explanation of this near-optimality, and no wind-tunnel or field campaign has ever estimated the second-order structure of farm power. The obstacle is conceptual: pairwise yaw interactions are neither purely substitutes nor purely complements, because yawing a downstream turbine erodes the value of yawing upstream while two turbines yawing together reinforce each other through their shared downstream beneficiaries, and the balance between the two channels depends on the operating point. We resolve the puzzle by analyzing the second-order structure of the objective P(γ). Every mixed partial decomposes into a complementarity channel and a substitution channel, whose sign is decided by the wake-interaction DAG and the operating point (Theorem 1); from the decomposition follow a bounded-interaction greedy bound (Theorem 2), a decoupling law at power-maximizing profiles (Law 1), and monotone comparative statics for the optimal profiles. On FLORIS, serial pairs are strategic substitutes, lateral pairs with shared beneficiaries are strategic complements, and chain pairs undergo a complement-to-substitute phase flip (+0.674 kW/deg² at the origin to −0.215 kW/deg² at (20°, 20°, 20°)); the off-diagonal-to-diagonal Hessian ratio drops from 0.27–0.97 at generic points to 0.022–0.068 at optima across 3×3, 4×4, misaligned, and AEP cases; upstream-to-downstream greedy achieves a mean optimality gap of 0.103 % (max 0.477 %) over 12 random layouts; and the structure survives the LES-calibrated (cc) and field-calibrated (empirical Gauss) model families. A pre-registered wind-tunnel protocol for measuring the three falsifiable predictions is provided (Appendix D).

---

## 1. Introduction

Wake losses cost a wind farm 10–20 % of its gross energy in aligned conditions [Howland et al., 2019]. Wake steering reclaims part of this by misaligning upstream turbines, deflecting their wakes laterally and accelerating downstream rows [Gebraad et al., 2016; Fleming et al., 2014]; field experiments measured 7–13 % gains at favorable directions [Howland et al., 2019].

The optimization side of wake steering has a curious record. The problem is nonconvex and multimodal [Laizet et al., 2022], and Bestehorn et al. [2025] recently proved the discretized problem strongly NP-hard and inapproximable in general. Yet in practice, simple schemes do nearly as well as careful continuous optimization: the Boolean greedy sweep of Stanley et al. [2022] reaches within 0.6 % of gradient-based optima at 50–500× lower cost; serial-refine [Fleming et al., 2022] became the FLORIS default on similar evidence. Nobody has explained *why* these heuristics are so good, and the absence of any approximation guarantee is conspicuous.

This paper provides the missing structural analysis. Rather than studying optimizers, we study the objective. We show that the farm-power function of the standard deficit-additive wake models (the FLORIS GCH family, linear or sum-of-squares superposition) has a clean mixed-partial decomposition: interactions between yaw decisions are either complementary or substitutive, and which one holds for a given turbine pair is dictated by the wake DAG and the operating point. Three findings follow, each independently testable:

1. **Interaction decomposition (Theorem 1).** ∂²P/∂γi∂γj = B_ij − A_ij, with B_ij ≥ 0 a sum of positive contributions from turbines downstream of both i and j, and A_ij ≥ 0 a substitution term active only when j is downstream of i. Serial pairs are substitutes; lateral pairs with common downstream turbines are complements; chain-adjacent pairs flip sign along a phase boundary we compute.
2. **Decoupling at the optimum (Law 1).** At power-maximizing profiles the Hessian is nearly diagonal (off-diagonal/diagonal norm ratio 0.02–0.07, versus 0.27–0.97 elsewhere). The optimum is a point of maximal interactional decoupling; the problem becomes locally separable exactly where we most want it to.
3. **Bounded-interaction greedy guarantees (Theorem 2).** The greedy upstream-to-downstream sweep is optimal to within an explicit bound in the interaction energy, explaining the empirical gaps (mean 0.103 %, max 0.477 % over 12 random layouts) and Stanley et al.'s 0.6 %.

We also show that the sign matrix of mixed partials recovers the wake topology (a farm-level flow diagnostic), and that the decomposition yields monotone comparative statics: optimal yaw profiles decrease monotonically with turbulence intensity and downstream distance, which is the mechanism behind trends observed in sensitivity studies [Gori et al., 2023; King et al., 2021; Quick et al., 2020].

To our knowledge (see the search audit in Appendix C, executed 2026-08-30 against arXiv, OpenAlex/Crossref full-text, and general web in English and Chinese), the interaction decomposition, the sign matrix, the decoupling law, and the greedy bound have not been reported before. The closest prior work: submodularity of the *layout* problem (adding turbines) [Zhang et al., 2011]; graph-based interconnection matrices for *dynamic* farm models [Starke et al., 2024]; game-theoretic utility design without structural analysis [Marden et al., 2013]; and empirical optimal-yaw trends [Gori et al., 2023; King et al., 2021]. Section 8 positions our work against these precisely.

**Paper outline.** §2 defines the model class; §3 proves the decomposition; §4 verifies it numerically and maps the phase structure; §5 establishes the decoupling law; §6 analyzes greedy methods; §7 covers comparative statics; §8 discusses relations and limitations; §9 anchors the theory in existing experiments and pre-registers a falsifiable measurement program; §10 concludes. Appendix A holds proofs, Appendix B the reproduction protocol, Appendix C the novelty audit, Appendix D the experimental pre-registration template.

## 2. Model class and notation

We consider the class of *deficit-additive wake-power maps*, which contains the FLORIS GCH family as a special case. Let N turbines sit at positions x_i ∈ R². The mean flow induces a partial order: i ≺ j ("i upstream of j") if turbine i's wake can affect turbine j; the relation is a DAG along the flow. Each turbine's normalized effective velocity is

ṽ_j(γ) = 1 − Σ_{i≺j} w_ij(γ_i)          (linear superposition), or
ṽ_j(γ) = √(1 − Σ_{i≺j} w_ij(γ_i)²)      (sum-of-squares, FLORIS default),

where w_ij ≥ 0 is the deficit kernel of turbine i evaluated at j's rotor, a C² function of the yaw angle γ_i ∈ [0, γ̄]. We require **recovery monotonicity**: ∂w_ij/∂γ_i ≤ 0, i.e., yawing upstream never deepens the deficit at downstream rotors; write r_ij(γ_i) := −∂w_ij/∂γ_i ≥ 0 for the recovery sensitivity. The farm power is

P(γ) = Σ_j cos^p(γ_j) · ṽ_j(γ)³,

with p = pP ≈ 1.88 in FLORIS. This is the standard model: cubic power law in rotor-effective speed, cos^p self-power factor under yaw misalignment [Howland et al., 2019; King et al., 2021]. All results below hold verbatim for any convex power map φ(ṽ) with φ″ ≥ 0 and any non-increasing self-factor p_j(γ_j).

We write M_ij(γ) := ∂²P/∂γi∂γj for the mixed partial, and call the matrix M the **interaction matrix** of the farm at state γ.

## 3. Theorem 1: the interaction decomposition

**Theorem 1.** For i ≠ j, under either superposition rule,

M_ij(γ) = B_ij(γ) − A_ij(γ), where

B_ij = Σ_{k ≻ i,j} cos^p(γ_k) · β_k(i,j) ≥ 0,
β_k = 6 ṽ_k r_ik r_jk                (linear superposition),
β_k = 3 w_ik w_jk r_ik r_jk / ṽ_k     (sum-of-squares),

and, with 1{·} the indicator,

A_ij = 3p sin(γ_j) cos^{p−1}(γ_j) · ( ṽ_j² r_ij ) · 1{j ≻ i}          (linear),
A_ij = 3p sin(γ_j) cos^{p−1}(γ_j) · ( ṽ_j w_ij r_ij ) · 1{j ≻ i}      (sum-of-squares).

*Proof (linear case; sum-of-squares is identical with ∂ṽ_k/∂γ_i = w_ik r_ik/ṽ_k and the model curvature term ∂²ṽ_k/∂γi∂γj = −w_ik w_jk r_ik r_jk/ṽ_k³).* Differentiate P = Σ_k p_k ṽ_k³, p_k := cos^p(γ_k). For k downstream of both i and j, ∂ṽ_k/∂γ_i = r_ik, ∂ṽ_k/∂γ_j = r_jk, and ∂²ṽ_k/∂γi∂γj = 0, so the k-term contributes p_k·6ṽ_k·r_ik r_jk; this is the B channel. For k = j with j ≻ i, the j-term contributes p_j′·3ṽ_j²·r_ij = −3p sin γ_j cos^{p−1}γ_j ṽ_j² r_ij; this is the A channel. Every other turbine contributes zero because its velocity depends on at most one of γ_i, γ_j. ∎

**Sign rules.** Because B_ij ≥ 0 and A_ij ≥ 0, the sign of each pairwise interaction is decided by the wake DAG:

- **(S1) Independence.** If i, j share no downstream turbine and neither is downstream of the other, M_ij = 0.
- **(S2) Pure chain pair → substitutes.** If j ≻ i and no turbine lies downstream of both, M_ij = −A_ij ≤ 0, strict for γ_j > 0 with r_ij > 0: yaw decisions on a serial pair are strategic substitutes, because yawing the downstream turbine reduces the value of yawing the upstream one. The upstream benefit flows through the downstream turbine's power, whose weight cos^p(γ_j) falls.
- **(S3) Lateral pair → complements.** If neither is downstream of the other and some k lies downstream of both, M_ij = B_ij ≥ 0: yaw decisions are strategic complements, each turbine's yaw raising the marginal benefit of the other's through their common beneficiaries.
- **(S4) General pair → phase structure.** sign(M_ij) = sign(B_ij − A_ij); the set {B_ij = A_ij} is the complement–substitute phase boundary, which moves with spacing, turbulence, and the yaw state.

**Corollary 1 (two turbines).** For a serial pair, M_12 = −A_12 ≤ 0: the two-turbine problem is exactly submodular on the yaw box, i.e., the marginal benefit of yawing turbine 1 decreases in γ₂. Verified in Table 1 (all measured mixed partials negative; magnitude growing with γ₂ as sin γ₂ cos^{p−1}γ₂ predicts).

**Corollary 2 (phase flip, three-turbine chain).** M_12 = 6 cos^p(γ₃) ṽ₃ r_13 r_23 − 3p sin γ₂ cos^{p−1}γ₂ ṽ₂² r_12. Complementarity holds iff

2 cos^p(γ₃) ṽ₃ r_13 r_23 > p sin γ₂ cos^{p−1}γ₂ ṽ₂² r_12.

Since r_13 and r_23 decay with streamwise distance while r_12 does not, complements are favored by short spacing and low turbulence; substitutes dominate for long spacing, high turbulence, and large γ₂. The measured FLORIS phase map (§4.2) matches both the existence and the direction of the flip.

**Corollary 3 (AEP invariance).** AEP(γ) = Σ_ω q_ω P_ω(γ) with q_ω ≥ 0 is a nonnegative mixture, so its interaction matrix is the same mixture of the per-condition matrices: the decomposition, sign rules, and phase structure carry over to energy objectives (wind roses, Weibull integrals). Confirmed numerically in §5.

**Remark (robustness).** The decomposition needs only three ingredients: additive deficits, a convex power map, and a self-factor decreasing in own yaw. It therefore holds across the Gaussian/Jensen/multizone model families and both superposition rules, so the sign rules are not an artifact of one parameterization. Secondary steering [King et al., 2021] changes kernel magnitudes, not the sign structure.

## 4. Numerical verification and the phase structure

**Setup.** All simulations use FLORIS v4.6.6 with the GCH model (Gaussian velocity and deflection, Crespo-Hernández turbulence, sum-of-squares superposition), NREL 5 MW turbines, 8 m s⁻¹ inflow, TI = 0.06 unless stated, wind direction 270° (meteorological), yaw box [0°, 30°]. Mixed partials are central finite differences (h = 2.5–5°). The setup reproduces the validation numbers of our companion engineering project to the last digit: two turbines at 5D: 2190.39 kW baseline, 2368.40 kW at 25° (+8.13 %); 3×3 at 5D×3D: 8095.15 kW baseline, +14.87 % (row 1 yawed 30°), +22.73 % (rows 1–2), +24.04 % (per-row [30,20,0]°), so the structures we report are those of the standard engineering model.

**4.1 Two-turbine and three-turbine chains.** Table 1: the two-turbine mixed partial is negative throughout the valid region (γ₂ ≤ 25°), with magnitude growing in γ₂, exactly the A-channel law A ∝ sin γ₂ cos^{p−1}γ₂ (the γ₂ = 30° boundary is excluded: FLORIS reports negative rotor velocities beyond 25° there). For the three-turbine chain, M_13 and M_23 (pairs whose downstream member has no further beneficiaries) are negative everywhere; M_12 flips sign with the operating point: +0.674 kW/deg² at the origin (complementarity through the shared turbine 3 dominates), −0.215 at (20°,20°,20°) (substitution dominates), +0.058 at the near-optimal [30,20,0]°. The flip is the predicted two-channel competition.

**4.2 Phase map.** Figure 1 maps sign(M_12) over the (γ₂, γ₃) plane at γ₁ = 20°: complements at small γ₂, substitutes beyond a boundary that moves right as γ₃ grows (the shared-beneficiary channel strengthens with γ₃, since r_23 grows while the wake is still interacting with turbine 3). Evaluations at γ ≥ 25° near the box corners were excluded: FLORIS reports negative rotor velocities there, and finite differences lose convergence. This is a model validity boundary, not physics, and we report it as such (see Appendix B).

**4.3 The sign matrix of the 3×3 farm.** Figure 2 shows the full 9×9 interaction matrix at the origin and at the optimum. At the origin the matrix *is* the wake DAG: same-column chain pairs (1,4), (2,5), (3,6) carry the largest entries (+0.67, +0.67, +0.67 kW/deg²); same-row lateral pairs (1,2), (2,3) are weaker complements (+0.19); the last row is decoupled from everything. At 300° wind the pattern re-assembles around the rotated flow geometry; the sign matrix is a direct, computable diagnostic of farm flow topology, complementary to (and sharper than) the binary interconnection matrices of graph-based dynamic models [Starke et al., 2024], since it measures interaction *strength and sign of the objective*, not just connectivity.

**4.4 Robustness across model choices.** The decomposition is model-robust (§3 Remark), and the observable signatures are too: with the Jiménez deflection model the optimum again shows a near-diagonal Hessian (off-diagonal ratio 0.042 vs 0.319 at baseline) and a row-monotone profile. The Jensen velocity model at these conditions has its optimum at the box corner (yaw = 0 everywhere, no steering benefit), a known model-dependence [Gori et al., 2023]; corner optima are excluded from the decoupling law, which concerns interior optima.

## 5. Law 1: decoupling at the optimum

**Observation (the decoupling law).** At power-maximizing yaw profiles, the interaction matrix is nearly diagonal. Table 2 reports the off-diagonal-to-diagonal Frobenius ratio ‖M_off‖/‖diag(M)‖:

| Case | at optimum | at γ = 0 | at γ = 20° |
|---|---|---|---|
| 3×3, wd 270° | **0.023** | 0.360 | 0.404 |
| 3×3, wd 300° | **0.022** | 0.266 | 0.648 |
| 3-chain | **0.030** | 0.349 | 0.170 |
| 4×4, wd 270° | **0.055** | 0.521 | n/a |
| 3×3, AEP over 12 directions | **0.068** | 0.966 | n/a |
| 6-turbine random (weak benefit) | 0.174 | 0.181 | 0.334 |

The drop is an order of magnitude or more in every case with an interior optimum. The optimal profiles themselves are row-synchronous and monotonically decreasing downstream (the 4×4 optimum is rows at [30°, 25.5°, 16.5°, 0°]), consistent with the lattice structure of §3.

**Stationarity identity (three-turbine chain).** At an interior maximizer, ∂P/∂γ₂ = 0 gives p sin γ₂* cos^{p−1}γ₂* = 3 cos^p(γ₃*) ṽ₃² r_23 / ṽ₂³, and substitution into M_12 leaves

M_12(γ*) = 3 cos^p(γ₃*) ṽ₃ r_23 · ( 2 r_13 − 3 ṽ₃ r_12 / ṽ₂ ).

At the optimum the two channels are *tied* by the middle turbine's stationarity, and the residual interaction is set by one factor that is small in the operating regime (far-wake: ṽ₃ ≈ ṽ₂ ≈ recovered, r_13 ≪ r_12). Full decoupling (M ≡ 0 at optima) remains open; we state it as a conjecture with the small-deficit regime as the leading mechanism.

**Algorithmic consequences.** Near the optimum the problem is locally separable: per-turbine 1-D line searches can run in parallel without cross-talk, and a diagonal (Jacobi) preconditioner suffices for second-order steps. This is precisely the regime in which serial-refine [Fleming et al., 2022], Boolean greedy [Stanley et al., 2022], and row-wise schemes operate, which explains their near-optimality despite no global guarantees (§6 makes this quantitative).

## 6. Greedy methods and the bounded-interaction guarantee

**Theorem 2 (greedy gap via interaction energy).** Let x^G be the output of the upstream-to-downstream coordinate-greedy sweep on the grid {0, δ, …, γ̄}, and x* any maximizer of P over [0, γ̄]^N. Then

P(x*) − P(x^G) ≤ ½ Σ_{i≠j} M̄_ij γ̄² + ½ Σ_i d̄_i (δ/2)² + Σ_i d̄_i δ γ̄ · 1{grid truncation},

with M̄_ij = sup|M_ij| over the box and d̄_i = sup|∂²P/∂γ_i²|. (Proof in Appendix A; it uses a second-order path expansion, grid-optimality of each greedy coordinate, and the observation that the linear term is controlled by per-coordinate grid sub-optimality.)

The bound says: greedy can fail only through the interaction energy, and the interaction energy is what §4–5 measured: small, localized, and *vanishing at the optimum itself*. It also explains the shape of the empirical record:

- Our 12 random layouts (N = 6–9, wd 240–300°): greedy within **0.103 % (mean) / 0.477 % (max)** of multi-start SLSQP, and the sampled-M̄ certificate brackets every measured gap.
- The companion project's 3×3: greedy [30,20,0]° = +24.04 % vs SLSQP +24.13 %, a 0.09 % gap.
- Stanley et al.'s Boolean sweep: ≤0.6 % across random and real layouts; serial-refine similar.

The bound is not vacuous: with sampled M̄_ij and d̄_i, it evaluates to the same order as the observed gaps (Table 3). Conversely, §4.2 shows where greedy *could* fail: at operating points with strong complementarity, the sweep order matters, and we recommend evaluating the sign matrix once (N² model calls) before choosing between an upstream-to-downstream sweep (substitution-dominant farms) and row-synchronous joint optimization (complement-dominant farms).

## 7. Comparative statics: why optimal profiles look the way they do

The decomposition turns scattered empirical trends into consequences of one mechanism.

**Turbulence.** The self-cost term −p sin γ₁ cos^{p−1}γ₁ ṽ₁³ is independent of TI, while every recovery sensitivity r_ij decreases pointwise with TI (wakes recover faster). Hence ∂P/∂γ₁ has the single-crossing property in (γ₁, TI), and γ₁* is monotone non-increasing in TI, with no convexity assumption. Measured (Figure 3): two-turbine γ₁* falls 29.8° → 28.1° → 25.3° → 21.0° → 10.7° → 0.8° as TI rises 0.03 → 0.15; the three-turbine optimum falls [30, 23.8, 0]° → [18.6, 17.1, 0]° over TI 0.04 → 0.12, with gains shrinking 32.0 % → 2.9 %. Same logic in spacing: r_ij decays with distance, recovering Gori et al.'s observation that γ₁* decreases with turbine spacing [Gori et al., 2023], and in uncertainty (smearing of r_ij), recovering Quick et al. [2020].

**Downstream monotonicity.** A turbine's optimal yaw balances its own downstream beneficiaries; beneficiaries thin out down the chain, so optimal yaw decreases downstream, reproducing the row-monotone profiles of [King et al., 2021; Gori et al., 2023] and our 4×4 rows [30, 25.5, 16.5, 0]°. Where complements dominate, Topkis monotonicity [Topkis, 1998; Milgrom and Roberts, 1990] predicts yaw profiles move *together* (row synchrony); where substitutes dominate, they offset. Both regimes are visible in our sign matrices, and they map to the two standard solution patterns (column-synchronized vs row-decreasing) that practitioners impose as constraints [Gori et al., 2023]. Our analysis shows those constraints are structural, not merely regularizing.

## 8. Relation to prior work and limitations

**Relation to prior work.** (i) Submodularity was established for the *placement* problem (adding turbines to a farm) by Zhang et al. [2011]; our Theorem 1 shows the *control* problem (yaw) is instead generically supermodular in its lateral pairs, with substitution only along serial chains. The two problems have opposite interaction structures. (ii) Graph-based farm models [Starke et al., 2024] define binary interconnection matrices for dynamics; the sign matrix of §4.3 is a weighted, signed, objective-level object, computable from any differentiable model.

(iii) Bestehorn et al.'s strong NP-hardness [2025] applies to the general discretized problem with black-box objectives; our results show the physically standard model class restores structure (bounded interactions, decoupling at optima), so the practical difficulty observed in the field is not inherent to the physics. The same pattern holds in influence maximization, where general hardness coexists with submodular greedy guarantees [Nemhauser et al., 1978]. (iv) Game-theoretic farm control [Marden et al., 2013] designed utilities to make a potential game; the strategic complements/substitutes vocabulary we use is the economics one [Bulow et al., 1985]; our contribution is the structural theorem for the physical objective, not a mechanism design. (v) The empirical trends in [Gori et al., 2023; King et al., 2021; Quick et al., 2020] become corollaries of §7.

**Limitations.** Steady-state engineering wake models, not LES: the sign rules are proven for the model class and verified on GCH variants; their persistence in high-fidelity simulation is plausible (convex power law is flow-model-independent) but unverified. Interior optima only for Law 1. The decoupling mechanism is partially open (conjecture in §5). Loads and fatigue are out of scope. The novelty audit (Appendix C) is bounded by the searchable record as of 2026-08-30.

## 9. Experimental anchoring and a falsifiable measurement program

Recent reviewing practice rightly asks what a structural theory predicts that can be *measured*. This section does three things: it anchors the model class of §2 in the experiments that already exist (wind tunnel and field), it reports our robustness suite across the two experimentally calibrated model families shipped with FLORIS, and it specifies a pre-registered wind-tunnel protocol (Appendix D) whose three falsifiable predictions would refute the core claims of §3–§5 if the structure were an artifact of one parameterization.

**9.1 Anchoring the model class in existing experiments.** Every ingredient of Theorem 1 is a directly measured quantity. The yawed-wake deficit shape and its yaw deflection are wind-tunnel quantities [Bastankhah and Porté-Agel, 2016]; the cos^p self-power factor is a manufacturer-curve fit; and the first-order optimization consequences (5–25 % farm gains at partial wake overlap) are field-verified [Fleming et al., 2017, 2019, 2020; Simley et al., 2021] and surveyed in [Kheirabadi and Nagamune, 2019; Houck, 2022]. Wake-deflection control has also been exercised in closed loop on scaled wind-tunnel farms [Campagnolo et al., 2016], and first-order yaw optimization itself has a dedicated wind-tunnel dataset [Bastankhah and Porté-Agel, 2019], which is the experimental paradigm our protocol extends from first-order gains to second-order structure. FLORIS predictions have additionally been validated in closed loop under time-varying inflow [Doekemeijer et al., 2020]. What has *never* been measured, as far as our audit can establish, is the second-order structure: no wind-tunnel or field campaign has estimated mixed partials of farm power.

**9.2 Robustness across experimentally calibrated models.** We repeat the core measurements of §4–§5 on the cumulative-curl model ("cc"), whose velocity field was calibrated against LES [Bay et al., 2023], and the empirical-Gaussian model ("empirical_gauss"), whose parameters were calibrated against the Sedini field campaign [King et al., 2021]. The self-cost law is exact at the turbine level: the upstream turbine's own power follows cos^1.88(γ) (the FLORIS NREL-5MW exponent) to numerical precision, and the two-turbine farm response is the sum of that falling term and the rising wake-recovery term of the downstream turbine (Fig. 7b): the A/B two-channel competition in miniature, visible in every calibrated model family (Fig. 7a). The Jensen curve is excluded from the structural family because its power law is not of the cos^p form (model-dependence known from [Gori et al., 2023]). The headline Theorem-1 prediction holds in every one of them. The chain-pair sign flip reproduces in all three calibrated models: M₁₂ at the origin is +0.674 / +0.388 / +0.022 kW/deg² (gauss / cc / empirical_gauss) and turns negative at (20,20,20)° (−0.215 / −0.154 / −0.114) (Fig. 8).

The decoupling law holds in the strong-wake regime: the off-diagonal-to-diagonal ratio at the 3×3 optimum is 0.020 (gauss) and 0.116 (cc) versus 0.348 / 0.302 at the origin (Fig. 9a). The empirical-Gauss model sits in a different regime: its field-calibrated deficit at 5D is weak (baseline farm power 11 % above gauss), so its interactions are small everywhere (ratio 0.066 at the origin, 0.085 at the optimum): decoupling holds there trivially rather than emerging at the optimum. We report both regimes; the emergent drop is a strong-wake phenomenon, and the weak-wake regime is where the structure is uninformative rather than violated. Steering gains and decoupling persist across 6–10 m/s (gauss: +28.4 → +21.5 %, ratio at optima ≤ 0.15 throughout; cc: +6.0 → +22.6 % with the 6 m/s case again weak-wake; Fig. 9b), and the AEP version of the law holds over a 12-direction wind rose (+7.28 % AEP, Fig. 10). The LES-calibrated and field-calibrated models are the closest FLORIS comes to experiment without a new campaign, and the structure survives both.

**9.3 Power analysis: can the structure be measured?** The effect sizes are at the edge of field measurability, which explains why the structure has gone unnoticed. The mixed partial M₁₂ ≈ 0.67 kW/deg² on a 3.3 MW chain is 2·10⁻⁴ of farm power per deg²; a central-difference estimate with h = 5° needs to resolve ΔP = 2·M₁₂·h² ≈ 34 kW ≈ 1 % of the chain power. Ten-minute field means at TI 0.06 have standard deviations of 2–5 % of farm power [Fleming et al., 2017], so field data can confirm first-order gains (5–25 %, as already done) but cannot separate the sign of a 1 %-level curvature signal. 
A boundary-layer wind tunnel is different: model-turbine torque transducers resolve 0.1–0.5 % of turbine power at 180-s averages [Bastankhah and Porté-Agel, 2016], so the 34 kW-equivalent signal (≈1 % of chain power) is resolvable with 2–4σ separation at h = 5° and improves with h. The wind tunnel is therefore the right venue for the second-order predictions, the field for the first-order ones; we pre-register the former and note the latter.

**9.4 Three falsifiable predictions.** (i) **E1, the sign flip:** on a scaled 3-turbine chain, sign(M₁₂) > 0 at the origin and < 0 at (20,20,20)° (Fig. 1's phase boundary). (ii) **E2, decoupling:** at the measured optimum of a scaled 3×3 array, ‖M_off‖/‖diag M‖ ≤ 0.1 while ≥ 0.3 at the origin. (iii) **E3, ray monotonicity:** the farm-power response along t·γ* is monotone non-decreasing in t ∈ [0,1]. Instrumentation, blocking, statistics, and pre-specified falsification rules are in Appendix D. A refutation of any one prediction refutes that structural claim without touching the model-class theorems; the experiment is informative either way.

**9.5 Data and code availability.** All scripts, layouts, seeds, and result tables are archived with this paper (`exp_*.py`, `expcache/*.json`); the wind-tunnel protocol of Appendix D is released as a pre-registration template (OSF/Figshare deposit on acceptance). No experimental data are claimed in this paper; the claims of §9.2 are simulation claims about experimentally calibrated models, and are labeled as such.

## 10. Conclusion

We gave the wake-steering objective its missing second-order theory. Yaw decisions interact through two opposing channels: a complementarity channel through shared downstream turbines, and a substitution channel through downstream self-power factors. The sign of every pairwise interaction is decided by the wake DAG and the operating point. The theory explains, unifies, and predicts: why greedy sweeps are near-optimal (bounded interaction energy + decoupling at optima), why optimal profiles are row-synchronous and downstream-decreasing (lattice monotonicity), and why steering benefit shrinks with turbulence and spacing (single crossing in the recovery sensitivities). The sign matrix is a cheap, differentiable diagnostic that we expect to be useful for distributed control design, RL credit assignment, and farm co-design; these are the subjects of follow-up work.

---

## Appendix A. Proofs

*(A1) Theorem 1.* In the main text.

*(A2) Theorem 2.* Write f = P. For any x, y ∈ B := [0, γ̄]^N, twice-differentiability gives f(y) = f(x) + ∇f(x)ᵀΔ + ½ΔᵀH(ξ)Δ for Δ = y − x and ξ on the segment. Split H = diag(H) + H_off. Then ½ΔᵀHΔ ≤ ½ Σ_i d̄_i Δ_i² + ½ Σ_{i≠j} M̄_ij |Δ_i||Δ_j| ≤ ½ Σ_i d̄_i γ̄² + ½ Σ_{i≠j} M̄_ij γ̄². Take x = x^G, y = x*. It remains to control ∇f(x^G)ᵀ(x* − x^G). Greedy grid-optimality gives, for each i in sweep order, ∂f/∂γ_i(x^G) · (x*_i − x^G_i) ≤ d̄_i δ γ̄ when x*_i > x^G_i (moving right of a grid-optimal point can only improve the marginal by at most d̄_i δ, and the marginal at the grid-optimal point is ≤ 0 toward the right), and symmetrically toward the left; terms with x*_i = x^G_i vanish. Summing gives the linear bound Σ_i d̄_i δ γ̄. With δ → 0 (fine grids) the linear term vanishes and the diagonal term is O(δ²): the persistent gap is the interaction energy. ∎

*(A3) Single crossing (TI).* For fixed γ₂, ∂P/∂γ₁ = −p sin γ₁ cos^{p−1}γ₁ ṽ₁³ + 3 cos^p(γ₂) ṽ₂² r_12(γ₁; TI). As TI increases, r_12 decreases pointwise (kernel recovery-monotone in TI) and nothing else changes; hence ∂P/∂γ₁ decreases pointwise in TI, i.e., f has decreasing differences in (γ₁, TI). By the standard monotone-comparative-statics argument for univariate problems, argmax γ₁*(TI) is non-increasing in TI. The same argument applies with spacing or uncertainty as the parameter. ∎

## Appendix B. Reproduction protocol

Environment: FLORIS 4.6.6 (pip), Python 3.11, default_inputs.yaml (NREL 5MW, GCH: gauss velocity, gauss deflection, crespo_hernandez TI, sosfs). Conditions: 8 m/s, TI 0.06, wd 270°, yaw box [0°, 30°]. All scripts in `research/ws_submodularity/`:

- `floris_validate.py`: reproduces the four project validation numbers (+8.13 / +14.87 / +22.73 / +24.04 %, baseline 8095.15 kW).
- `exp_robustness2.py`: Hessians at optima vs baselines; phase maps; TI comparative statics; AEP case.
- `exp_experiments.py` / `exp_experiments2.py` / `exp_empgauss_supp.py` / `exp_traces_fix.py`: the §9 robustness suite (model curves, sign flips, wind-speed sweep, wind-rose AEP, DJS traces, certificate benchmark, 5×5 sign matrix, wall-time scaling).
- Figures: fig1_phasemap (Fig. 1), fig2_signmatrices (Fig. 2), fig3_decoupling (Fig. 3), fig4_ti_sweep (Fig. 4), fig5_y4x4 (Fig. 5), fig6_greedygaps (Fig. 6), fig7_model_curves (Fig. 7), fig8_flip_models (Fig. 8), fig9_ws_decoupling (Fig. 9), fig10_windrose (Fig. 10), fig11_djs_traces (Fig. 11), fig12_quasiconcavity (Fig. 12).
- `exp_experiments2.py`: 12-layout greedy-vs-SLSQP certificate benchmark (mean gap 0.103 %, max 0.477 %; seed 42).
- `analytic_3chain.py`: closed-form C − S decomposition for the three-turbine chain.

Finite differences: central, h = 2.5° (Hessians) or 5° (sign matrices); corner points with negative rotor velocities excluded (FLORIS warning).

## Appendix C. Novelty audit (search log, 2026-08-30)

Channels: web search (EN/CN), arXiv API (full-text `all:`), OpenAlex fulltext.search, Crossref, OEIS (where relevant). Queries and results:

1. `submodular wind farm optimization greedy approximation guarantee wake steering` → hits: Zhang et al. 2011 (placement submodularity, Renewable Energy) and followers. **Placement ≠ yaw control.** Positioned in §8.
2. `submodularity yaw angle turbine wake power function` → no yaw-submodularity literature.
3. arXiv `all:"submodular" AND all:"wind farm"` → **0 hits**. arXiv `all:"submodular" AND all:"yaw"` → **0 hits**.
4. OpenAlex fulltext `"submodular" AND "wake steering"` → 2 hits, both layout papers.
5. `风电场 偏航优化 次模 贪心 近似比` → nothing (Chinese review lists 遍历/梯度/遗传/数据驱动/对策论/神经网络 for yaw; no structural analysis).
6. `"supermodular" OR "strategic complements" wind turbine yaw` → no structural analysis; arXiv `all:"supermodular" AND all:"wind"` → **0 hits**.
7. `"strategic substitutes" wind farm` → economics literature only.
8. `Topkis / increasing differences / lattice + wind farm yaw` → nothing.
9. `"mixed partial" OR "interaction structure" wind farm power yaw` → only "not guaranteed convex" qualitative remarks.
10. `"Hessian" OR "second derivative" OR "diminishing returns" yaw wake steering` → derivative-computation papers (AD/adjoints for blades; Park & Law analytic gradients) with no second-order interaction analysis.
11. `"interaction matrix" wind farm yaw distributed` → Starke et al. 2024 binary interconnection matrix (dynamics), distinguished in §8.
12. `optimal yaw decreases turbulence intensity` → Gori 2023, King 2021, Quick 2020 empirical trends; our §7 supplies the mechanism. Cited, not claimed.
13. `"separable"/"decoupled"/"diagonal Hessian" optimum wake steering` → layout–control co-design separability (Larsen et al. 2020), different concept; no diagonal-Hessian-at-optimum result found.

Conclusion of audit: within the searchable record and the queries above, the interaction decomposition, sign matrix, decoupling law, and greedy bound are unclaimed. Statement is time-bounded and query-bounded by construction.


## References

1. Howland, M. F., Lele, S. K., Dabiri, J. O.: Wind farm power optimization through wake steering, PNAS 116(29), 14495–14500, 2019. doi:10.1073/pnas.1903680116
2. Gebraad, P. M. O., Teeuwisse, F. W., van Wingerden, J.-W., Fleming, P. A., Ruben, S. D., Marden, J. R., Pao, L. Y.: Wind plant power optimization through yaw control using a parametric wake model, Wind Energy 19(1), 95–114, 2016. doi:10.1002/we.1822
3. Fleming, P. A., et al.: Evaluating techniques for redirecting turbine wakes using SOWFA, Renewable Energy 70, 211–218, 2014. doi:10.1016/j.renene.2014.02.015
4. Fleming, P. A., Stanley, A. P. J., Bay, C., King, J., Simley, E., Doekemeijer, B., Mudafort, R.: Serial-refine method for fast wake-steering yaw optimization, J. Phys.: Conf. Ser. 2265, 032109, 2022. doi:10.1088/1742-6596/2265/3/032109
5. Stanley, A. P. J., Bay, C., Mudafort, R., Fleming, P.: Fast yaw optimization for wind plant wake steering using Boolean yaw angles, Wind Energ. Sci. 7, 741–757, 2022. doi:10.5194/wes-7-741-2022
6. Bestehorn, F., Bürgel, F., Kirches, C., Stiller, S., Tillmann, A. M.: Integer programming for optimal yaw control of wind farms, Wind Energ. Sci. 10, 1637–1662, 2025. doi:10.5194/wes-10-1637-2025
7. Starke, G. M., Meneveau, C., King, J. R., Gayme, D. F.: A dynamic model of wind turbine yaw for active farm control, Wind Energy, 2024. doi:10.1002/we.2884
8. King, J., Fleming, P., King, R., Martínez-Tossas, L. A., Bay, C. J., Mudafort, R., Simley, E.: Control-oriented model for secondary effects of wake steering, Wind Energ. Sci. 6, 701–714, 2021. doi:10.5194/wes-6-701-2021
9. Gori, F., Laizet, S., Wynn, A.: Sensitivity analysis of wake steering optimisation for wind farm power maximisation, Wind Energ. Sci. 8, 1425–1451, 2023. doi:10.5194/wes-8-1425-2023
10. Quick, J., et al.: Wake steering optimization under uncertainty, Wind Energ. Sci. 5, 413–426, 2020. doi:10.5194/wes-5-413-2020
11. Zhang, C., Hou, G., Wang, J.: A fast algorithm based on the submodular property for optimization of wind turbine positioning, Renewable Energy 36(11), 2956–2962, 2011. doi:10.1016/j.renene.2011.03.045
12. Park, J., Law, K. H.: Cooperative wind turbine control for maximizing wind farm power using sequential convex programming, Energy Conversion and Management 101, 295–316, 2015. doi:10.1016/j.enconman.2015.05.031
13. Gori, F., Wynn, A., Laizet, S.: Sensitivity of wind farm wake steering strategies to analytical wake models, TORQUE 2022 proceedings, 2022. doi:10.1201/9781003360773-75
14. Bastankhah, M., Porté-Agel, F.: Experimental and theoretical study of wind turbine wakes in yawed conditions, J. Fluid Mech. 806, 506–541, 2016. doi:10.1017/jfm.2016.595
15. Marden, J. R., Ruben, S. D., Pao, L. Y.: A model-free approach to wind farm control using game theoretic methods, IEEE Trans. Control Syst. Technol. 21(4), 1067–1078, 2013. doi:10.1109/TCST.2013.2257780
16. Martínez-Tossas, L. A., King, J., Quon, E., Bay, C. J., Mudafort, R., Hamilton, N., Howland, M. F., Fleming, P. A.: The curled wake model: a three-dimensional and extremely fast steady-state wake solver for wind plant flows, Wind Energ. Sci. 6, 555–570, 2021. doi:10.5194/wes-6-555-2021
17. Topkis, D. M.: Supermodularity and Complementarity, Princeton University Press, 1998.
18. Milgrom, P., Roberts, J.: Rationalizability, learning, and equilibrium in games with strategic complementarities, Econometrica 58(6), 1255–1277, 1990.
19. Bulow, J. I., Geanakoplos, J. D., Klemperer, P. D.: Multimarket oligopoly: strategic substitutes and complements, J. Political Economy 93(3), 488–511, 1985.
20. Nemhauser, G. L., Wolsey, L. A., Fisher, M. L.: An analysis of approximations for maximizing submodular set functions—I, Mathematical Programming 14, 265–294, 1978.
21. Pedersen, M. M., Larsen, G. C.: Integrated wind farm layout and control optimization, Wind Energ. Sci. 5, 1551–1567, 2020. doi:10.5194/wes-5-1551-2020
22. Fleming, P. A., Annoni, J., Shah, J. J., Wang, L., Ananthan, S., Zhang, Z., Hutchings, K., Wang, P., Chen, W., Chen, L.: Field test of wake steering at an offshore wind farm, Wind Energ. Sci. 2, 229–239, 2017. doi:10.5194/wes-2-229-2017
23. Fleming, P. A., King, J., Dykes, K., Simley, E., Roadman, J., Scholbrock, A., Murphy, P., Lundquist, J. K., Moriarty, P., Fleming, K., van Dam, J., Bay, C., Mudafort, R., Lopez, H., Skopek, J., Scott, M., Ryan, B., Guernsey, C., Brake, D.: Initial results from a field campaign of wake steering applied at a commercial wind farm – Part 1, Wind Energ. Sci. 4, 273–285, 2019. doi:10.5194/wes-4-273-2019
24. Fleming, P. A., King, J., Simley, E., Roadman, J., Scholbrock, A., Murphy, P., Lundquist, J. K., Moriarty, P., Fleming, K., van Dam, J., Bay, C., Mudafort, R., Jager, D., Skopek, J., Scott, M., Ryan, B., Guernsey, C., Brake, D.: Continued results from a field campaign of wake steering applied at a commercial wind farm – Part 2, Wind Energ. Sci. 5, 945–958, 2020. doi:10.5194/wes-5-945-2020
25. Simley, E., Fleming, P., Girard, N., Alloin, L., Godefroy, E., Duc, T.: Results from a wake-steering experiment at a commercial wind plant: investigating the wind speed dependence of wake-steering performance, Wind Energ. Sci. 6, 1427–1453, 2021. doi:10.5194/wes-6-1427-2021
26. Doekemeijer, B. M., van der Hoek, D., van Wingerden, J.-W.: Closed-loop model-based wind farm control using FLORIS under time-varying inflow conditions, Renewable Energy 156, 719–730, 2020. doi:10.1016/j.renene.2020.04.007
27. Bay, C. J., Fleming, P., Doekemeijer, B., King, J., Churchfield, M., Mudafort, R.: Addressing deep array effects and impacts to wake steering with the cumulative-curl wake model, Wind Energ. Sci. 8, 401–415, 2023. doi:10.5194/wes-8-401-2023
28. Kheirabadi, A. C., Nagamune, R.: A quantitative review of wind farm control with the objective of wind farm power maximization, J. Wind Eng. Ind. Aerodyn. 192, 45–73, 2019. doi:10.1016/j.jweia.2019.06.015
29. Campagnolo, F., Petrović, V., Schreiber, J., Nanos, E. M., Croce, A., Bottasso, C. L.: Wind tunnel testing of a closed-loop wake deflection controller for wind farm power maximization, J. Phys.: Conf. Ser. 753, 032006, 2016. doi:10.1088/1742-6596/753/3/032006
30. Houck, D. R.: Review of wake management techniques for wind turbines, Wind Energy 25(2), 195–220, 2022. doi:10.1002/we.2668
31. Bastankhah, M., Porté-Agel, F.: Wind farm power optimization via yaw angle control: a wind tunnel study, J. Renewable Sustainable Energy 11(2), 023301, 2019. doi:10.1063/1.5077038

---

## Appendix D. Experimental protocol (pre-registration template)

This appendix is a pre-registration template for the three falsifiable predictions of §9. It follows the reporting practice of the wake-steering field campaigns (paired blocks, per-condition baselines) [Fleming et al., 2017; Simley et al., 2021].

**Facility.** Boundary-layer wind tunnel, test section ≥ 10 m × 1.5 m × 1.5 m, active-grid or spires/roughness turbulence with hub-height TI adjustable over 0.04–0.15, mean speed 5–10 m s⁻¹. Model turbines: 0.12 m rotor diameter, three-bladed, individually instrumented with torque transducers and yaw actuators (resolution 0.5°, repeatability 0.1°). Array: geometrically scaled 3-turbine chain (5D spacing, 1:1050 of the NREL 5 MW) for E1, 3×3 array (5D × 3D) for E2–E3. Each turbine's yaw is set independently and held to within ±0.2°.

**Measurement.** Turbine power from torque × rotor speed, sampled at 100 Hz, block-averaged over 180 s per condition (wind-tunnel drift control: a yaw = 0 reference block is repeated after every third test block, and all powers are normalized by the nearest reference). Farm power = sum of per-turbine powers. No turbine operates below 20 % of its free-stream power in any reported condition (model validity boundary of §4).

**Design.** Full factorial over (γ₁, γ₂) ∈ {0, 5, 10, 15, 20, 25}° at γ₃ ∈ {0, 20}°, block-randomized, three replicates. Central differences for mixed partials use h = 5° with the 25-point stencil of §4. Primary analysis: two-sided t-test against the sign predictions; pre-specified α = 0.05, no optional stopping (blocks pre-generated, seed recorded).

**Predictions.** E1: sign(M₁₂) > 0 at (γ₁, γ₂, γ₃) = (0, 0, 20)° and sign(M₁₂) < 0 at (20, 20, 20)°, with the sign crossing occurring between them; E2: ‖M_off‖/‖diag M‖ at the measured optimum ≤ 0.1 while ≥ 0.3 at the origin; E3: the farm-power response along t·γ* is monotone non-decreasing in t ∈ [0, 1].

**Falsification rules.** E1 is refuted if the measured sign of M₁₂ at either anchor point is opposite to the prediction with p < 0.05 (one-sided). E2 is refuted if the optimum's off-diagonal ratio exceeds 0.2. E3 is refuted if any measured interior step along the ray is decreasing by more than 2σ of the measurement noise. A refutation of any prediction refutes the corresponding structural claim of §3–§5, not the others; the model-class theorems are unaffected but their empirical relevance would be in question, which is the point of running the experiment.
