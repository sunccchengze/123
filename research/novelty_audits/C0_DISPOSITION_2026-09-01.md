# C0 disposition update — broad route closed after adverse-source review

**Date:** 2026-09-01 (Asia/Shanghai)
**Supersedes:** the provisional `UNRESOLVED` status of C0 in
`C0_ABSTENTION_RISK_CONTROL_NOVELTY_AUDIT_2026-09-01.md`.
**Decision:** **C0, as a broad “calibrated abstention / risk-limiting dynamic
wake-steering” research route, is CLOSED. It must not be developed or described
as a new high-impact method.**

This update records an expected but important falsification. It preserves the
initial formulation rather than silently revising it after a close predecessor
appeared.

---

## 1. Decisive new antecedents

### D1 — Direct wind-control overlap

**Becker & van Wingerden (2026)**, *Risk-averse wake steering optimization for
energy and power maximization under uncertain wind direction changes*, *Journal
of Physics: Conference Series* 3224, 032124,
[doi:10.1088/1742-6596/3224/3/032124](https://doi.org/10.1088/1742-6596/3224/3/032124).

The Crossref record was read on 2026-09-01. Its abstract says that the authors:

- use a computationally cheap **dynamic wake model** and synthetic time-varying
  wind-direction series;
- obtain expected values and uncertainty for power and energy;
- explore **four cost functions** to derive robust setpoints; and
- report an alternative cost function that **avoids losses**, with similar but
  smaller gains at substantially lower yaw-angle investment.

This is an unambiguous wind-specific predecessor for C0's broad motivation:
dynamic operation under uncertain wind direction, risk-averse setpoint choice,
and avoidance of loss. C0 cannot claim that a decision rule intended to refrain
from harmful yaw is a new wind-control problem or method.

### D2 — Generic statistical mechanism overlap

**Xu, Guo & Wei (2025/2026)**, *Selective Conformal Risk Control*,
[arXiv:2512.12844v2](https://arxiv.org/abs/2512.12844),
[doi:10.48550/arXiv.2512.12844](https://doi.org/10.48550/arXiv.2512.12844).

The arXiv primary page and HTML text were read on 2026-09-01. It explicitly
combines selective classification (abstention on low-confidence inputs) with
conformal risk control, gives a transductive exchangeability result and an
inductive PAC-style calibration variant. It is a preprint, not treated here as
peer-reviewed wind-control validation, but it directly prevents any claim that
C0 invented the general abstention-plus-risk-control mechanism or its generic
coverage/risk theory.

### D3 — Earlier operational overlap that makes the gap narrower still

- **Rott et al. (2018)**, *Robust active wake control in consideration of wind
  direction variability and uncertainty*, WES 3, 869–882,
  [doi:10.5194/wes-3-869-2018](https://doi.org/10.5194/wes-3-869-2018): dynamic
  wind-direction changes and measurement inaccuracy can make intended power
  gains fail; the paper introduces a robust yaw-control methodology using real
  wind-direction time series.
- **Kanev (2020)**, *Dynamic wake steering and its impact on wind farm power
  production and yaw actuator duty*, *Renewable Energy* 146, 9–15,
  [doi:10.1016/j.renene.2019.06.122](https://doi.org/10.1016/j.renene.2019.06.122):
  dynamic wake steering and yaw-actuator duty are already a named research
  object.
- **Hodgson & Andersen (2026)**,
  [doi:10.5194/wes-11-2173-2026](https://doi.org/10.5194/wes-11-2173-2026):
  explicitly note that operational yaw may need to avoid instantaneous power
  loss, not merely optimize mean gain. This is a strong motivation, not an
  unclaimed blank slate.

Together these sources close the shortcut of combining familiar words—dynamic,
risk-averse, no-loss, abstention, calibrated, robust—and calling the combination
a contribution.

---

## 2. What is closed, precisely

| Proposed C0 element | disposition | reason |
|---|---|---|
| Dynamic yaw control under wind-direction uncertainty | **closed** | Rott, Kanev, Simley, Becker, Starke, and OFF-related literature cover it. |
| Risk-averse/loss-avoiding wake-steering setpoints | **closed** | Becker & van Wingerden (2026) is direct. |
| “Do not steer when uncertain” as a generic control intuition | **closed** | It follows from the above robust/risk-averse literature; it is not an independent novelty. |
| Conformal risk control plus selective abstention as a new statistical method | **closed** | Xu et al. (2025/2026) is a direct generic methodological predecessor. |
| Static-FLORIS demonstration of any of the above | **closed** | It would be below the evidence level of the closest work and cannot demonstrate causal/deployment safety. |
| A future wind-specific causal, sequential, non-exchangeable action-assignment theorem plus independently tested intervention protocol | **not formulated; not a candidate** | This phrase only identifies a possible direction for future hostile searching. There is no precise contribution, proof, data, or evidence of novelty. |

The last line is intentionally **not** a narrowed C0 claim. The project must not
move it forward merely because it sounds more specialized.

---

## 3. Search trace that triggered the update

| date | channel/query | result | audit consequence |
|---|---|---|---|
| 2026-09-01 | Crossref title query for `Risk-averse wake steering optimization for energy and power maximization under uncertain wind direction changes` | DOI-level record and full abstract for Becker & van Wingerden, 2026 | Direct wind-control predecessor; broad C0 G2 fails. |
| 2026-09-01 | OpenAlex exact-title query | Dataset linked to that named publication was located, corroborating that this is a real, recent research object; source metadata does not itself prove method details | Supporting provenance only; Crossref abstract remains the evidence for the overlap. |
| 2026-09-01 | Web/primary arXiv: `selective conformal risk control` | Xu et al. v2 page gives abstention + conformal risk-control framework and stated guarantees | Generic core mechanism is unavailable as an originality claim. |
| 2026-09-01 | `wake steering risk-averse`, `wake steering CVaR`, `risk control wake steering`, `safe reinforcement learning wind farm yaw`, `counterfactual wake steering`, `safety filter wind farm control` | Results showed many adjacent robust/dynamic/controller/field lines; no finite search can rule out further direct work | Confirms that a keyword composition is especially unsafe; no residual is promoted. |

---

## 4. Consequences for the project

1. The initial C0 audit remains useful as a record of the intended question, but
   its status is no longer `UNRESOLVED`: it is **CLOSED AS FORMULATED**.
2. `RESEARCH_IMPACT_ASSESSMENT_2026-09-01.md`, `IDEATION.md`, `SUMMARY.md`, and
   the repository README have been amended to prevent an obsolete C0
   recommendation from being selected later.
3. No new manuscript, abstract, method figure, or performance claim may be
   generated from C0.
4. A genuinely new project must begin from a separate consequence-and-novelty
   audit, not a cosmetic renaming of C0. It must first establish a nontrivial
   difference from D1–D3 and all direct sources discovered in its later search.
5. The correct present classification is: **P1/P2/P3 archive only; C0 closed;
   no live high-impact paper candidate in this repository.**

This is a better research outcome than leaving an attractive but covered idea in
the register. A high-impact contribution needs a new scientific capability,
not a relabelled combination of existing robust control and generic calibration
methods.
