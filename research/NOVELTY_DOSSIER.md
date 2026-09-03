# NOVELTY_DOSSIER — 新颖性审计档案

> **2026-09-01 补充：** 对初始 C0（可弃权、风险受限动态 wake-steering）假设的独立新颖性审计见 [`novelty_audits/C0_ABSTENTION_RISK_CONTROL_NOVELTY_AUDIT_2026-09-01.md`](novelty_audits/C0_ABSTENTION_RISK_CONTROL_NOVELTY_AUDIT_2026-09-01.md)，其最终处置见 [`C0_DISPOSITION_2026-09-01.md`](novelty_audits/C0_DISPOSITION_2026-09-01.md)。C0 因动态风险规避/避损的直接风电先例与通用选择性风险控制先例而 **CLOSED AS FORMULATED**；它不能作为任何“首创”或投稿主张，且不改变 P1/P2/P3 的非投稿结论。
>
> **当前覆盖结论（2026-08-31 forensic round）：** 本文件的旧 P1-b/P2“存活”“无结构先例”“核心创新”结论已被后续模型域、数值稳定性、代码语义和直接先例审计推翻。P1/P2/P3 目前均非独立 WES 投稿候选；旧段落仅保留为可追溯审计历史，不能被选择性引用。P1/P2 的权威纠正见 `P1_P2_FORENSIC_STATUS.md`，P3 的纠正在本文文末及 `SELF_AUDIT.md` 审计点 #8。
>
> 审计原则：候选点的"新颖"是待证伪假设。所有检索留痕（查询式/通道/日期/结果）。任何通道命中实质先例 → 作废或深挖到无先例子层。
> 初始检索日期：2026-08-30；关键纠正检索：2026-08-31。

## P1 演化史

### P1-a 原假设：尾流偏航功率函数次模 ⇒ 贪心 (1−1/e) 保证
- 状态：**作废（被符号分析推翻，非被检索推翻）**
- 检索通道与结果（2026-08-30）：
  1. web_search "submodular wind farm optimization greedy approximation guarantee wake steering" → 命中 **Zhang et al. 2011 (Renewable Energy)「turbine positioning 的次模性+lazy greedy」** 及后续（Chen, Wang 等 2014-2019）。→ 结论：**排布(micro-siting)问题次模性已被充分研究**；但检索到的全部文献均针对"加装风机"，无一针对"偏航角优化"。
  2. web_search "submodularity yaw angle turbine wake power function" → 无偏航次模文献。
  3. arXiv API `all:"submodular" AND all:"wind farm"` → **0 命中**。
  4. arXiv API `all:"submodular" AND all:"yaw"` → **0 命中**。
  5. OpenAlex fulltext `"submodular" AND "wake steering"` → 仅 2 篇，均为 layout 优化。
  6. 中文检索 "风电场 偏航优化 次模 贪心 近似比" → 仅命中排布优化与综述；偏航方法列表（遍历/梯度/遗传/数据驱动/对策论/神经网络）无次模。
- **自我证伪（符号分析）**：对线性叠加高斯尾流 P=Σcos^p(γj)(1−Σw)³ 求混合偏导 ∂²P/∂γi∂γj，交叉项 +6u·u'ᵢ·u'ⱼ>0 ⇒ 决策**互补**而非替代 ⇒ 次模性假设**不成立**。SOSFS 叠加下同样为正。⇒ P1-a 作废。

### P1-b 新假设：偏航决策的互补/替代"相结构"（主攻点）
- **核心命题**：∂²P/∂γi∂γj = Σ_{共享下游 k} C_ijk（互补项，恒>0）− S_ij·1{j∈D(i)}（替代项，恒>0）。符号由尾流作用图（DAG）拓扑决定：纯串列两机→替代；同排共享下游→互补；一般对→两力平衡。
- **为什么无人提过**：偏航优化的结构分析文献只讨论凸性/多模态（Laizet 2023、Park&Law SCP），游戏论文献用势博弈（Marden 2013）设计效用，无人计算混合偏导结构/符号矩阵，无人给出互补-替代相变条件。
- 检索（2026-08-30）：
  1. web_search `"supermodular" OR "strategic complements" wind turbine yaw OR "wake steering"` → 无结构分析先例（命中均为联合控制模式互补 yaw+TSR/induction，属"控制模态组合"，非"机组间决策结构"）。
  2. arXiv `all:"supermodular" AND all:"wind"` → **0 命中**。
  3. web_search `"strategic substitutes" wind farm yaw` → 仅经济学通论，无风电应用。
  4. web_search `Topkis / increasing differences / lattice + wind farm` → 无。
  5. web_search `"mixed partial" / "interaction structure" wind farm power yaw` → 无（只有"not guaranteed convex"式定性表述）。
- 关联先例（定位用，非冲突）：WES 2025 "Integer programming for optimal yaw control"（Bestehorn et al.）证明通用 WFYP 强 NP-hard 不可近似 ⇒ 本工作的正面结构结果与其形成"通用难 vs 物理类易"的互补叙事，需在文中精确引用并区分。
- **状态：存活，进入数值验证阶段。**

## 审计通道可用性（环境盘点）
- arXiv API / OpenAlex / Crossref：经 fetch_page 可达 ✓
- OEIS：经 fetch_page 可达 ✓（数学查重）
- GitHub code search：gh api ✓
- web_search：中英 ✓
- LLM API：✗（无 key）→ 实验路线定为"解析+FLORIS 数值"

## 复现基准（与承泽项目对齐）
- FLORIS 4.6.6, default_inputs.yaml (GCH: gauss velocity, gauss deflection, sosfs, crespo_hernandez TI), NREL 5MW, 8 m/s, TI=0.06, WD=270°:
  - 两机 5D 串列：P0=2190.40 kW；+25°=2368.39 kW（+8.13%）✓ 与项目 2190.39/2368.40 一致
  - 3×3（顺风 5D×横向 3D）：P0=8095.15 ✓；row1+30 → +14.87% ✓；rows12+30 → +22.73% ✓；[30,20,0] → +24.04% ✓
- 项目脚本 confirm 配置一致（generate_data.py / generate_array_data.py）。

## 论文二/三 算法侧审计（2026-08-30 补充）
- `"coordinate descent" OR "Jacobi" OR "parallel" yaw optimization` → 命中 **Kuo et al. 2020, Energies 13(4):865 (WGWD)**：几何尾流重叠加权图解耦 + 并行随机搜索。→ 与我方区别：权重是几何重叠而非目标函数混合偏导；子求解器是无证书随机搜索；无符号区分。已在 Paper 2 正面引用并区分。
- `wind farm power tracking yaw inverse bisection monotonic` → 当时仅定位到 APC 文献（Tamaro et al. 2025、Quick 2021）。**此条已被 2026-08-31 第四轮审计补正并取代**：检出 Starke et al. 2023、Oudich et al. 2023、Sterle et al. 2024 和 Tamaro et al. 2026 等实质相邻/直接先例；见文末 P3 更正记录。
- 并行坐标下降/坐标下降理论（Richtárik & Takáč; Wright 2015）为通用算法基座，作为方法学引用，不构成创新点冲突。

## 终局复核（2026-08-30，成稿后第三轮）
- EN 新措辞：`"strategic complements" OR "strategic substitutes" wake steering yaw` → 0 相关命中（仅无关的尾流控制论文）。经济学词汇在偏航领域确无先例使用。
- ZH 通道：`偏航优化 风电场 混合偏导 交互 互补 替代 解耦` → 仅命中 DFIG 电气解耦（电力电子，与尾流控制无关）。
- 代码通道：GitHub code search 因 gh 令牌失效未执行（环境问题，待用户重连）；网页替代检索 `github wake steering interaction matrix hessian` → 无结构分析先例，仅有 BFGS 拟牛顿（优化器用途，非结构发现）。
- 该轮当时的结论后来被 P3 第四轮检索部分推翻：C−S 相结构与最优点解耦的检索结论仍需独立复查，但“逆问题射线单调 + 二分反演”不能再被列为已无先例的核心创新；见文末 P3 更正记录。

## GitHub 代码通道补完（2026-08-31，gh 重连后）
查询集（gh api search/code，全部 code 索引）：
1. "sign matrix" "wake steering" → 0
2. "submodular" "wind farm" yaw → 0
3. "strategic complements" "wake steering" → 0
4. "strategic substitutes" wind turbine → 0
5. "Jacobi" "yaw" "wake steering" → 0
6. "power tracking" yaw "bisection" → 0
7. "mixed partial" "wind farm" → 0
全部 0 命中 → 代码通道无先例实现。

## 实验锚定文献核实（2026-08-31）
- Fleming et al. 2017, WES 2:229（首次海上现场尾流转向试验）doi:10.5194/wes-2-229-2017 ✓
- Fleming et al. 2019, WES 4:273（商用风电场现场试验 Part 1）doi:10.5194/wes-4-273-2019 ✓
- Fleming et al. 2020, WES 5:945（Part 2）doi:10.5194/wes-5-945-2020 ✓
- Simley et al. 2021, WES 6:1427（风速依赖性现场试验）doi:10.5194/wes-6-1427-2021 ✓
- Doekemeijer et al. 2020, Renewable Energy（FLORIS 闭环时变来流）doi:10.1016/j.renene.2020.04.007 ✓
- Bastankhah & Porté-Agel 2016, JFM 806（偏航尾流风洞实测）doi:10.1017/jfm.2016.595（论文一 ref 14）✓

## v2 实验补充（2026-08-31）：新数值口径
- 重跑 12 随机布局贪心基准（修正排序轴 bug + 修正 SLSQP 目标函数单位 W→kW）：均值 gap 0.103%、最大 0.477%（旧 0.019%/0.545% 因基线较弱弃用；新口径更严格、结论不变）。
- 模型稳健性扩展：cc（LES 标定）符号翻转复现 +0.388→−0.154；empirical_gauss（Sedini 现场标定）翻转复现 +0.022→−0.114，但其 5D 尾流弱（2T 增益≈0、od/diag 原点即 0.066→最优 0.085）——弱尾流区解耦"平凡成立"而非"涌现"，论文一 §9.2 如实区分两个区制。
- AEP：12 方向风玫瑰 +7.28%。
- 风速扫描 6–10 m/s：gauss 增益 +28.4→+21.5%，解耦比最优处 0.020–0.147 全部 ≤0.15。
- 论文三旧版复跑（历史记录，**不是当前 Table 2 比较**）：二分反演误差 1e-5–1e-7 kW；双线性代理 60.2783 kW（0.6003% Pmax）。当前匹配九目标协议见文末：最大 Brent 残差 0.00078209 kW、五节点代理 51.89370 kW（0.51679% endpoint power）。

## P3 第四轮新颖性与证据等级更正（2026-08-31）

### 触发与结论
- 触发：对“偏航功率跟踪/射线反演/二分”主张进行重新联网检索，并按原始页或 Crossref 元数据复核。
- **结论：P3 原先的宽泛创新叙事作废。** “偏航功率跟踪”“通过 yaw 扩展储备/跟踪范围”“功率目标下的 yaw setpoint 调度”均已有直接实质先例；不能再声称领域回避该问题、这是第一种 yaw power-tracking scheme、或静态数值扫描构成 well-posedness certificate。

### 本轮查询与命中
1. `"Yaw-Augmented Control for Wind Farm Power Tracking" 2023 Starke Meneveau King Gayme`
   - **Starke, Meneveau, King, and Gayme (ACC 2023)**, *Yaw-Augmented Control for Wind Farm Power Tracking*, pp. 184–191, DOI [10.23919/ACC55779.2023.10156444](https://api.crossref.org/works/10.23919/ACC55779.2023.10156444).
   - IEEE/OSTI 摘要明确：动态 yaw outer loop 加 pitch inner loop，在 LES 风电场跟踪两条功率轨迹。它直接反驳“yaw power tracking 不存在”的说法。
2. `"Providing power reserve for secondary grid frequency regulation of offshore wind farms through yaw control"`
   - **Oudich, Gyselinck, De Belie, and Kinnaert (2023)**, *Wind Energy* 26, 850–873, DOI [10.1002/we.2845](https://api.crossref.org/works/10.1002/we.2845).
   - 静态 wake model + FAST.Farm 瞬态评估，用分布式 yaw 优化考察 FRR 的功率储备与响应时间；是 P3 “静态 yaw/储备”层面的直接近邻。
3. `"Model predictive control of wakes for wind farm power tracking" Sterle Hans Raisch`
   - **Sterle, Hans, and Raisch (2024)**, *Journal of Physics: Conference Series* 2767, 032005, DOI [10.1088/1742-6596/2767/3/032005](https://api.crossref.org/works/10.1088/1742-6596/2767/3/032005).
   - 在线 MPC 用 yaw 与 axial induction 追踪 reference，含尾流动态与实时能力论证；是比 P3 更宽的动态控制先例。
4. `wind farm yaw power setpoint tracking pitch induction dynamic control reference 2020 2026`
   - **Tamaro, Campagnolo, and Bottasso (2025)**, *Wind Energy Science* 10, 2705–2728, DOI [10.5194/wes-10-2705-2025](https://wes.copernicus.org/articles/10/2705/2025/): yaw+induction、离线 setpoint scheduler 与 PI 闭环，在 LES-ALM 下比较 APC。
   - **Tamaro, Bortolin, Campagnolo, Mühle, and Bottasso (2026)**, *Wind Energy Science* 11, 1607–1630, DOI [10.5194/wes-11-1607-2026](https://wes.copernicus.org/articles/11/1607/2026/): 最大储备 APC 的缩比风洞验证，含动态风向、功率跟踪、疲劳和执行器占空比。这是当前日期下必须引用的最新直接 WES 工作。
5. `"wind farm power tracking" yaw control inverse monotonicity bisection`、`"inverse" "yaw" "power target" wind farm wake steering`
   - 本轮未检出把“已证明严格单调的静态 yaw profile ray”与标量逆映射联合作为核心贡献的直接文献；但检索受查询/索引范围限制，**不能把未命中写成 first/不存在**。

### 自我证伪：P3 的数学与实验表述
- 现有 `THEORY.md` 不包含对九机 FLORIS ray 的连续单调性证明；原稿将 41 个节点的非递减误写成 certificate。数值发现不等于定理，已按 interaction-structure-miner 的“诚实边界”降级为有限网格 screen。
- 原稿的全区间 inverse-Lipschitz 和 ``K-monotone'' 表述没有在该仓库中找到可审计推导。尤其导数下界 $c>0$ 是 inverse-Lipschitz 的前提，不能由离散 trace 推出；这些无支撑主张已从 P3 删除。
- 即使连续性给出端点间至少一个根，单调性只负责唯一性；Brent/bisection 的根搜索与“唯一 inverse map”不能混为一谈。
- 当前 41 点与 401 点 trace 都只支持一个 FLORIS 4.6.6、8 m/s、TI=0.06、wd=270° 的数值观察。401 点最小相邻增量为 0.231771 kW；它不是连续导数的下界或验证式证明。

### 当前可复现数字与公平性
- `expcache/ray_monotonicity.json`：41 点 operational screen 和 401 点 retrospective diagnostic，均明确标为 finite-grid evidence。
- `expcache/table2_tracking.json` 与 `proxy_tracking_benchmark.json`：同一个预先定义的九个**内部** targets（观测端点增益的 5%–99%，8192.46–10021.99 kW）。
- 端点为 $P_0=8095.147893676136$ kW、$P_1=10041.457351172001$ kW；不得把内部九点称为完整 attainable range。
- 当前同网格最大残差：Brent $0.0007820919527148362$ kW；五节点 proxy $51.89370445068744$ kW，即端点功率的 $0.5167945511876381$%。图 C1/C3/C4 读取同一缓存；生成 C4 前对 target arrays 做 exact equality assertion。
- 此处只可称 implementation-specific accuracy comparison。proxy 的五个离线节点与 Brent 的每目标 7–11 次 evaluator calls 不是 matched online budget，故不得声称速度/实时性优势。

### 处置与剩余风险
- P3 已改为“static ray-inversion benchmark”的诚实定位，并正面引用 Oudich、Starke、Sterle 与 Tamaro 的工作。
- **投稿闸门：当前 P3 不应作为独立 WES 研究论文提交。** 若要恢复独立稿件资格，至少需要：(a) 可审计的解析或 validated-numerics 连续单调性/唯一性结果，且明确模型域；(b) 跨布局、来流、模型和不确定性的预注册测试；(c) 与有动态、负载和执行器约束的 APC 基线进行同口径比较；(d) 在完成这些工作后重新执行六通道新颖性审计。
- 这不会自动推翻 P1/P2，但 P1/P2 的定理、数值范围、比较基线和新颖性也必须各自独立再审，不能借用 P3 的旧结论。

---

## P1/P2 forensic novelty correction (2026-08-31)

### Decision

**P1 and P2 are withdrawn as research-paper candidates.** This decision is not based on a claim that no useful future question remains. It follows because their old contribution statements cannot survive the combined mathematical and prior-art audit. The detailed evidence and reproducible script are in `P1_P2_FORENSIC_STATUS.md` and `ws_submodularity/p1_p2_forensic_audit.py`.

### Why P1 cannot retain its old novelty framing

The old P1 novelty statement depended on claiming a complement–substitute decomposition and a phase transition for FLORIS GCH. The analytical map actually assumed separable single-source kernels, a fixed directed graph, and recovery monotonicity. GCH includes yaw-added recovery and secondary steering (King et al. 2021, doi:10.5194/wes-6-701-2021), so it cannot honestly be presented as that toy model's special case without a new dependency proof. A reproducible lateral-offset GCH counterexample also fails the automatic recovery-monotonicity premise. The old headline finite-difference phase flip reverses sign under step refinement. Thus there is no validated GCH structural result left to characterize as a novel interaction law.

This does **not** mean that no conditional mathematical theorem could be novel. It means a future author must first formulate and prove one under explicit conditions, distinguish it from GCH behavior, validate derivatives and domains, and only then restart the novelty audit. Literature absence from a narrow phrase query is not enough.

### Direct P2 antecedents and misattribution correction

The previous dossier inaccurately attributed a weighted-graph wake-decoupling method to Kuo et al. (2020). Kuo's cited title is *Wind Farm Yaw Optimization via Random Search Algorithm*; it cannot support WGWD/decoupling attribution.

The renewed DOI-level audit found these direct P2-relevant antecedents:

| source | verified contribution relevant to former P2 | consequence |
|---|---|---|
| Shu, Song & Hoon Joo (2022), *Applied Energy* 306, 117986, doi:[10.1016/j.apenergy.2021.117986](https://doi.org/10.1016/j.apenergy.2021.117986) | sparsified wake directed graph, decentralised optimization, and clusters | precludes broad `first decentralized clustering` language |
| Li et al. (2025), *International Journal of Green Energy* 22, 2826–2841, doi:[10.1080/15435075.2025.2472291](https://doi.org/10.1080/15435075.2025.2472291) | weighted graph wake decoupling and parallel subproblems | precludes WGWD-style novelty or attribution to Kuo |
| Tu et al. (2026), *Applied Energy* 406, 127259, doi:[10.1016/j.apenergy.2025.127259](https://doi.org/10.1016/j.apenergy.2025.127259) | generalized serial refinement for large-scale wake steering | requires substantive distinction from serial/grid refinement |
| Gori, Laizet & Wynn (2023), *Wind Energy Science* 8, 1425–1443, doi:[10.5194/wes-8-1425-2023](https://doi.org/10.5194/wes-8-1425-2023) | optimization sensitivity to model and implementation | prevents sweeping algorithmic conclusions from a small static screen |

The former P2 implementation is also a cyclic Gauss–Seidel sweep rather than the claimed frozen-state Jacobi method, so its prior-art comparison was framed around an algorithm it did not implement. A future P2 novelty statement would require a genuinely specified and tested algorithm plus a fresh search against these and newer results.

### Evidence-status discipline

- A web/arXiv/OpenAlex/code zero-hit record is only a dated search result, never evidence of global novelty.
- A finite sample of mixed partials is not a global interaction bound; it cannot establish a guarantee or make a clustering method distinct through a certificate.
- An apparent common final grid point of two update rules is not an algorithm-equivalence result.
- P1/P2 retain no `first`, `law`, `theorem`, `certificate`, `guarantee`, `proven`, or submission-ready novelty claim.

### Remaining search obligation

Any genuinely new topic must be searched again **after** its model, proof, implementation, and comparison protocol are fixed. The search must include date-stamped web and scholarly-index queries, DOI verification, direct source reading, code/repository search where relevant, and explicit coverage of the closest current papers rather than a list of generic background citations.
