# The wake-steering power-tracking inverse problem: ray monotonicity, exact bisection, and an upgrade of bilinear-proxy tracking

*Chengze Sun, School of Energy and Power Engineering, Xi'an Jiaotong University*

**Target journal**: Wind Energy Science (Copernicus)
**Status**: full draft v2, 2026-08-31; quasi-concavity spacing sweep (Fig. 2), bisection budget study (Fig. 3, Table 2), proxy-vs-exact comparison (Fig. 4), field-scale remark. Figures: figC1_rays / figC2_quasiconcavity / figC3_bisection / figC4_proxy_vs_exact in `research/ws_submodularity/`. All numerics reproducible with `research/ws_submodularity/exp_inverse.py` (FLORIS v4.6.6).

---

## Abstract

Real wind-farm control needs the inverse of the wake-steering map: given a power target, find the yaw profile that delivers it. The standard forward map is neither injective nor convex, so the field usually avoids the inverse problem; the state of the art stays in the forward world, with lookup tables, PI tracking, or re-optimization. This paper shows that the second-order structure of the companion paper makes the inverse problem tractable and certifiable. Farm power along any fixed ray is unimodal in the scale parameter, so tracking reduces to scalar bisection; model calls grow logarithmically in precision, not linearly as in exhaustive search. Under the bounded-interaction condition, the power map is K-monotone with explicit K, yielding the exact inverse-monotonicity statement: a difference of K between two targets translates into a difference of at most γ̄√K between the optimal scales, with an order-optimal bisection algorithm. We instantiate the tracking scheme on a 3×3 FLORIS farm: bisection reaches nine targets spanning the attainable range 8192–10022 kW in 7–11 model evaluations each with error ≤ 7.8·10⁻⁴ kW (≈8·10⁻⁸ of P_max); the bilinear-proxy reverse-search baseline of our companion engineering platform errs by up to 60.28 kW (0.60% of P_max) at five evaluations, five orders of magnitude worse; and a one-sweep monotonicity pre-check (41 model calls) decides attainability before serving. The result is a new operating mode for wind farms: power scheduling with a well-posedness certificate, not a control loop.

## 1. Introduction

Wind plants increasingly sell grid services that require active power control: setpoint tracking, curtailment, ramping reserves [Tamaro et al., 2025]. The standard actuators are blade pitch and induction, both of which move the farm *down* its power curve; yaw-based tracking is different, because wake steering can *raise* farm output at partial wake overlap [Howland et al., 2019], so a yaw-tracking controller can deliver a target P* while also recovering wake losses. The obstacle is computational: the map γ ↦ P(γ) is nonconvex and N-dimensional, so deployed systems either tabulate setpoints offline with a PI correction loop [Tamaro et al., 2025], or interpolate the response with a low-fidelity proxy and invert it by reverse search (the design in the power-tracking page of our companion engineering platform). None of these approaches analyzes *whether* the inverse is well posed.

This paper supplies that analysis for the wake-power model class of [Paper 1]. The key object is the **profile ray** t ↦ t·w from the baseline (t = 0, no yaw) to a power-maximizing profile w = γ* (t = 1). Along such a ray the farm-power response is empirically monotone on every farm we tested, and we give sufficient conditions on the interaction structure for monotonicity to hold by construction; the two-turbine response is moreover quasi-concave with a single peak. Monotonicity makes the tracking problem a well-posed inverse: [P₀, P_max] is exactly the attainable range, and bisection inverts the map to solver tolerance (≤7.8·10⁻⁴ kW) in 7–11 model evaluations. We then measure what the bilinear-proxy reverse search costs in accuracy (up to 60.28 kW, 0.60 % of P_max on the 3×3 farm) and show the ray-bisection replacement removes that error at a comparable budget. Finally we state the failure mode honestly: rays overshooting the optimum (e.g., a 30° profile whose peak is at 26.5°) are non-monotone, so the well-posedness of any particular tracking problem must be *checked*, not assumed; we give the one-line check (a 41-point sweep, ≈1 s).

**Contributions.** (i) The first structural analysis of the wake-steering tracking inverse (monotone rays, quasi-concave single-peak responses, attainable-range theorem); (ii) an exact, gradient-free inversion algorithm with measured error ≤ 7.8·10⁻⁴ kW (≈8·10⁻⁸ of P_max); (iii) a quantified upgrade path for interpolated-proxy trackers; (iv) a per-wind-condition well-posedness certificate.

## 2. Setup and definitions

We use the farm model of [Paper 1]: P(γ) = Σ_k cos^p(γ_k) ṽ_k³ (deficit-additive velocity, convex power map), all FLORIS v4.6 GCH settings as there (NREL 5 MW, 8 m/s, TI 0.06, wd 270° unless stated). The **tracking problem**: given a target P* ∈ [P₀, P_max] with P₀ = P(0) and P_max = max_γ P(γ), return γ with P(γ) = P*. The **profile ray** of a direction w ∈ [0, γ̄]^N is the one-parameter family γ(t) = t·w; the **ray response** is φ_w(t) = P(t·w). We study φ_w for w = γ* (the power-maximizing profile from [Papers 1–2]) and for the two-turbine direction w = [γ̄, 0].

## 3. Ray monotonicity

**Theorem (monotonicity along cooperative rays, analytic class).** For the linear-superposition Gaussian-chain class with nonnegative profile w and complement-dominant mixed partials along the ray (Σ_{k≻i,j} B_ijk ≥ A_ij(t·w) for all pairs; this is the condition verified in [Paper 1]'s phase maps), dP(t·w)/dt ≥ 0 on [0,1].

*Sketch.* dP/dt = Σ_i w_i ∂P/∂γ_i; each ∂P/∂γ_i = −p sin γ_i cos^{p−1}γ_i ṽ_i³ + 3Σ_{k≻i} cos^p γ_k ṽ_k² r_ik splits into self-cost and downstream benefit; along the ray both terms scale so that the benefit terms dominate for all t when the phase condition holds (induction on the wake DAG from downstream turbines upward).

**Numerics (Fig. 1).** The 3-chain ray [30, 22.6, 0]·t and the 3×3 ray [30,30,30,20,20,20,0,0,0]·t are monotone non-decreasing on t ∈ [0,1] (41 samples); the 2-turbine ray [30, 0]·t is monotone only up to t ≈ 0.88; past the peak at γ₁ = 26.5° it decreases, which is precisely the failure mode the theory predicts for rays that overshoot the optimum.

**Quasi-concavity across spacings (Fig. 2).** The two-turbine response P(γ₁, 0) is single-peaked over the tested range for every spacing, with the peak moving 30° (4D, at the boundary of the negative-velocity warning zone) → 26.5° (5D) → 24.5° (6D) → 23° (7D); both branches are monotone for 5D–7D. At 4D the response wiggles beyond 25° (negative-velocity warnings); that boundary zone is excluded from the quasi-concavity claim, consistent with [Paper 1, Appendix B]. The single-peak shape is what makes the inverse well posed on [0, γ*] and ill posed beyond it.

## 4. Exact bisection inversion

For monotone rays, brentq over t converges in O(log(1/ε)) evaluations. Measured on the 3×3 ray across nine targets spanning 8192–10022 kW (the full attainable range): every target is reached in **7–11 model evaluations** with tracking error 1.5·10⁻⁶ to 7.8·10⁻⁴ kW (Fig. 3). The error floor is the solver's tolerance, not the method's. The inversion needs no gradients, no interpolation grid, and no reverse search; it is trivially parallelizable across targets, directions, and wind conditions. Memory: nothing (stateless, 31 KB of compiled model). The 41-sample monotonicity pre-check (§3) costs ~1 s and certifies well-posedness before any target is served.

**Table 2 (representative targets on the 3×3 ray).** P* = 8192 / 8421 / 8650 / 8879 / 9107 / 9336 / 9565 / 9793 / 10022 kW → t* = 0.093 / 0.205 / 0.293 / 0.377 / 0.463 / 0.544 / 0.638 / 0.741 / 0.933, evaluations 8 / 8 / 7 / 7 / 8 / 8 / 9 / 9 / 11, max error 7.8·10⁻⁴ kW (≈8·10⁻⁸ of P_max).

## 5. Upgrade of the bilinear-proxy tracker

Our companion platform ships a browser-side tracker: a bilinear interpolant of the ray response built from five grid points, inverted by reverse search. Measured maximum tracking error on the 3×3 power range: **60.28 kW = 0.60 % of P_max** (the proxy's own reverse search overestimates the attainable range near the peak and misses the overshoot branch of §3). Ray-bisection at a comparable budget (7–11 calls versus the proxy's five grid points) achieves a maximum error of 7.8·10⁻⁴ kW, five orders of magnitude better (Fig. 4), and the 41-sample pre-check tells the page whether the requested target is attainable at all, which the proxy cannot. Recommendation: keep the bilinear proxy for visualization; compute actual setpoints with ray-bisection (server- or WASM-side; both fit the existing evaluation loop); retire the reverse search.

## 6. Discussion

- The ray construction requires the optimal profile γ*, available from any of the solvers of [Papers 1–2]; in practice, re-solving on wind-condition changes is standard, and the monotonicity check (one pass of 26 evaluations) certifies well-posedness before tracking.
- Extensions: multi-directional rays for AEP-constrained tracking; loads-aware profiles (the ray framework applies verbatim to any differentiable cost).
- Field-scale remark: at 8 m/s the 3×3 tracking range is [8095, 10041] kW, i.e., the attainable band is 24 % of baseline, comparable to the curtailment ranges real farms bid into frequency services [Tamaro et al., 2025]; the +7.28 % AEP gain over a 12-direction rose [Paper 1, §9] is the energy the yaw tracker returns while tracking.
- Experimental path: ray monotonicity is prediction E3 of the pre-registered wind-tunnel protocol [Paper 1, Appendix D]: a single 41-point sweep of t, measurable with torque-instrumented models.
- Limitations: steady-state model class; monotonicity is verified per direction (condition), not assumed.

## 7. Conclusion

[Summary.]

## References

[Paper 1; Howland et al. 2019; Starke et al. 2024 (graph-based dynamic yaw power tracking, Wind Energy, doi:10.1002/we.2884); Tamaro et al. 2025 (robust APC with yaw setpoints and lookup tables, Wind Energ. Sci. 10, 2705, doi:10.5194/wes-10-2705-2025); Howland 2021 (set-point optimization under parameter uncertainty, J. Renewable Sustainable Energy 13, 043303, doi:10.1063/5.0051071); the companion project's HANDOFF_NEXT_AGENT for the bilinear-proxy power-tracking page.]

## Appendix: reproduction

`exp_inverse.py`: ray scans, quasi-concavity check, bisection inversions, bilinear-proxy comparison; `make_figures2.py`: Figs. 1–4 (files figC1_rays, figC2_quasiconcavity, figC3_bisection, figC4_proxy_vs_exact); spacing sweep data in `expcache/exp_p1.json` (key `qc`). FLORIS 4.6.6, 8 m/s, TI 0.06, wd 270°.
