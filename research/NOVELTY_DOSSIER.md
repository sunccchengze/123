# NOVELTY_DOSSIER — 新颖性审计档案

> 审计原则：候选点的"新颖"是待证伪假设。所有检索留痕（查询式/通道/日期/结果）。任何通道命中实质先例 → 作废或深挖到无先例子层。
> 日期：2026-08-30（全部检索当日执行）

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
- `wind farm power tracking yaw inverse bisection monotonic` → 命中 APC 文献（Tamaro et al. 2025, WES 10:2705：yaw/induction setpoint 查表 + PI 闭环；Quick 2021 setpoint uncertainty）。→ 均无逆映射单调性结构分析/精确反演。已在 Paper 3 引用并区分。
- 并行坐标下降/坐标下降理论（Richtárik & Takáč; Wright 2015）为通用算法基座，作为方法学引用，不构成创新点冲突。

## 终局复核（2026-08-30，成稿后第三轮）
- EN 新措辞：`"strategic complements" OR "strategic substitutes" wake steering yaw` → 0 相关命中（仅无关的尾流控制论文）。经济学词汇在偏航领域确无先例使用。
- ZH 通道：`偏航优化 风电场 混合偏导 交互 互补 替代 解耦` → 仅命中 DFIG 电气解耦（电力电子，与尾流控制无关）。
- 代码通道：GitHub code search 因 gh 令牌失效未执行（环境问题，待用户重连）；网页替代检索 `github wake steering interaction matrix hessian` → 无结构分析先例，仅有 BFGS 拟牛顿（优化器用途，非结构发现）。
- 结论不变：核心三创新点（C−S 相结构 / 最优点解耦 + 交互能界 / 逆问题射线单调 + 二分反演）在全部已执行通道上无先例；相邻文献全部定位、引用并区分（详见前两节）。

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
- 论文三数字复跑确认：二分反演误差 1e-5–1e-7 kW；双线性代理 60.2783 kW（0.6003% Pmax）。
