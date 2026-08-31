# Theory: The interaction structure of wake-steering objectives

> 核心发现：风电场偏航功率目标 P(γ) 的混合偏导 ∂²P/∂γi∂γj 分解为"互补通道 B_ij"与"替代通道 A_ij"之差，符号由尾流作用图拓扑与参数域共同决定；最优点处相互作用近似解耦。

## 1. Model class (deficit-additive wake-power maps)

- N turbines at positions x_i; yaw vector γ ∈ [0, γ̄]^N.
- Downstream relation i ≺ j: turbine i's wake affects j (a DAG along the mean flow).
- Effective normalized velocity at j: ṽ_j(γ) = 1 − Σ_{i≺j} w_ij(γ_i) ≥ 0  (linear superposition; for SOSFS: ṽ_j = √(1 − Σ w_ij²)).
- Wake kernels w_ij: C² in γ_i on (0,γ̄), **recovery monotone**: ∂w_ij/∂γ_i ≤ 0 (yawing upstream never deepens the deficit at j), with r_ij(γ_i) := −∂w_ij/∂γ_i ≥ 0.
- Power: P(γ) = Σ_j cos^p(γ_j) · ṽ_j(γ)³,  p > 0 (FLORIS default p = pP = 1.88).

All FLORIS v4 GCH-family models fall in this class up to superposition rule (sosfs) and secondary-steering corrections (which preserve sign structure: see Remark 1).

## 2. Theorem 1 (interaction decomposition)

For i ≠ j, M_ij(γ) := ∂²P/∂γi∂γj = B_ij(γ) − A_ij(γ), where

- **complementarity channel** (via turbines k downstream of both i and j):
  B_ij = Σ_{k ≻ i,j} cos^p(γ_k) · β_k(i,j) ≥ 0,
  β_k = 6 ṽ_k r_ik r_jk (linear superposition),  β_k = 3 w_ik w_jk r_ik r_jk / ṽ_k (SOSFS).
- **substitution channel** (only when j ≻ i, acting through j's own power factor):
  A_ij = 3p sin(γ_j) cos^{p−1}(γ_j) ṽ_j² r_ij ≥ 0  (linear),
  A_ij = 3p sin(γ_j) cos^{p−1}(γ_j) ṽ_j w_ij r_ij (SOSFS).
  A_ij = 0 for γ_j = 0.

**Proof (linear superposition; SOSFS analogous).** Write P = Σ_k p_k ṽ_k³, p_k := cos^p(γ_k). For k ≻ i,j, ∂ṽ_k/∂γ_i = r_ik, ∂ṽ_k/∂γ_j = r_jk, ∂²ṽ_k/∂γi∂γj = 0, giving the B term via ∂²(p_k ṽ_k³) = p_k·6ṽ_k·r_ik r_jk. For k = j (j ≻ i): ∂²(p_j ṽ_j³)/∂γi∂γj = p_j′ · 3ṽ_j² r_ij = −3p sinγ_j cos^{p−1}γ_j ṽ_j² r_ij = −A_ij. All other k give zero. ∎

**Structural consequences (sign rules):**

- (S1) *No shared downstream, no order relation* ⇒ M_ij = 0 (turbines independent).
- (S2) *Pure chain pair* (j ≻ i, no common downstream) ⇒ M_ij = −A_ij ≤ 0: **strategic substitutes**; strict for γ_j > 0 and r_ij > 0.
- (S3) *Lateral pair with shared downstream* (neither downstream of the other, ∃k ≻ i,j) ⇒ M_ij = B_ij ≥ 0: **strategic complements**.
- (S4) *General pair*: sign(M_ij) = sign(B_ij − A_ij); the zero set B_ij = A_ij is the **complement–substitute phase boundary**, which moves with spacing, turbulence, and the yaw state γ.

**Corollary 1 (two turbines).** For N = 2 serial: M_12 = −A_12 ≤ 0 — the marginal benefit of yawing turbine 1 is a decreasing function of γ₂: **diminishing returns**, i.e. submodularity on the box, holds exactly for the two-turbine problem (consistent with FLORIS numerics, Table EXP A).

**Corollary 2 (phase flip, 3-chain).** M_12 = 6 cos^p(γ₃) ṽ₃ r_13 r_23 − 3p sinγ₂ cos^{p−1}γ₂ ṽ₂² r_12. Complementarity iff
2 cos^p(γ₃) ṽ₃ r_13 r_23 > p sinγ₂ cos^{p−1}γ₂ ṽ₂² r_12.
Since r_13, r_23 decay with streamwise distance while r_12 does not, **complementarity favors short spacing and low turbulence; substitution dominates for long spacing, high turbulence, and large γ₂.** (Matches FLORIS phase map.)

**Corollary 3 (AEP invariance).** AEP(γ) = Σ_ω q_ω P_ω(γ), q_ω ≥ 0 ⇒ M^AEP_ij = Σ_ω q_ω M^ω_ij ⇒ the decomposition and sign rules carry over to energy-objectives (wind-rose mixtures, Weibull integrals). Numerically confirmed: AEP Hessian decouples at the AEP-optimum (od/diag 0.068 vs 0.966 at baseline).

**Remark 1 (robustness).** Any twice-differentiable deficit-additive model with convex power map φ and recovery-monotone kernels yields B_ij ≥ 0 via φ″ ≥ 0; the substitution channel A_ij ≥ 0 needs only p′_j(γ_j) ≤ 0 (power factor decreasing in own yaw). Hence the sign rules (S1)–(S4) hold for the whole model family, not a single parameterization.

## 3. Law 1 (decoupling at the optimum) — empirical + stationarity identity

**Observation (FLORIS v4.6 GCH, 8 m/s, TI 0.06, wd 270°):** at the SLSQP maximizer γ*, the Hessian is nearly diagonal: ‖M_off‖/‖diag‖ = 0.023 (3×3), 0.022 (wd 300°), 0.030 (3-chain), 0.174 (random 6-turbine with weak steering benefit), vs 0.27–0.97 at generic points. **The optimum sits at a point of (near-)maximal interactional decoupling.**

**Stationarity identity (3-chain, linear superposition):** at an interior maximizer, ∂P/∂γ₂ = 0 gives
p sinγ₂* cos^{p−1}γ₂* = 3 cos^p(γ₃*) ṽ₃² r_23 / ṽ₂³,
hence M_12(γ*) = 3 cos^p(γ₃*) ṽ₃ r_23 · ( 2 r_13 − 3 ṽ₃ r_12 / ṽ₂ ).
Interpretation: at the optimum the two channels are tied by the stationarity of the middle turbine; the residual interaction is set by the single factor (2r_13 − 3ṽ₃ r_12/ṽ₂), which is small in the operating regime (far-wake, near-recovered ṽ₃ ≈ ṽ₂, small r_13 vs r_12).

**Consequences.** (i) Explains why sequential upstream→downstream greedy / Boolean (Stanley 2022) / serial-refine (Fleming 2022) recover ≥99.5% of the optimum in practice; (ii) near γ* the problem is locally separable ⇒ parallel per-turbine 1-D line searches converge in very few sweeps (Paper 2 algorithm); (iii) second-order methods can use a diagonal (Jacobi) preconditioner.

## 4. Theorem 2 (greedy gap via bounded interactions)

Let f = P on the box B = [0,γ̄]^N, twice differentiable, and let x^G be the output of the upstream→downstream coordinate-greedy sweep on the grid G = {0, δ, 2δ, …, γ̄}. Then
f(x*) − f(x^G) ≤ (1/2) Σ_{i≠j} M̄_ij γ̄² + (1/2) Σ_i d̄_i (δ/2)²,
where M̄_ij = sup_{B} |M_ij| and d̄_i = sup_B |∂²P/∂γ_i²|·1{grid truncation}.

*Sketch.* Taylor with integral remainder: f(x*) − f(x^G) = ∇f(x^G)·(x*−x^G) + (1/2)(Δ)ᵀH(ξ)Δ. Greedy grid-optimality gives per-coordinate marginals ≤ O(d̄_i δ²): the linear term is bounded by Σ_i d̄_i δ γ̄... (refined in the paper); the quadratic term splits into diagonal (bounded by d̄_i δ²/8 at grid points along the sweep... ) and off-diagonal Σ_{i≠j} M̄_ij Δ_i Δ_j ≤ Σ M̄_ij γ̄². ∎

**Empirical tightness (v2 benchmark, seed 42).** 12 random layouts (N=6–9, wd 240–300°): Boolean greedy (5° grid, correct streamwise order) vs multi-start SLSQP — mean gap 0.103 %, max 0.477 % (one case −0.009 %, greedy above SLSQP). Certificate (sampled M̄_ij): bounds 0.12–7.05 % of P, always above the measured gap. Supersedes the earlier 0.019 % figure, which used a weaker reference; the claim survives.

## 5. Proposition (monotone comparative statics — mechanism of known trends)

For the two-turbine case, ∂P/∂γ₁ = −p sinγ₁ cos^{p−1}γ₁ ṽ₁³ + 3 cos^p(γ₂) ṽ₂² r_12(γ₁).
This has the **single-crossing property** in (γ₁; TI, spacing): r_12 decreases pointwise in TI and spacing (wakes recover faster / farther), while the self-cost term is independent of them ⇒ the argmax γ₁* is monotone non-increasing in TI and in spacing. Higher-order chains inherit the mechanism recursively (each turbine's optimum balances its own downstream benefits).

This provides the **structural mechanism** for the empirical trends reported by Wynn et al. (WES 2023, γ₁* decreasing with spacing), King et al. (2021, row-monotone decreasing profiles via secondary steering), and Quick et al. (2020, uncertainty shrinks γ*). The lattice-theoretic reading (Topkis/Milgrom–Roberts): where B dominates, yaw profiles move together (complements); where A dominates, they substitute — matching the observed row-synchronous and row-monotone patterns.

## 6. Open items / falsifiability

- Law 1 holds for all tested GCH cases; to be probed on larger farms (Horns Rev) and Jensen/multizone models (robustness table in paper).
- The exact conditions for M(γ*) ≡ 0 (true decoupling) remain open; conjectured sufficient condition: symmetric kernels + small-deficit regime.
- Phase boundary B=A: closed form for the Gaussian kernel family in progress (sympy), to be compared against FLORIS maps.
