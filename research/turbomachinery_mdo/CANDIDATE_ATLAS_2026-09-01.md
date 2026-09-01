# 高发散候选图谱：AI 赋能叶轮机械多学科设计优化

**版本：2026-09-01（Asia/Shanghai）**
**状态：`Triage only / 尚无 Research candidate`**
**目的：** 防止在 GE-E3 与 Pak-B 的断开数据合同上过早得出“无方向”或伪造“已找到方向”两种相反错误。本图谱主动生成并初筛 25 条跨方法、跨学科路线；它不是论文题目清单、不是综述，也不是新颖性声明。

**与既有记录的关系：** 本文件只扩展候选空间，不改写既有关闭决定。数据事实和此前直接前例见[证据与检索日志](EVIDENCE_AND_SEARCH_LOG_2026-09-01.md)、[候选台账](CANDIDATE_LEDGER_2026-09-01.md)；进入真实 MDO 所需的数据合同见[重开条件](REENTRY_REQUIREMENTS.md)；本轮写作与主张边界的复查见[自审计](SELF_AUDIT_2026-09-01.md)。

> **本轮结论。** 25 条路线中，5 条仅保留为需要继续红队审查的**窄研究线索**；2 张卡片带有 `S`（单学科前置）标记，其中 L1 同时也是 `R`，L3 还需要当前范围外的 paired RANS/URANS 真值；其余 19 条为 `B/C/A`（阻断、关闭或工具）。**没有一条同时通过 G0（真实耦合对象）与 G2（敌对新颖性）**，故当前不能诚实地产生“可投稿的 AI 叶轮机械 MDO 论文路线”。这不是“没有思路”的结论，而是一个有边界的筛选结果。

---

## 1. 读法、硬边界与判定纪律

### 1.1 状态码

| 代码 | 含义 | 允许做什么 | 不允许做什么 |
|---|---|---|---|
| `R` | **Red-team lead**：有一个比通用模块拼接更窄的数学/物理对象，但直接近邻、定理和真值合同尚未完成敌对核验。 | 查原文、写反例、定义最小验证与 kill criterion。 | 称为候选、训练模型、预告论文贡献。 |
| `S` | **Single-discipline precondition**：有可能由一个已核验 binary 支撑，但只能是气动或端壁表面温度问题。 | 在 manifest 后做严格单学科基线。 | 称作 MDO、金属温度、寿命或跨库耦合。 |
| `B` | **Blocked**：理论上有工程问题，但当前资源没有其共同设计、物理链或独立真值。 | 记录未来 re-entry 数据合同。 | 用 GE-E3/Pak-B 拼接、伪数据或 latent alignment 代替。 |
| `C` | **Closed at stated breadth**：核心机制已被直接/高度相邻工作占据，或只是已关闭路线的换名。 | 作为基线/反例引用。 | 以改网络、换采集函数或叠标签重立项。 |
| `A` | **Archive/tooling**：有价值的审计或复现基础设施，但不构成投稿级方法贡献。 | 维护 manifest、XDSM、回归测试。 | 把工具包装成新 MDO 方法。 |

### 1.2 不能绕开的数据事实

当前材料只支持两个断开的片段：

```text
GE-E3: x_GE, a_GE  → 3-D 流场 → 气动后处理
Pak-B: x_Pak（孔布局 SDF） → 端壁表面 Temperature 场
```

它们目前没有可核验的共同设计向量、共同 case ID、共同工况、CHT 金属温度、冷却流量/压损、结构响应或寿命真值。因此，以下任何一项一旦需要

\[
 x \rightarrow \text{CFD/CHT} \rightarrow T_{metal} \rightarrow \sigma \rightarrow \text{life},
\]

就必须在“最小合法验证”中拥有**同一对象、同一参数化、同一工况链的真值**。用 OT、生成模型、shared latent space、统计配对或把两组标量并列，均不能替代该条件；详见 [R9](CANDIDATE_LEDGER_2026-09-01.md#3-已关闭路线)。

### 1.3 本图谱的四项硬筛

每条路线都必须回答四个问题；任一问题未答，状态不得高于 `R`：

1. **不可替代机制（G1/G2）：** 它针对的物理或决策对象是什么，而非“AI + BO + UQ + MDO”的模块和？
2. **最小真值合同（G0/G4）：** 用哪个共同 \(x\)、哪条耦合边、哪种独立回算反驳它？
3. **强基线（G2/G5）：** 至少哪一篇直接近邻、哪一种简单方法、哪一种同预算方法必须同时赢过？
4. **停止条件：** 什么结果会明确证明该路线不值得继续，而不是仅解释为“调参还不够”？

> 本文的“最小合法验证”是**必要条件，不是本轮计划，也不是声称资源已具备**。其中出现 CFD、CHT、FEA、寿命或实验时，均表示当前资源缺口。

---

## 2. 25 条路线总览

| ID | 路线（缩写） | 核心对象，而非标签 | 当前状态 | 主要障碍 |
|---|---|---|---|---|
| F1 | 决策稳定的场接口证书（DSIC） | 高维耦合场误差是否足以翻转可行性/支配关系 | `R` | 与 goal-oriented ROM / Pareto surrogate 的实质差异未成立；无耦合真值。 |
| F2 | 接口价值驱动的高保真分配（IVFA） | 哪一条接口、哪次回算最可能改变系统决定 | `C` | goal-oriented enrichment、MDO model management、active sampling 已高度覆盖。 |
| F3 | 损伤等价时空场景压缩（DESR） | 保留 path-dependent damage 与 hotspot identity，而非场 \(L^2\) | `R` | 需证明不只是 problem-dependent scenario reduction；无 CHT–FEA–life 链。 |
| F4 | 临界区域切换感知 MDO（CRS） | 最大温度/应力位置切换的事件边界 | `R` | hot-spot optimization 与分段/非光滑 surrogate 强邻近；无真值链。 |
| F5 | 多接口误差归因与预算（MIEA） | 每条学科接口误差对系统 QOI 的可分辨影响 | `C` | goal-oriented error control、UMDO、coupling approximation 已覆盖。 |
| T1 | hot-streak–coolant 空间失配鲁棒设计 | 热条带迁移与气膜覆盖重叠失配 | `C` | GE-E3 vane 的 hot streak/swirl CHT + cGAN/MOGA 已直接邻近。 |
| T2 | 瞬态工况—冷却结构协同设计 | ramp history 与冷却几何共同决定的热应力/寿命 | `B` | 当前无瞬态、固体、材料及寿命真值。 |
| T3 | as-built 孔形—公差—寿命协同分配 | 制造偏差通过流量/热梯度/应力的链式后果 | `B` | AM as-built cooling 与鲁棒孔优化已有近邻，且当前无 scan/CHT/FEA。 |
| T4 | 内外冷却网络—结构一体优化 | 内部流量网络、外部气膜、压损及结构的共同设计 | `C` | 多目标 CHT 冷却通道/孔布局优化是成熟主题；Pak-B 没有内部网络。 |
| T5 | 空间随机热载荷的可靠性 MDO | correlated thermal-field uncertainty 到失效概率 | `C` | random-field optimization / UMDO 已宽泛覆盖；当前无 thermal–structure truth。 |
| P1 | 热场拓扑相变假说（TTPS） | 可反驳的冷膜断裂/连通性状态转换 | `R` | PH/TDA 广义路线已占据；Pak-B 缺乏流动/CHT机制观测。 |
| P2 | 可变孔数布局神经算子 | variable-cardinality SDF → 温度场 | `C` | SDNO 正是 Pak-B 上的直接前例。 |
| P3 | 气膜交互分解/修正 | 孔（排）非线性 interaction 与 superposition error | `C` | Chen I/II、Yao、Yang、Gao 直接覆盖。 |
| P4 | 传感—冷却—控制共同设计 | sensor locations 与 coolant actuation/寿命闭环 | `B` | 无传感器、动态控制、金属温度或寿命数据。 |
| P5 | 守恒/单调/边界条件约束的冷却场代理 | 可计算物理约束下的场预测 | `C` | physics-informed operator / turbulence closure 已是大类；Pak-B schema 不足以定义守恒残差。 |
| L1 | 因果不变流场表示（CIFS） | geometry/condition interventions 下稳定的场预测机制 | `S` + `R` | GE-E3 必须先证实完整 factorial/case metadata；仍不是 MDO。 |
| L2 | 反事实场接口学习 | 对明确 \(do(x)\) 的场级反事实，而非相关性外推 | `B` | causal representation identifiability 极强；当前没有所需干预映射/耦合系统。 |
| L3 | steady→time-averaged unsteady 流场校正 | 混合平面/稳态模型缺失的 rotor–stator interaction | `S`（外部数据需求） | 新近 GNN turbomachinery work 已直接；GE-E3 并非该 paired RANS/URANS 合同。 |
| L4 | PDE/网格一致 neural field | mesh-invariant、residual-aware 高维流场 surrogate | `C` | FNO/DeepONet/GNN/物理约束 neural field 是成熟簇。 |
| L5 | 可制造约束下生成式逆设计 | performance target → 多个 feasible blade/cooling designs | `C` | cINN/概率逆叶片设计和各类 generative design 已直接邻近。 |
| W1 | MDO 数据图/语义合同 | 自动判定数据是否支持给定 MDO 主张 | `C` | KADMOS、CMDOWS、digital thread、ontology/contract 工作强邻近。 |
| W2 | 主动耦合模型辨识 | 在候选物理耦合图之间选择最少的区分性计算 | `B` | causal-graph MDO、BOED/model discrimination 近邻；当前甚至没有可竞争的共有耦合模型。 |
| W3 | 求解失败/隐藏约束感知 Pareto | 仿真失败也改变安全设计接受决策 | `C` | safe/hidden-constraint BO 与 failure-aware SAO 已是成熟大类。 |
| W4 | 可审计的耦合 MDO 基准/manifest | 版本、XDSM、真值和回算完整性 | `A` | 必要基础设施；不能替代研究机制。 |
| W5 | Pareto 拓扑/不确定性保证 | front topology、persistence 或 Pareto UQ | `C` | Pareto topology、PH-BO、random Pareto surfaces、Pareto UQ 已直接阻断。 |

下面的卡片保留“**机制—近邻—最小验证—强基线—kill criterion**”五个要素。`C/B/A` 卡片同样保留，是为了避免以后换词重启一个已被否定的方向。

---

## 3. 场接口、误差传播与决策（F1–F5）

### F1 — 决策稳定的场接口证书（DSIC） · `R`

- **窄命题。** 对真实共享设计 \(x\) 的接口场 \(q(x)\in\mathcal H\)，不是优化场重构误差本身，而是回答：给定一个**校准过的**场误差集合 \(\mathcal E(x)\)，该误差是否足以改变下游约束可行性或 archive 内任意两点的 dominance。令 \(f_i\) 为最小化目标、\(g_j\le0\) 为约束，可定义
  \[
  f_i^\pm(x)=\underset{e\in\mathcal E(x)}{\operatorname{ext}}\ f_i\bigl(x,\hat q(x)+e\bigr),\qquad
  g_j^+(x)=\sup_{e\in\mathcal E(x)}g_j\bigl(x,\hat q(x)+e\bigr).
  \]
  仅当 \(g_j^+(x)\le0\)（全部 \(j\)）时允许“安全可行”；仅当 \(f_i^+(a)<f_i^-(b)\)（全部 \(i\)）时允许“\(a\) 确实支配 \(b\)”。其余情况应为 **unresolved / 回算触发**，而不是伪“安全证书”。在条件 \(q-\hat q\in\mathcal E\) 成立时，这些只是直接的区间推论；真正难点是 \(\mathcal E\) 如何在相关、OOD、高维场上得到有效校准。
- **不能偷换成什么。** 不能把上述不等式称为新定理，也不能只在单个标量 QoI、独立 GP 区间或训练集 coverage 上演示后称为 MDO safety。
- **直接近邻与威胁。** goal-oriented/model-constrained ROM 已针对指定输出选 basis [S1]；气动 nonlinear PDE 的 dual-weighted-residual/online output estimator 已存在 [S2]；MDO interface POD 已压缩流固数据交换 [S3]；CPOD 已为多目标流场优化校正 POD 对 integral QoI 的偏差 [S4]；dominance-based Pareto surrogate 已直接学习 dominance relation [S5]。这些工作意味着“目标导向、Pareto、接口降维、误差/支配”四个名词的组合**不够新**。
- **最小合法验证。** 一个单一参数化的 cooled blade/vane，至少有 \(x\to\) CFD/CHT 接口场 \(\to\) FEA/life 或两条有反馈的学科边；高/低保真成对 run；冻结的 holdout high-fidelity runs；在真正的 Pareto archive 上衡量 feasibility/dominance flip，而非仅 field RMSE。当前 GE-E3/Pak-B 不具备该合同。一个 manufactured coupled PDE 只能测试逻辑，不可支撑 turbomachinery MDO 结论。
- **强基线。** 全场 POD/autoencoder、goal-oriented RB/DWR、Coelho 型 interface POD、CPOD、objective-wise calibrated interval/conformal score、constraint-boundary sampling、全高保真 archive。
- **Kill criterion。** 若 (i) 该规则仅是上述 QoI bound 的重述，无法给出不同的误差对象；(ii) 以同一回算预算无法少于基线的 false accept/false reject；或 (iii) 所需 \(\mathcal E\) 大到所有 archive 点都 unresolved，则关闭。

### F2 — 接口价值驱动的高保真分配（IVFA） · `C`

- **原想法。** 以“某接口误差最可能改变最终接受/拒绝”代替全局 RMSE，给 CFD/CHT/FEA 之间分配有限的高保真预算。
- **为什么不能单独立项。** 一旦价值定义为 QoI error、active constraint 或 Pareto improvement，就落入 goal-oriented enrichment、Pareto-active-region sampling、MDO model management/UMDO 与 active learning 的既有对象 [S1–S4, S6]；团队 MSFO 又已在 GE-E3/端壁冷却对象上做多/单保真选择 [S7]。
- **最小验证 / 强基线。** 若未来 F1 的不同数学对象成立，才可作为其一部分，用同预算的 uniform、variance、EI/EHVI、DWR/QoI enrichment、MSFO 比较真实错误决策数。
- **Kill criterion。** 只要 acquisition 可改写为已知 QoI error、EI/EHVI、active-constraint 或 MSFO 分数的单调变换，或者没有 F1 的新误差对象，永久并入 `C`，不得独立投稿。

### F3 — 损伤等价时空场景压缩（DESR） · `R`

- **窄命题。** 对时空热边界随机场 \(\xi(s,t)\)，寻找带权场景 \(\{(\xi_k,w_k)\}_{k=1}^K\)，其目标不是最小化输入场距离，而是保留 \(x\mapsto\{D_\ell(x,\xi),\ell^\star(x,\xi)\}\) 中的**路径相关损伤分位数、失效判定与 governing-hotspot identity**。候选差异只能来自对 path-dependent damage operator 的结构利用，例如在材料损伤模型/伴随可微时建立可检验的损伤敏感度界。
- **直接近邻与威胁。** 已有直接利用目标和约束的 problem-dependent scenario reduction，并给出稳定性讨论 [S8]；random-field optimization 已将随机场直接写入优化 [S9]；疲劳随机载荷的 ML control variate/不偏估计也已处理“整段应力历史→损伤” [S10]；水轮机启动轨迹的 ML + Rainflow/Miner + 实验验证已说明“用代理优化损伤”本身不是空白 [S11]。更直接地，equivalent-fatigue-load 框架已经以 damage/failure equivalence 压缩复杂载荷、并讨论目标结构不确定性 [S38]；damage micromechanics 的 ROM 工作也已用耗散驱动/贝叶斯方式选择高维 load paths [S39]。因此本线索现在是**高风险 `R`**：只有“跨设计、分布量、hotspot identity 的联合保持”能够被严格证明不同于这些已有对象，才有继续价值。
- **最小合法验证。** 同一叶片几何 \(x\)、可追溯的瞬态 CHT 热边界、温度相关 FEA、预先定义且可复算的 fatigue/TMF model、独立场景样本和 holdout high-fidelity life calculation。GE-E3/Pak-B 均没有。
- **强基线。** KL/PCA 截断、随机/分层场景、Wasserstein/Euclidean scenario reduction、input-field QoI/DWR reduction、全场 MC、已知 problem-dependent reduction。
- **Kill criterion。** 若同样 \(K\) 下 KL 或已有 problem-dependent reduction 对 failure probability、life quantile、hotspot identity 同样准确；若 damage model 对输入实际上近似线性/无路径依赖；或没有可验证的 high-fidelity life truth，则关闭。

### F4 — 临界区域切换感知 MDO（CRS） · `R`

- **窄命题。** 把 \(s^\star(x)=\arg\max_s\Theta(x,s)\)（或最大应力点）迁移视为物理/决策事件，而不是平滑场回归的附带产物。仅在能预先定义区域图、切换公差、网格稳定性和后果（例如不同危险区对应不同结构/寿命限制）时，才可能研究 event-boundary-aware surrogate。
- **直接近邻与威胁。** 热管理中，\(T_{max}\) 的位置随优化改变以及其非光滑性已被明确讨论 [S12]；hotspot-field ROM/局域目标模型已可做到精确误差控制 [S13]。因此“预测最大温度与 hotspot 位置”不是机制。
- **最小合法验证。** 同一网格族下的场真值，预注册的 critical regions，独立设计点上的 \(T_{max}\)/\(\sigma_{max}\)/location 与随后的 life consequence；至少一个 mesh-refinement negative control。Pak-B 若二进制可得，最多能测试 surface `Temperature` 的单学科 event，不可叫 metal hotspot/life。
- **强基线。** 全场 RMSE 最优 surrogate、softmax/KS max objective、区域最大值回归、普通 active learning、分段 mixture-of-experts。
- **Kill criterion。** 若区域标签对阈值/网格不稳定，若全场 RMSE 与事件错误完美同序（说明没有额外决策结构），或若事件不能改变可回算的工程约束，则关闭。

### F5 — 多接口误差归因与预算（MIEA） · `C`

- **原想法。** 将总系统 QOI 误差分配给 CFD→CHT、CHT→FEA、FEA→life 等接口，并据此分配模型改进预算。
- **关闭理由。** 在有可微耦合模型时，这是 goal-oriented adjoint/error propagation；在随机设置是 UMDO/UQ；在忽略弱耦合时已有 optimal coupling approximation [S14]。没有实质不同的误差算子和可识别假设，就只是上述工作在新图上的实现。
- **Kill criterion。** 任何 proposed attribution 若与 chain rule/adjoint sensitivity、Sobol/Shapley 或 known coupling approximation 等价，或无法处理合作用项而仍声称唯一归因，则关闭。

---

## 4. 气热、结构、寿命与运行（T1–T5）

### T1 — hot-streak–coolant 空间失配鲁棒设计 · `C`

- **想法。** 用热条带/旋流迁移与冷却膜覆盖的空间错配定义损失，优化孔布局或冷却流量分配。
- **近邻与关闭理由。** GE-E3 vane 上已有 hot streak + swirl 的 CHT 研究 [S15]，并已有以非均匀热载荷、hot streak/swirl、276-bit 孔布局、cGAN 与 MOGA 的 CHT 气膜优化 [S16]。这已覆盖核心物理叙事和 AI 优化结构。
- **资源边界 / kill criterion。** Pak-B 不是该 vane CHT 合同，GE-E3 无对应冷却/固体域。除非先证明一个不可被上述“空间错配 + CHT optimization”替代的新机制及新真值，否则关闭。

### T2 — 瞬态工况—冷却结构协同设计 · `B`

- **想法。** 同时优化温度/转速 ramp \(u(t)\) 与冷却结构 \(x_c\)，以热应力、效率和寿命为目标。
- **近邻与威胁。** 启停和变负荷的 transient thermal–fluid–solid blade analyses 已量化热应力对 ramp rate 的敏感性 [S17]；动态 system co-design 是 MDO 已有大类。论文价值只可能来自一个明确的 blade-specific control–damage mechanism，不能只是 NSGA-II/RL 加代理。
- **最小合法验证。** 瞬态 CHT、温度相关结构模型、材料/寿命模型、operational trajectory constraints，以及 independent transient replays。当前数据无一具备。
- **强基线 / kill criterion。** 固定几何优化控制、固定控制优化几何、两阶段 sequential、MPC/直接配点或传统 dynamic co-design；若联合设计优势被任一 sequential baseline 消除，或 life model 未可验证，关闭。

### T3 — as-built 孔形—公差—寿命协同分配 · `B`

- **想法。** 不只鲁棒优化 nominal 孔形，而是把可测/可设的制造公差当设计变量，研究 as-built 几何经流量、热梯度和孔边应力对寿命的影响。
- **近邻与威胁。** 小制造偏差对 \(\eta\) 和 discharge coefficient 的 UQ 已被量化 [S18]；AM as-built inlet/exit rounding、粗糙度与 overall cooling performance 已有 CT/实验研究 [S19]；鲁棒孔形优化也已有前例。因此“manufacturing uncertainty + cooling optimization”不能作为新颖性。
- **最小合法验证。** design-intent/as-built 成对几何、制造分布、internal/external CHT、孔边 FEA/TMF、独立 scan/实验或高保真回算。当前无 scan、材料、压力流量或结构标签。
- **Kill criterion。** 若公差仅以 iid diameter noise 代替、没有可观测 as-built feature 与链式机制、或 robust optimum 不异于已有 worst-case/PCE/MC 结果，则关闭。

### T4 — 内外冷却网络—结构一体优化 · `C`

- **想法。** 共同优化内部冷却网络、外部气膜孔、压损和热应力。
- **关闭理由。** 冷却结构优化综述已涵盖 CHT、内部通道、孔布局、多目标热/压损/寿命取舍 [S20]；C3X cooling-passage 多目标优化已直接改变通道形状和位置 [S21]。Pak-B 无内部冷却网络或压损，GE-E3 无冷却构型。
- **Kill criterion。** 如果提案不能指出新的、可测的 internal–external coupling mechanism（而非更多设计变量），不再继续。

### T5 — 空间随机热载荷的可靠性 MDO · `C`

- **想法。** 用 KL/GP 表示 hot streak、HTC 或材料场不确定性，优化失效概率。
- **关闭理由。** 随机场优化 [S9]、空间自适应 PCE 的 FSI UQ、UMDO/RBMDO 和团队/领域内多源随机叶片寿命代理已形成成熟谱系；“空间相关 + RBDO/MDO”不足以成立。现有 GE/Pak 更无共享 thermal–structure chain。
- **Kill criterion。** 若唯一新增项是 covariance kernel、KL 截断阶数或 optimizer，更改为归档线索。

---

## 5. 气膜物理、变拓扑与监测（P1–P5）

### P1 — 热场拓扑相变假说（TTPS） · `R`（且仅可降级为 `S`）

- **窄命题。** 不把 persistent homology 当作特征工程，而是先定义可反驳的物理状态假说：在固定、已知的无量纲工况下，某类 jet lift-off、冷膜断裂、再附着或二次流重排会引起阈值化温度/效率场连通域的稳定改变；该改变必须在独立高保真场中先于或同步于一个预定义的工程风险量发生。
- **直接近邻与威胁。** Pareto-set topology [S22]、topological BO [S23]、Pareto front UQ [S24] 与 PH-driven multiobjective topology design 已阻断“用 PH 做多目标优化/保证 Pareto topology”的宽泛路线。流体 TDA 也是已有簇。故拓扑只能是**诊断变量**，不能是贡献本身。
- **最小合法验证。** 相同几何/工况上的 velocity、temperature/efficiency、必要时涡量或流线真值；预先冻结滤波、阈值族、persistence threshold；比较独立样本上的事件检测。Pak-B 当前只公开 surface `Temperature`，没有 velocity、工况变化或 CHT，因此最多能测试一个不作机理归因的单学科关联。
- **强基线。** area-average、\(T_{max}\)、hot-area fraction、spatial gradient、connected-component count、传统 jet/secondary-flow diagnostics、无拓扑的 logistic/event model。
- **Kill criterion。** 若结果随阈值/网格/平滑任意改变、无法超过经典场统计量、或没有独立流动诊断支持物理事件，则关闭。

### P2 — 可变孔数布局神经算子 · `C`

- **关闭理由。** SDNO 已在 Pak-B 用 SDF、Calculate Net、Superposition Net 和 Sellers 结构训练低孔数/预测高孔数 [S25]。孔数外推、set/variable-cardinality representation、SDF 或 neural operator 不得换名重启。
- **Kill criterion。** 只要模型输入仍是 Pak-B SDF、输出仍是 `Temperature` 场、贡献仍是高孔数外推，视为 SDNO 基线复现而非新路线。

### P3 — 气膜交互分解/修正 · `C`

- **关闭理由。** Chen I/II 已用 decomposition、error-source tracking、kidney-vortex row interaction 和 nonlinear superposition [S26, S27]；Yao 已用 vortex-encoded AI 修正 dense layouts [S28]。Pak-B 还没有已核验的 nested subset mapping/0-hole reference，不能把不同布局当物理干预。
- **Kill criterion。** 任一“孔/排 interaction + 误差修正/风险排序/active query”如果没有与上述机制不同的、可被真值反驳的对象，保持关闭。

### P4 — 传感—冷却—控制共同设计 · `B`

- **想法。** 为叶片选择有限个可存活的温度/应变/压力测点及 coolant actuation，以最小化 life-risk 或控制成本。
- **近邻与缺口。** optimal sensor placement、sparse field reconstruction、digital twin 与主动冷却/健康管理均有广泛先例；真正创新必须来自“传感可辨识的损伤/热状态如何改变冷却设计”的明确机制。Pak-B 无传感器位置/噪声/动态/执行器/金属温度，GE-E3 无冷却控制。
- **最小合法验证。** 同一 hardware 上的 sensor forward model、noise/placement constraints、control inputs、transient CHT/FEA/life truth；与 full-field oracle、D-optimal/EI、POD/CS 与固定布局比较。
- **Kill criterion。** 若没有硬件可实现性和 closed-loop truth，只是稀疏重构或 sensor-placement 论文，不能称 MDO。

### P5 — 守恒/单调/边界条件约束的冷却场代理 · `C`

- **关闭理由。** PDE-residual、physics-informed neural operator、invariant turbulence closure 已是成熟方法族；例如 ML turbulent diffusivity 已针对气膜流动使用无量纲、不变特征并需要 RANS/高保真流场 [S29]。Pak-B 的公开接口没有可用于写完整守恒残差的速度、压力、物性、边界和网格语义。
- **Kill criterion。** 若“physics”只等于输出范围裁剪、平滑正则或未证实的 Seller/单调假设，关闭；不得把它称为守恒保证。

---

## 6. 因果、场学习与逆设计（L1–L5）

### L1 — 因果不变流场表示（CIFS） · `S` + `R`

- **窄命题。** 若 GE-E3 binary 最终证实了同一几何与边界条件的明确干预结构，可把 geometry 与 operating condition 的受控变化当 environment/intervention，研究是否存在一种 field representation \(z\)，使预测机制在这些环境下稳定，而不是仅在 pooled ERM 下拟合。研究对象是**预先可见的 condition/geometry shift 下的误差与守恒/性能后果**，不是把 IRM 标签贴到 FNO 上。
- **不可越过的因果边界。** 只有在样本元数据确认 case pairing、干预变量、其他条件保持规则和支持域后，才可能使用 \(do(\cdot)\) 语言；没有这种合同，只能叫 multi-environment/domain generalization，不能从 CFD 样本的相关性声称发现因果机制。
- **直接近邻与威胁。** IRM 已给出多环境不变预测的理论目标及其强假设 [S30]；因果图已用于 MDO 的降维/分解 [S31]；已有 turbomachinery GNN field surrogate 强调 mesh/permutation invariance 和稳态—非定常误差校正 [S32]。所以“因果 + flow surrogate”本身不新。
- **最小合法验证。** GE-E3 实际 binary 的 version/hash/schema/case map；grouped split（整几何、整工况组合和组合外推）；三个或以上训练环境；完全 holdout 的 geometry×condition combinations；normalization leakage audit；真实 field QOI 和气动指标。当前仍未拿到 binary，故不得训练。
- **强基线。** pooled ERM FNO/DeepONet/Transformer/GNN、group DRO/REx、IRM/IRM variants、domain-adversarial representation、明确物理无量纲化、简单 per-condition model；negative controls 必须含随机 environment label、错误的 grouping、变量置换。
- **Kill criterion。** 若 (i) metadata 不支持干预解释；(ii) 在 grouped OOD 上不优于 ERM/GroupDRO；(iii) 只提升 IID；或 (iv) 消融后优势来自额外参数/不公平 split，则关闭。即使全部通过，也只是 GE-E3 **单学科气动前置论文**，不可写为 MDO。

### L2 — 反事实场接口学习 · `B`

- **想法。** 从高维流场/热场中学习明确设计干预的 counterfactual field，并把其作为下游耦合接口。
- **关闭/阻断理由。** causal representation learning 的可识别性需要干预、潜变量、噪声与映射的强假设 [S33]。GE-E3/Pak-B 没有统一因果图、更没有共同的 downstream structural interface。它不能以 “counterfactual” 名称绕过 R9。
- **Kill criterion。** 没有可追溯 \(do(x)\)、matched counterfactual truth 和反事实错误测试，即刻关闭，不做隐空间“反事实”可视化。

### L3 — steady→time-averaged unsteady 流场校正 · `S`（外部资源要求）

- **想法。** 对 mixing-plane/RANS 的缺失 rotor–stator interaction 做 mesh-level correction，使下游设计更可靠。
- **近邻与边界。** 新近 turbomachinery GNN 已从 steady RANS 预测 time-averaged URANS，并公开讨论这一对象 [S32]。GE-E3 公开合同当前也不是 paired steady-RANS/URANS。因此只能作为“阅读该类模型的强基线”而非当前路线。
- **Kill criterion。** 没有 paired input/output solver truth、mesh correspondence 与全行/多工况 split，则不碰；不得从 GE-E3 单一场猜测 URANS label。

### L4 — PDE/网格一致 neural field · `C`

- **关闭理由。** FNO、DeepONet、mesh GNN、physics-informed closure 和 transformer neural operator 已覆盖“高维 PDE 场 + mesh invariance + 物理残差”。仅换 operator block、attention 或 coordinate embedding 不是机制。
- **Kill criterion。** 新提案若其主结果仅是 field RMSE/速度而没有不同的受检验物理/决策对象，关闭。

### L5 — 可制造约束下生成式逆设计 · `C`

- **关闭理由。** gas-turbine blade 的 cINN/probabilistic inverse design 已从 performance/constraints 生成多个 design 并用 CFD 验证 [S34]。结合 diffusion、VAE、GAN 或 constraints 仍须先展示不同的可制造/多物理机制；当前两数据集没有共同 design-to-performance relation。
- **Kill criterion。** 若目标仍是“由 performance 反推 blade/cooling geometry”的 one-to-many generation，而约束仅通过 post-filter 实现，保持关闭。

---

## 7. 数据、工作流与 Pareto 叙事（W1–W5）

### W1 — MDO 数据图/语义合同 · `C`

- **价值。** 用机器可读的变量、单位、设计 ID、solver version、coupling edge、truth role 与 split 显式判定“某数据是否支撑某 MDO 主张”。这正是本目录 manifest/XDSM 的正确用途。
- **为什么不是论文主线。** MDAO formulation/integration 已有 KADMOS graph-based methodology [S35]、CMDOWS/dynamic workflow、digital thread、ontology/data integration 等大量前例。一个 schema 或 dashboard 不会自动形成新科学机制。
- **正确产出。** `build_data_manifest.py`、数据卡、XDSM、负面案例（GE-E3/Pak-B 不可拼接）。其 kill criterion 是：一旦 schema 无法阻止明显的假耦合或无法复现版本，作为工具也应重写；即使成功也仍是 `A`。

### W2 — 主动耦合模型辨识 · `B`

- **窄问题。** 在预先给定、物理上可辩护的多种 coupling models \(\{M_k\}\) 中，选择最少的新仿真/实验来降低“哪个模型会改变可行 Pareto 决策”的不确定性。
- **直接近邻与障碍。** causal graph 已用于 MDO 变量筛选 [S31]；optimal experimental design、model discrimination 和 problem-dependent data valuation 也是成熟方向。当前更根本的问题是没有任何共同 \(x\) 或可辩护的 GE–Pak coupling model 集合。
- **最小合法验证。** 先有多个可反驳、共享单位/边界的物理模型，后有可执行的共同实验/高保真 query；比较 uniform DOE、D-optimal、expected model discrimination、decision-focused BOED。
- **Kill criterion。** 若候选模型只由 neural architecture/latent alignment 区别，而不是物理上可反驳的 couplings，或最终没有 decision-level truth，关闭。

### W3 — 求解失败/隐藏约束感知 Pareto · `C`

- **关闭理由。** safe optimization、hidden constraint BO、failure-aware SAO、constrained Pareto identification 已直接处理“计算失败也传递信息”。当前数据甚至没有 solver-failure label；Pak-B/GE-E3 是已生成场数据，不是可重复执行的 black-box simulation campaign。
- **Kill criterion。** 若 failure label 由 surrogate 预测错误、人为阈值或缺失值冒充，或没有重跑验证，则关闭。

### W4 — 可审计耦合 MDO 基准/manifest · `A`

- **价值与边界。** 可重放的 coupled benchmark 应包含 XDSM、共同设计参数化、单位、版本、truth fidelity、solver seed、split、独立 replay 和明确的 failed cases。公开的 scalable RMDO benchmark/standard MDO formulations 可作为形式参考 [S36]。
- **为什么不叫研究候选。** 基准构建若没有新的、被广泛采用的 evaluation gap 或公开多物理真值，通常是基础设施而非 AI-MDO 方法。当前本仓库唯一可执行的工具是未来 MAT binary 的 provenance manifest，尚无真实 binary。
- **Kill criterion。** 若无法提供可运行的共同真值或不能再现一个基础 baseline，就不应把“benchmark”写入论文贡献。

### W5 — Pareto 拓扑/不确定性保证 · `C`

- **关闭理由。** data-driven Pareto-set topology [S22]、persistence-diagram BO [S23]、Pareto-front UQ [S24]、random Pareto front surfaces、PH-driven topology-design selection 已覆盖宽泛命题。另有 dominance-surrogate、error-bounded Pareto approximation 与 uncertainty-aware MOEA 等强邻域 [S5, S37]。
- **Kill criterion。** 任何主要卖点若可概括为“用 persistent homology/拓扑/不确定性看 Pareto front”，保持关闭。F1 若继续，必须以**真实接口场误差与决策反转**为对象，不能滑回该路线。

---

## 8. 仅存的五条红队线索：下一轮必须先做什么

这五条不是候选排名；它们只是目前没有被“一个直接前例 + 一个当前硬缺口”同时彻底击穿的狭窄问题。任何一条均须在开始实现前完成下表的 **first disproof**。

| 线索 | 先做的反证工作 | 通过前绝不做的事 | 通过所需的新证据 |
|---|---|---|---|
| F1 DSIC | 精读 [S1–S5]，逐式比较 error object、assumption、certificate target；构造一个例子证明普通 QoI bound 与 proposed rule 给出不同接受决定。 | 不写“safe/certified Pareto ROM”，不把 interval arithmetic 叫新理论。 | 真实 shared-\(x\) coupled benchmark；calibration protocol；同预算决策错误对比。 |
| F3 DESR | 精读 [S8–S11, S38–S39]，逐项证明 joint damage-distribution/hotspot-preserving objective 不等于已有 problem-dependent reduction、equivalent fatigue load 或 load-path ROM；写出非线性/路径依赖必要条件。 | 不以 Miner 后处理或 KL 压缩冒充新场景约简。 | 瞬态 CHT–FEA–life truth 与独立场景。 |
| F4 CRS | 预注册 event definition，做 mesh/threshold perturbation 反例；证明 event loss 不能由 RMSE/softmax max 代替。 | 不把 hotspot position 的回归误差叫工程价值。 | 同一耦合系统的 risk/life 后果与独立 replay。 |
| P1 TTPS | 首先建立一个冷膜断裂/再附着等可观察、可否证的物理机制；与 classic field diagnostics 做盲测。 | 不画 persistence diagram 后再倒推物理故事；不称 Pareto topology。 | velocity/thermal field 的独立高保真或实验诊断。 |
| L1 CIFS | 先取得并审计 GE-E3 case map，验证是否真的存在符合干预解释的环境结构；做随机环境标签负对照。 | 不把 simulation DOE 自动称为因果发现；不称 MDO。 | frozen binary manifest，grouped OOD split，公平 baseline 和多环境验证。 |

### 8.1 当前资源下最诚实的优先级

1. **先等待/合法取得并冻结 GE-E3/Pak-B binary，而不是训练。** 没有 schema、case map、hash、许可和 split，L1/P1 连单学科可重复性也没有。
2. **若 binary 到位，L1 或 P1 最多可成为单学科审计研究的 exploratory protocol。** 它们不能补齐 MDO 断边；若结果不支持相应机制，应按 kill criterion 关闭。
3. **F1/F3/F4 是未来真实耦合计算/数据出现后的方法线索，当前只能做文献级反证和解析反例。** 一个自造 toy PDE 可测试条件逻辑，但不能抬升为叶轮机械多学科验证。
4. **其余路线不应靠“多发散一点”再次重开。** 发散阶段已保存它们的机制和近邻；下一步应是对五条 `R` 线索做更深、原文级的敌对核验，而不是重复添加词汇相近的方向。

---

## 9. 本轮可复查的近邻来源登记

下表记录本图谱实际依赖的可访问网页、出版社页面或原始开放文档。标记 `摘要级` 意味着它只能支持表中明确的题目/摘要事实；**不能据此推断论文未做的实验、定理或限制**。后续若某线索接近候选，必须获取并精读原文。

| 编号 | 来源与检索层级 | 此处只使用的事实 |
|---|---|---|
| S1 | [Bui-Thanh et al., *Goal-Oriented, Model-Constrained Optimization for Reduction of Large-Scale Systems* PDF](https://kiwi.oden.utexas.edu/papers/Goal-oriented-basis-optimization-Bui-Willcox.pdf)（开放文档） | goal-oriented/model-constrained ROM 为目标 QoI 构造 basis。 |
| S2 | [goal-oriented RB for nonlinear parametric PDEs, DOI 10.1002/nme.6395](https://doi.org/10.1002/nme.6395)（出版社摘要） | 参数化非线性 PDE、dual-weighted residual、output-adaptive snapshots 与 output error estimation。 |
| S3 | [Coelho et al., 2008, MDO interface POD, DOI 10.1007/s00158-007-0212-5](https://doi.org/10.1007/s00158-007-0212-5)（出版社摘要） | POD/MLS 用于减少 fluid–structure MDO 的跨学科数据交换。 |
| S4 | [Brette et al., CPOD and Kriging, DOI 10.1007/s00158-009-0434-9](https://doi.org/10.1007/s00158-009-0434-9)（出版社摘要） | 多目标流场优化中以 constrained POD 保留 integral QoI/Pareto accuracy。 |
| S5 | [Loshchilov et al., Dominance-Based Pareto-Surrogate](https://inria.hal.science/inria-00522653v1/document)（开放文档） | 用 rank-SVM/primary-secondary constraints 建模局部 Pareto dominance。 |
| S6 | [Constrained multi-objective optimization with limited function-evaluation budget](https://link.springer.com/article/10.1007/s12293-022-00363-y)（出版社摘要） | constrained MOO 中已有 surrogate、约束误差 margin 和有限预算处理。 |
| S7 | [Wang et al., 2024 MSFO, DOI 10.1115/1.4064228](https://doi.org/10.1115/1.4064228)（出版社/Crossref 摘要） | 团队多/单保真融合在 GE-E3 blade optimization 和 turbine-endwall layout 中验证。 |
| S8 | [Bertsimas & Mundru, optimization-based scenario reduction PDF](https://optimization-online.org/wp-content/uploads/2022/01/8773.pdf)（开放文档） | scenario reduction 可用 objective/constraint structure 定义 problem-dependent divergence，并讨论稳定性。 |
| S9 | [Random field optimization](https://www.sciencedirect.com/science/article/pii/S0098135422001922)（出版社摘要） | 随机场可直接进入一般无限域优化模型。 |
| S10 | [ML control variates for time-domain fatigue analysis](https://www.sciencedirect.com/science/article/abs/pii/S0888327020305781)（出版社摘要） | 对随机应力时程的 fatigue damage，有 ANN-based unbiased control-variate 与 error estimate。 |
| S11 | [Fatigue damage reduction in hydropower startups with ML](https://www.nature.com/articles/s41467-025-58229-z)（开放正文） | ML stress surrogate + Rainflow/Miner 优化启动，并以缩比机实验检验损伤。 |
| S12 | [Hot spot temperature optimization of customized region](https://www.sciencedirect.com/science/article/abs/pii/S0017931022004379)（出版社摘要） | \(T_{max}\) 位置会随优化改变，最高温度目标具有特殊非光滑性。 |
| S13 | [Low-rank MOR for hotspot thermal analysis](https://www.sciencedirect.com/science/article/abs/pii/S0167926018305224)（出版社摘要） | hotspot-targeted thermal ROM 可有 predefined error bound。 |
| S14 | [Baptista et al., *Optimal Approximations of Coupling in Multidisciplinary Models* PDF](http://mcubed.mit.edu/files/public/RT3/2017__Willcox__Optimal_Coupling.pdf)（开放文档） | 以系统输出分布的信息损失与 coupling sparsity 选择近似耦合，并含 turbine-engine cycle analysis。 |
| S15 | [GE-E3 film-cooled vane under hot streak and swirl](https://www.sciencedirect.com/science/article/abs/pii/S1359431117368400)（出版社摘要） | GE-E3 vane 的 CHT 已研究 hot streak/swirl 对气膜与热载荷的作用。 |
| S16 | [He et al., 2022 CHT/cGAN/MOGA cooling layout, DOI landing page](https://www.sciencedirect.com/science/article/abs/pii/S0017931022006196)（出版社摘要） | nonuniform hot streak/swirl，CHT CFD，cGAN，276-bit holes 和 MOGA。 |
| S17 | [Startup/shutdown/load variation transient blade fields](https://link.springer.com/article/10.1007/s11630-022-1603-z)（出版社摘要） | transient thermal-fluid-solid simulations 显示 ramp rate 影响 thermal stress。 |
| S18 | [Manufacturing deviations in fan-shaped film-cooling hole UQ](https://www.mdpi.com/2226-4310/6/4/46)（开放正文） | conical angle/fillet/diameter deviation 改变 \(\eta\) 与 discharge coefficient，使用 PCE UQ。 |
| S19 | [As-built additively manufactured cooling holes](https://asmedigitalcollection.asme.org/turbomachinery/article/145/3/031017/1152177/Printability-and-Overall-Cooling-Performance-of)（出版社摘要） | as-built rounding/roughness 影响 overall cooling performance。 |
| S20 | [Optimization of cooling structures in gas turbines: review](https://www.sciencedirect.com/science/article/pii/S1000936121003289)（出版社摘要） | 汇集气膜/内部冷却、CHT、热应力、寿命和多目标优化近邻。 |
| S21 | [C3X cooling passage multiobjective optimization](https://www.sciencedirect.com/science/article/abs/pii/S1359431116306597)（出版社摘要） | 以通道形状/位置、最大温度与温度梯度进行 reduced CHT 多目标优化。 |
| S22 | [Hamada et al., Pareto-set topology with persistent homology](https://ar5iv.labs.arxiv.org/html/1804.07179)（开放预印本） | PH 已用于判断 Pareto sample 的 simplex topology。 |
| S23 | [Topological Bayesian Optimization](https://arxiv.org/abs/1902.09722)（开放预印本） | persistence diagrams 已进入 BO。 |
| S24 | [Pareto-front uncertainty quantification](https://link.springer.com/chapter/10.1007/978-3-030-53669-5_28)（出版社章节页） | Pareto fronts 的均值、方差、区间和统计困难已有系统讨论。 |
| S25 | [Wang et al., 2024 SDNO, DOI 10.1063/5.0239483](https://doi.org/10.1063/5.0239483)（出版社摘要） | Pak-B、SDF、Sellers-type superposition、低孔训练/高孔外推。 |
| S26 | [Chen et al., 2025 I, DOI 10.1063/5.0276858](https://doi.org/10.1063/5.0276858)（Crossref/出版社摘要） | multi-row decomposition、error-source tracking、kidney-vortex interaction。 |
| S27 | [Chen et al., 2025 II, DOI 10.1063/5.0293895](https://doi.org/10.1063/5.0293895)（Crossref/出版社摘要） | vortex-induced-velocity/turbulent-diffusion nonlinear superposition。 |
| S28 | [Yao et al., 2025, DOI 10.1063/5.0260945](https://doi.org/10.1063/5.0260945)（Crossref/出版社摘要） | vortex-encoded AI + Sellers operation 面向 dense cooling layouts。 |
| S29 | [ML turbulent diffusivity for film cooling](https://asmedigitalcollection.asme.org/turbomachinery/article/140/2/021006/378888/A-Machine-Learning-Approach-for-Determining-the)（出版社页面/检索摘要） | 气膜 RANS heat-flux closure 已采用 machine learning；其完整物理输入要求不能由 Pak-B 公开接口假定。 |
| S30 | [Arjovsky et al., Invariant Risk Minimization](https://leon.bottou.org/publications/pdf/tr-irm-2019.pdf)（开放预印本） | 多环境 invariant predictor 的目标、条件和局限。 |
| S31 | [Wu et al., causal relationship to assist MDO, DOI 10.1115/1.4042342](https://doi.org/10.1115/1.4042342)（出版社摘要） | causal graph/DSM 用于 MDO 中变量筛选、降维与分解。 |
| S32 | [GNN prediction of time-averaged unsteady turbomachinery flow, DOI 10.1115/1.4069140](https://doi.org/10.1115/1.4069140)（开放正文） | steady RANS→time-averaged URANS、mesh GNN、rotor–stator interaction correction。 |
| S33 | [Interventional causal representation learning](https://proceedings.mlr.press/v202/ahuja23a/ahuja23a.pdf)（开放文档） | 高维因果表示的干预与可识别条件。 |
| S34 | [Probabilistic inverse turbine-blade design, DOI 10.1115/1.4052301](https://asmedigitalcollection.asme.org/mechanicaldesign/article/144/2/021706/1119286/Inverse-Aerodynamic-Design-of-Gas-Turbine-Blades)（出版社页面） | cINN + multifidelity GP 的 3-D turbine-blade inverse design/CFD validation。 |
| S35 | [KADMOS graph-based MDAO formulation/integration](https://www.sciencedirect.com/science/article/pii/S1270963818326944)（出版社摘要） | formal graph 从 tool repository 到 MDAO workflow formulation。 |
| S36 | [Scalable robust MDO benchmark](https://arxiv.org/pdf/2303.01371)（开放预印本） | 可配置 discipline/coupling/design dimensions 的 RMDO benchmark。 |
| S37 | [Divide and Conquer: provably unveiling the Pareto front](https://arxiv.org/pdf/2402.07182)（开放预印本） | Pareto-front approximation error/convergence guarantee 的直接相邻理论。 |
| S38 | [Equivalent fatigue load approach for fatigue design of uncertain structures](https://www.sciencedirect.com/science/article/abs/pii/S0142112320300475)（出版社摘要） | 以复杂载荷的 damage/failure equivalence 构造 simplified/equivalent fatigue load，并考虑目标结构不确定性。 |
| S39 | [Goury et al., load-path selection for damage ROM, DOI 10.1007/s00466-016-1290-2](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7175740/)（开放正文） | 对高维/时变加载路径，使用耗散驱动样本与 Bayesian optimization 构造 computational-damage ROM。 |

---

## 10. 结论与防漂移规则

- 本图谱已经**扩大**而非缩小了探索：场接口、损伤路径、非光滑临界区、随机场、瞬态控制、制造、内部/外部冷却、物理拓扑、传感控制、因果场学习、逆设计、数据图和 Pareto 理论都已进入同一审计尺度。
- 扩大不等于允许重复：`C` 的路线必须保持关闭，`B` 的路线必须保持资源缺口可见，`S` 只能做单学科，`R` 也只是待反证线索。
- 当前最接近真正 MDO 方法问题的是 F1/F3/F4，但它们均缺少合法的 coupled truth；当前最接近可验证的公开数据问题是 L1/P1，但它们均不构成 MDO。**这两个事实必须同时写在任何后续摘要、代码 README、汇报页和投稿草稿中。**
- 下一轮的正确动作不是宣称“发现了空白”，而是按 §8 对五条 `R` 线索做原文级邻接核验、解析反例和可杀死实验设计；若未通过，继续关闭并重新发散。
