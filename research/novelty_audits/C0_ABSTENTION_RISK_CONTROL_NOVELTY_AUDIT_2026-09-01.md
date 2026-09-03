# C0 新颖性审计：可弃权、风险受限的动态 wake-steering

**日期：** 2026-09-01（Asia/Shanghai）
**当前状态：** `CLOSED AS FORMULATED — not a candidate`
**状态更新：** 本档案的初始 `UNRESOLVED` 状态已被同日后续的直接先例审查取代。决定性证据、查询轨迹和精确处置见 [`C0_DISPOSITION_2026-09-01.md`](C0_DISPOSITION_2026-09-01.md)。Becker and van Wingerden (2026) 已直接覆盖动态、风险规避、避免损失的 wake-steering setpoints；Xu et al. (2025/2026) 已覆盖通用的选择性弃权 + conformal risk control 机制。因此本文件后续的“候选”“下一轮”表述只保留为**审计历史**，不可执行为研究计划。
**审计规则：** 检索未命中不是“不存在先例”的证据；在完整方法固定及近邻原文
精读前，禁止使用“首创”“first”“novel”“安全保证”“因果控制”或“可投稿”
描述 C0。

---

## 0. 被审计的精确对象

C0 不是泛称的鲁棒 wake steering。暂定对象是一个完整组合：

> 在有时变入流、yaw 执行器约束和模型误差的 wind-farm control 中，使用预先固定、
> 经独立数据校准的风险门；只有当候选动作相对于 baseline 的净功率收益下界为正，
> 且载荷/约束风险上界可接受时才实施动作，否则明确保持 baseline。其评估须含
> 受控反事实或同等可识别设计、动态高保真盲测和强基线对照。

定义越不精确，越无法审计新颖性。定义一旦改变，必须重开本审计。

**目前没有方法、证明、代码、数据或结果。** 本文件只保存问题选择和反证优先的
检索记录。

---

## 1. 近邻先例：已确认，不能回避

| ID | 来源及核验方式 | 已确认内容 | 对 C0 的约束 |
|---|---|---|---|
| A1 | Quick et al., *Wake steering optimization under uncertainty*，WES 5 (2020)，Crossref 原始元数据/摘要，[DOI](https://doi.org/10.5194/wes-5-413-2020) | 将风向、风速、TI、切变与 yaw 等不确定性纳入 OUU，比较二机与 11 机案例，目标为期望能量。 | 不能把“考虑不确定性”“更小 yaw”或“降低风险”称为新。必须区分期望值优化和真实校准的部署门。 |
| A2 | Simley, Fleming & King, *Design and analysis of a wake steering controller with wind direction variability*，WES 5 (2020)，Crossref 原始元数据/摘要，[DOI](https://doi.org/10.5194/wes-5-451-2020) | 考虑动态风向和 yaw 定位不确定性，并用现实 yaw-offset controller 仿真。 | 不能把风向预测/变化、动态 yaw LUT 或不确定输入当作创新。 |
| A3 | Starke et al., *A dynamic model of wind turbine yaw for active farm control*，*Wind Energy* 27 (2024)，Crossref 原始元数据/摘要，[DOI](https://doi.org/10.1002/we.2884) | 图式动态 yaw 模型，结合实时入流估计，静态/动态 LES 验证，并进入最优控制回路。 | 动态建模、图结构、LES 或闭环措辞本身没有新颖性。 |
| A4 | Becker et al., *A dynamic open-source model to investigate wake dynamics in response to wind farm flow control strategies*，WES 10 (2025)，Crossref 原始元数据/摘要，[DOI](https://doi.org/10.5194/wes-10-1055-2025) | 开源 OFF 框架；10 机案例、基于现场数据的 24 h 风向序列，子段与 LES 比较。 | 任何动态工程模型比较必须至少对齐这种验证层级和公开性。 |
| A5 | Tamaro et al., *A robust active power control algorithm to maximize wind farm power tracking margins in waked conditions*，WES 10 (2025)，[DOI](https://doi.org/10.5194/wes-10-2705-2025)；Tamaro et al., *Scaled testing of maximum-reserve active power control*，WES 11 (2026)，Crossref 原始元数据/摘要，[DOI](https://doi.org/10.5194/wes-11-1607-2026) | reserve APC 联合 yaw 与 induction；2026 版本有动态风向风洞、实时控制、三个文献基线和疲劳影响。 | 不得重新包装 power tracking、reserve、yaw/induction 组合、动态风洞或“鲁棒 APC”。 |
| A6 | Hodgson & Andersen, *Wake steering under inflow wind direction uncertainty: an LES study*，WES 11 (2026)，Crossref 原始元数据/摘要，[DOI](https://doi.org/10.5194/wes-11-2173-2026) | 四机列 LES；文中研究范围内，约 4° 均值风向误差可将预测收益变成实际损失。 | 这是问题动机，不是 C0 的新结果；不能只复现敏感性图。 |
| A7 | Fleming et al., *Initial results from a field campaign... Part 1*，WES 4 (2019)，[DOI](https://doi.org/10.5194/wes-4-273-2019)；Fleming et al., *Continued results... Part 2*，WES 5 (2020)，[DOI](https://doi.org/10.5194/wes-5-945-2020)；Simley et al., 商业风场实验，WES 6 (2021)，[DOI](https://doi.org/10.5194/wes-6-1427-2021) | 现场 wake-steering 验证已存在。 | 无现场/受控证据时，不得暗示首次实际应用或部署有效性。 |

**审计结论 A：** 普通版本的“动态、鲁棒、预测、图优化、yaw/induction、APC、
风向不确定性、LES/风洞验证”均已实质覆盖；这些路径均不可作为 C0 的创新点。

---

## 2. 本轮主动检索日志

检索日期均为 2026-09-01。以下记录“查到了什么”和“尚未查到什么”，不将后者
曲解为不存在。

| 查询/路径 | 工具/渠道 | 命中和审计读法 | 结论 |
|---|---|---|---|
| `wake steering optimization uncertainty wind direction yaw` | WES/Crossref 原文元数据与前序网页检索 | A1、A2，直接覆盖不确定性与动态风向。 | 广义鲁棒 yaw 方向作废。 |
| `dynamic wake model active farm control LES yaw` | Crossref：10.1002/we.2884 | A3，动态图模型、实时入流估计、LES 和控制回路。 | “动态 yaw 模型”方向作废。 |
| `wake dynamics flow control strategies OFF LES field data` | Crossref：10.5194/wes-10-1055-2025 | A4，动态开源模型、现场驱动序列和 LES 比较。 | 低保真静态模拟不足以竞争。 |
| `wind farm active power control reserve yaw induction wind tunnel` | Crossref：10.5194/wes-11-1607-2026 | A5，实时风洞/动态风向/基线比较。 | “更好 power tracking”方向作废。 |
| `wake steering inflow wind direction uncertainty power loss LES` | Crossref：10.5194/wes-11-2173-2026 | A6，误差可能将预测增益反转为损失。 | 支持问题的重要性，不支持方法空白。 |
| `wake steering conformal prediction`; `wind farm control abstention`; `yaw control risk limiting`; `causal wake steering counterfactual` | 多轮网页/学术搜索（检索结果已在会话中核验） | 顶层结果没有在本轮提供一个已读原文、可确认“完全同一组合”的风电前例；但检索范围和数据库覆盖不足，且相邻术语可能使用 safe learning、assurance、chance constraints、selective prediction、off-policy evaluation、distributionally robust control 等命名。 | **无结论；必须扩检和精读。不得声称 C0 首创。** |
| 近邻论文 reverse/forward citations、近年专利、IEEE/ASME/Scopus/WoS 全库、中文数据库 | 尚未完成/当前访问未验证 | 无法从本次有限网页搜索排除直接前例。 | G2 未通过。 |

### 术语扩展清单（下一轮必须逐项检索）

- `safe reinforcement learning wind farm control`, `safe learning yaw control`,
  `constrained learning wind farm control`, `chance constrained wake steering`;
- `selective prediction`, `reject option`, `abstention`, `assurance case`,
  `risk limiting`, `risk controlling prediction sets` 与 `wind farm`/`yaw`/`wake`；
- `conformal`, `calibration`, `uncertainty quantification`, `lower confidence bound`,
  `prediction interval` 与 `wake steering`；
- `off-policy evaluation`, `counterfactual`, `causal inference`, `uplift`,
  `randomized crossover` 与 `SCADA`/`wind farm control`；
- `distributionally robust`, `CVaR`, `chance constraint`, `safety filter`,
  `control barrier` 与 `wind farm`；
- 同义词：wind-plant control / wind-farm flow control / wake redirection /
  yaw misalignment / axial-induction control / active power control。

每一条应记录数据库、日期、完整查询、前若干结果、DOI/URL、是否阅读全文、
和与 C0 的逐项差异。

---

## 3. 声称 C0 之前必须填满的差异矩阵

| 维度 | C0 所需精确定义 | 若与任一先例相同的后果 |
|---|---|---|
| 科学问题 | 有害干预的**实际**下行风险，而非平均预测增益 | 放弃广义问题陈述。 |
| 反事实 | 基线与 yaw 的潜在结果如何由随机交叉/可识别设计得到 | 只能做预测研究，不能使用 `causal`。 |
| 规则 | 何种 lower/upper bound、何种风险水平、何种动作筛选校正 | 不能使用 `risk-limiting` 或 `guarantee`。 |
| 假设 | 交换性、漂移、噪声、延迟、选择性部署、测量误差 | 不能外推到现场。 |
| 动态 | wake 传播、执行器、控制频率、入流时变性 | 静态实验仅可做消融，不能作主验证。 |
| 安全/载荷 | 直接载荷或经过验证的载荷代理、阈值、回退规则 | 不能使用 `load-safe`。 |
| 比较 | 与 A1–A6 可比的信息集、预算与协议 | 小于强基线即无工程价值。 |
| 验证 | 独立 LES/物理/现场盲测 | 无此项时不能称可部署。 |

---

## 4. 反证优先实验契约（仅在 G2 通过后启用）

- **零收益反例：** 真实 \(\Delta P\) 在模型预测高收益区域为负。gate 若仍部署，
  说明它没有实现其目的。
- **分布漂移反例：** 用未见风向、稳定度、TI、机组状态和时间块盲测；不能用
  随机打散时序替代。
- **模型转移反例：** 不允许在同一个低保真 model family 上校准并以同一模型宣布
  成功。至少需要独立模型/LES。
- **选择性偏差反例：** 只在易获益时施加 yaw 会使观测结果不可直接与 baseline
  比较；需随机化/交叉或明确的识别方法。
- **安全代价反例：** 若 lower-tail power、yaw travel、疲劳/载荷或拒绝率使净价值
  消失，算法应被判为无实用改善。

---

## 5. 最终 go/no-go（以同日处置更新为准）

| 决策 | 状态 | 理由 |
|---|---|---|
| 将 C0 叫作原创方法 | **NO-GO** | 宽泛方法已被 Becker & van Wingerden (2026) 与 Xu et al. (2025/2026) 覆盖。 |
| 写 C0 论文/摘要或出 C0 结果图 | **NO-GO** | 不应在被先例覆盖后继续叙事。 |
| 为 C0 做更多实验或预注册 | **NO-GO** | 更多低保真结果不能恢复其新颖性。可继续检索仅为完善归档，不是推进 C0。 |
| 以现有静态 FLORIS 完成高影响控制论文 | **NO-GO** | 与问题和验证阶梯不匹配。 |
| 在取得独立高保真与受控数据后评估 C0 | **NO-GO as C0** | 新资源可支持一个未来、另起定义并重新审计的项目，但不是恢复已关闭的 C0。 |

最终处置和决定性来源见 `C0_DISPOSITION_2026-09-01.md`。本档案不恢复 P1/P2/P3
的投稿状态，也不为未来项目提供任何“首创”背书。
