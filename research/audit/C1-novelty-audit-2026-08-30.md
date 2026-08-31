# C1 新颖性审计日志（2026-08-30）

候选主张：风电场风机行 = 可激介质（阈值点火 + 不应期 + 脉冲传播 + 传导阻滞 + 除颤）

| # | 引擎 | 查询 | 命中 | 裁决 |
|---|------|------|------|------|
| 1 | web_search | "excitable medium" wind farm turbines wake | 5（均为一般尾流/中保真模型论文，无"可激介质"概念） | 零命中 |
| 2 | arXiv API | "excitable medium" AND "wind farm" | 0 | 零命中 |
| 3 | web_search | hysteresis path dependence "wake steering" | 5（"hysteresis"指**控制防抖**，非场物理路径依赖） | 本概念零命中；措辞需规避 |
| 4 | web_search | "information bottleneck" wind turbine wake control | 0 | 零命中（C3 候选存活） |
| 5 | web_search | "hormesis" OR "hormetic" wind turbine wake mixing perturbation | 5（无毒理增强概念） | 零命中 |
| 6 | web_search | "optimal transport" wake steering wind farm | 5（均为贝叶斯/LES 优化） | 零命中 |
| 7 | web_search | "active inference" OR "free energy principle" wind farm | 1（Reddit 讨论，无学术文献） | 零学术命中 |
| 8 | web_search | "Fisher information" OR "information geometry" wind turbine wake | 1（GitHub topic 无关） | 零命中 |
| 9 | web_search | "fluctuation theorem" OR "stochastic thermodynamics" wind turbine | 5（均为湍流级联 FT，非风机） | 零命中 |
| 10 | web_search | "topological" protection invariant wind farm wake steering | 1（拓扑预测尾流的科普博客 → 尾流拓扑学已存在，C5 降级） | C5 降级 |
| 11 | web_search | "chirality" OR "chiral" wind turbine array wake asymmetric | 5（活性粒子/声学/化学，无风电场） | 零命中（C6 存活） |
| 12 | web_search | "Riemannian" OR "geometric" optimization yaw wake steering manifold | 5（均为 ML/机器人） | 零命中 |
| 13 | web_search | "early warning signals" OR "critical transition" wind farm yaw | 5（均为生态/气候 EWS） | 零命中（C29 存活） |
| 14 | web_search | "Lévy" OR "superdiffusion" wind turbine wake meander | 5（均为宇宙线） | 零命中 |
| 15 | web_search | "action potential" OR "nerve impulse" OR "spike" propagation wind turbine wake row | 5（全神经科学） | 零命中 |
| 16 | web_search | "refractory" wind turbine wake recovery period conduction | 1（生理学教材） | 零命中 |
| 17 | web_search | "conduction block" OR "defibrillation" wind farm turbine | 2（全心脏医学） | 零命中 |
| 18 | web_search | "tipping point" wind farm operation control stability | 5（能源政策新闻） | 零命中 |
| 19 | web_search | "FitzHugh" OR "Hodgkin-Huxley" wind turbine OR wind farm | 5（"Huxley Hill" 风电场名巧合） | 零命中 |
| 20 | web_search | synchronization wind turbine wake coupled oscillators array | 发现 arXiv:2605.25192（Kuramoto **电网频率**同步，非气动尾流） | 机制不同，C1 不受影响 |
| 21 | web_search | wake deficit traveling wave turbine row propagation pulse | 5（单风机非定常尾流行波，无阵列阈值脉冲） | 机制不同，C1 不受影响 |
| 22 | web_search（中文） | 风电场 尾流 动作电位 不应期 可激 脉冲传播 | 5（全神经教育页） | 零命中 |
| 23 | arXiv API | "excitable" AND "wind turbine" | 60（全部为 excitation 振动激发，词干误配） | 零真命中 |
| 24 | arXiv API | "refractory" AND "turbine" | 40（全部为难熔合金 RHEA） | 零真命中 |
| 25 | arXiv API | "action potential" AND "wind turbine" | 0 | 零命中 |
| 26 | arXiv API | "integrate and fire" AND "wake" | 40（全部神经科学 sleep/wake） | 零真命中 |

## 第三轮：针对"具体新发现声明"的审计

| # | 引擎 | 查询 | 命中 | 裁决 |
|---|------|------|------|------|
| 27 | web_search | "cut-in cycling" wind turbine row synchronized pattern wake on-off oscillation | 5（Helix/DIC 同步控制：切入之上的受控周期；无近切入集体动力学） | 本概念零命中 |
| 28 | web_search | "spontaneous oscillation" OR "self-sustained oscillation" wind farm wake near cut-in | 5 | 零命中 |
| 29 | web_search | wind turbine "on-off" cycling "phase" locked row wake spacing "period" power | 发现 EPL 2016 相位锁定论文（功率涨落相位，非 on/off 态） | 必须引用区分 |
| 30 | web_search（中文） | 风机 切入 循环 振荡 阵列 同步 尾流 | 5（功率曲线科普+次同步振荡） | 零命中 |

## 最近邻文献（论文中必须引用并明确区分）

1. **Jensen et al., PNAS 116:10687 (2019)** — "Wind farm power optimization through wake steering"
   已记载：低风速下单风机在 cut-in 附近振荡（尾流+阵风致）；wake steering 降低 off-rate。
   **区别**：无行级集体动力学、无周期图案选择、无相位锁定颤振、无传播级联。
2. **Anvari, Wächter, Peinke, EPL 116:60009 (2016)** — "Phase locking of wind turbines leads to intermittent power production"
   已记载：大气边界层相关湍流致风机功率涨落相位锁定 → 间歇性。
   **区别**：对象是"功率涨落相位"（连续变量相关），非"on/off 离散态"；机制是大气相关，非尾流平流延迟；无周期=L/U 的延迟锁定极限环。
3. **Korb et al. 2023 / van Vondelen et al. 2024-25 (Helix/DIC 同步控制)** — 控制强制周期（切入之上，桨距激励）。
   **区别**：受控 vs 自持；周期=控制频率 vs 尾流平流时间。
4. **arXiv:2605.25192 (2026)** — 耦合风机 Kuramoto 电网频率同步。
   **区别**：电气相角 vs 气动 on/off 态。

## 精化后的新颖性主张（最终版）

在**近切入风速区间**，风电场风机行呈现**集合可激动力学**，具体包括五项此前未见的现象：
(a) 离散的 on/off **周期图案选择**（随间距变化）
(b) **相位锁定颤振**（"心动过缓节律"）：确定性极限环，周期 = 尾流平流时间 L/U
(c) **单向传播的点火级联**（阵风锋触发，沿列向下游传播，存在衰减/阻滞）
(d) **功率共振**：低风速区间场总功率随间距非单调
(e) **除颤协议**：协调推力脉冲可使行重新同步

以上 (a)-(e) 在全部 30 项审计中零命中。主张措辞："to the best of our knowledge"。

## 诚实性声明

索引未覆盖的付费墙文献在原理上无法排除。论文中使用 "to the best of our knowledge" 规范措辞，
本日志随论文数据仓库公开，供审稿人复核。

## 第一轮数值结果（T=1600-2000s，后经长时程复核修订）

- S1（T=1600）：L/D=4 图案 "100100000hhh…"，下游 26% 颤振；L/D 扫描功率非单调（8D 峰 1.623，10D 谷 1.499，12D 2.510 MW）
- S2（T=2000）：阵风（A=+0.8）触发上游点火级联 t2@775→t3@856→t4@1078→t5@1186→t6@1294；t7-24 出现等间隔 129.5s≈L/U 点火列
- S3（T=2000）：负阵风谷引发同步停机波（t811.5: t9-24 同时停）
- S4（T=2000）：除颤脉冲 0.466→0.491 MW（+5.4%）
⚠️ 注：N=24 行初始条件传播到底端需 ~3050s，上述 T=1600-2000s 结果可能含初始弛豫成分。
T=6000s 复核结果见 `results_v2.json` 与论文 §3。
