# SELF_AUDIT — 反省与复核日志

> **当前覆盖结论（2026-08-31 forensic round）：** 审计点 #9 已推翻 P1/P2 的旧投稿候选状态；它们现为不可投稿的非投稿取证记录。早期审计点中任何“P1/P2 核心贡献存活”“证书成立”“DJS 为 Jacobi”“可投”措辞均已被 #9 覆盖，保留仅为可追溯历史。P3 的独立投稿资格已由 #8 撤销。权威状态见 `P1_P2_FORENSIC_STATUS.md` 与 `SUMMARY.md`。
>
> 用户规则：每当觉得"挺厉害了/有点自负"时，必须停下来反省：我做的真的是全世界没人碰过的吗？真的能投顶刊吗？

## 审计点 #1（2026-08-30 凌晨，理论成形时）

**当时的自负**：认为"偏航决策互补/替代相结构"已是完整发现，可以动笔。

**反省动作**：
1. 重查 arXiv/OpenAlex/Web 各通道（supermodular/submodular/Hessian/diminishing returns/interaction matrix/mixed partial + wind/yaw/wake）→ 零结构分析先例；但发现**边界邻域**必须精确引用并区分：
   - Zhang 2011 等：排布问题的次模性（不同问题，不同决策变量）；
   - Stanley 2022 Boolean 贪心 / Fleming Serial-Refine：经验启发式，无结构理论；
   - Bestehorn 2025 (WES 10:1637)：通用 WFYP 强 NP-hard 不可近似——我的正面结果限定在物理模型类，文中必须正面处理该张力；
   - Starke 2023 (Wind Energy, graph-based dynamic yaw model)：已有"interconnection matrix Λ"（物理连接二元矩阵）——我的 Hessian 符号矩阵是不同对象（目标函数二阶结构），要明确区分并引用；
   - Wynn 2023 (WES 8:1425)、King 2021、Quick 2020：已观察"最优偏航随间距/TI 减小、行单调下降"——我的贡献是**机制理论**（C−S 分解 + Topkis 比较静态），不是原始观察，引用它们。
2. **自我证伪一例**：解析玩具模型在原点与 FLORIS 不一致（缺 yaw-added-recovery 线性项）→ 理论表述改为抽象核性质（r_ij≥0），不做参数级预测；
3. **自我证伪二例**：相图"可重入模式"在减小差分步长后发散 + FLORIS 负速度警告 → 判定为极端偏航角的模型边界伪影，**撤销该声明**，相图只保留稳健区域（γ≤25°）。
4. 复核数值：贪心-SLSQP 差（v2 基准：12 随机布局均值 0.103%、最大 0.477%，旧 0.019% 因基线较弱已弃用）与"最优点解耦"（od/diag 0.36→0.023）均已在多布局/多风向/AEP 下复现。

**结论**：核心贡献（C−S 交互分解定理 + 符号矩阵诊断 + 最优点解耦定律 + 有界交互贪心界 + 比较静态机制）目前在所有可触达通道中无先例；边界邻域已定位。继续，但论文中所有"首次"表述必须附检索边界与日期。

## 审计点 #2（待填：实验补充完成后）

## 审计点 #2（2026-08-30 深夜，三篇论文成稿后）

**当时的自负**：三篇论文 + 六张图 + 技能包，感觉任务完成度很高。

**反省动作**：
1. 对论文二、三的算法侧重新联网核查 → 发现两个必须引用的相邻先例：WGWD 2020（几何权重图解耦+并行随机搜索）与 APC 2025（yaw 功率跟踪查表+PI）。均已在文中正面区分：我方用的是目标函数混合偏导（带界），不是几何重叠权重；逆问题有单调性定理与精确反演，不是查表。**任何"解耦/跟踪"类表述都不得暗示这些工作不存在。**
2. 对"最优点解耦"再次检查：确认它只是经验定律（内点最优），机制只证了一半（stationarity identity），论文中如实写"conjecture + partial mechanism"——不吹成定理。
3. 对相图边界纪律再确认：≥25° 极端偏航（FLORIS 负速度）已从所有声明中排除；可重入模式已撤销。
4. 数字口径复核：论文一中的中心差分数值已与重算结果一致；两机 γ₂=30 边界行已标注排除。
5. 环境限制再确认：无法跑 LES/实测验证，论文中 Limitations 已写明"模型类上的结构，非流体物理定律"。

**结论**：核心创新点（互补/替代相结构 + 最优点解耦 + 交互能界 + 逆问题结构）经六通道审计仍无先例；相邻文献已全部定位并区分。三篇草稿目前是"结构完整、数值可复现、引用可核验"的状态，但距离投稿还差：作者信息、图注终稿、LaTeX 排版、引言文献补充（每篇约 5-10 条背景引用）、以及最重要的——**你（承泽）和指导老师的判断**。没有你的确认，我不会把它写成"已投稿"。

## 审计点 #3（2026-08-31，v2 实验扩充）

**当时的自负**：旧基准（贪心 gap 0.019%）数字已在论文里，以为直接补图即可收尾。

**反省动作**：
1. 重跑 12 随机布局贪心基准时发现 gap=+99.9%——追查发现两个 bug：①贪心排序轴用错（u=[cos wd, sin wd] 是侧向排序，应为流向量 [-sin wd, -cos wd]）；②SLSQP 目标函数返回瓦特而贪心返回千瓦，单位混用。修复后正确值：均值 gap 0.103%、最大 0.477%。**旧 0.019% 因基线较弱（单起点 SLSQP + 疑似同款排序问题）弃用**，全部论文/档案已替换为新口径。结论方向不变（贪心≈最优），数字变诚实。
2. empirical_gauss 模型补参数（turbulence=wake_induced_mixing + 关闭 secondary steering/transverse velocities）后，发现其 5D 尾流弱、3×3 最优处 od/diag 0.066→0.085（不降反升）——不是定律被违反，是弱尾流区"解耦平凡成立"。论文一 §9.2 改为如实区分两个区制，不 cherry-pick。
3. 4D 间距的 P(γ,0) 曲线在 γ≥25° 有抖动——落在声明的模型有效边界（负速度警告区）内，从拟凹性声明中排除并写明。
4. cos^p 拟合最初对两机总和取对数（不合式，p_fit=-0.78 无意义）——改为单机曲线上的精确 cos^1.88 自损律验证 + 农场曲线双通道展示。
5. GitHub 代码通道（gh code search）6 组查询全部 0 命中，已入档案。

**结论**：v2 全部实验数字在修复后复跑通过；论文一 §9（实验锚定+预注册协议）、论文二 §3/§5 新基准表、论文三图 1–4 与表 2 均以新口径为准。19 张图全部重新生成。

## 审计点 #4（2026-08-31 深夜，Supervisor-Skills 导师审查轮）

**当时的自负**：三篇 v2 定稿 + LaTeX 全稿，感觉"已经可投"。用户指示用 Supervisor-Skills 的导师技能再查一遍后，我一开始认为只会挑出排版措辞问题。

**反省动作**：
1. 调取 `pre-submission-reviewer` 规则书做机械扫描：em-dash/禁用词/长段/摘要结构逐项过——摘要五句、无"novel/innovative"类自夸词等已逐条核。
2. 参考文献作者与年份逐条上 OpenAlex/Crossref 核实（17+ 次查询）——发现 7 处归属/年份需修正，补 4 条（含 DJS 坐标下降引文 wright2015coordinate/richtarik2016parallel）。**教训：BibTeX 不能凭印象写，作者字段必须逐条核。**
3. 最重的一处：自查发现 **tab:m12 的 2-turbine 行是早期草稿格（−0.04/−0.19…），不是实测真值**。重新实测（h=5° 中心差分，FLORIS 4.6.6 GCH）：2-turbine 对 (0,0) 是严格零（r₁₂(0)=0），(0,10)=−0.002，(20,20)=−0.362，(30,20)=−0.081；3-chain 对应 +0.674/+0.230/−0.215/+0.058。已替换 .tex/.md。**教训：任何"先放草稿格、后补真值"的表格，收尾时必须逐格与实验缓存对账。**
4. tab:decoupling 原表口径混用（at-zero 一列来自旧实验、mid20 来自另一批）——写了专门重算脚本 `exp_decoupling_table.py` 以统一 h=5° 口径全量重算。新表与旧表差异显著（例 3×3 wd300 mid20 0.648→0.500；wd270 mid20 0.404→0.265；AEP 行 0.068/0.966→0.012/0.868）。摘要/contributions/表注/§5 叙述全部同步（0.27–0.97→0.22–0.87；0.022–0.068→0.008–0.069）。**教训：跨表数字只要口径变一处，全文所有引述必须 grep 一遍。**
5. random6 弱利区行：旧表写"0.174<0.181 即无下降"（两值不同），新口径下 opt=0.127 与 zero=0.127 严格相等——表述改为"gain +0.21% 的唯一无下降案例"（用增益作证据，而非比值差 0.000 的不可靠判据）。
6. 离线编译链（pdftex.js WASM + 垫片 copernicus_local.sty）三篇 0 error/0 undefined 通过——但**这只证明在垫片环境下无错**；正式投稿前必须用真实 copernicus.cls + amssymb/booktabs 在真 TeX 环境重编一遍（README 已写明，残余风险如实保留）。
7. 又抓到两处实质错误（数字对账+humanizer 双重检查的价值）：
   a. **论文三 Table 2 误差范围错**：文中写"1.3·10⁻⁵–3.9·10⁻⁴ kW、六数量级优于代理、同成本"。重跑 make_figures2.py 的 9 目标 bisection study（评估次数 8/8/7/7/8/8/9/9/11 与表完全一致）发现真值是 **1.5·10⁻⁶–7.8·10⁻⁴ kW（≈8·10⁻⁸ Pmax）**，且 60.28/7.8e-4 ≈ 7.7×10⁴ = **五数量级**而非六；代理 5 次网格评估 vs 二分 7–11 次，是"可比预算"而非"同成本"。摘要/§4/§5/结论/图注/md/SUMMARY 全部改真值。**教训：图脚本打印的中间结果就是表格真源，表必须与图脚本输出对账，不能凭旧文誊抄。**
   b. **QC 峰值网格分辨率**：论文一/三旧值"5D 峰 27°、6D 24°"是 1° 网格 argmax；0.5° 网格真值 26.5°/24.5°（0.1° 网格 26.6°），exp_inverse 打印"26°"是 `:.0f` 舍入假象。fig12/figC2 重画、论文三全部改 26.5°，并修掉了"峰在 γ≤25° 有效区内却引 26.5°"的自相矛盾句。
   c. **humanizer 技能抽查**：用户技能库 -SKILL- 最新分支 arena/01a048e7-skill 里找到 human-writing / behuman / content-humanizer（带 humanizer_scorer.py 实测脚本）。三篇摘要实测：paper1 89、paper2 91、paper3 79（被动语态 20% 偏高）→ 修掉 3 处被动后 paper3 升到 89；三篇均为 0 AI 词汇、0 hedge。behuman 明确声明不适用于技术写作，故不用于正文。

**结论**：本轮导师审查不是"锦上添花"，而是抓出了 2 处实质性错误（tab:m12 草稿格、tab:decoupling 口径混用）——恰好印证用户"别觉得进度挺厉害就停手"的规矩。三篇 .tex/.md 现以统一口径一致；push 后继续下一轮打磨。

## 审计点 #5（2026-08-31 深夜续，逐格数字对账轮）

**当时的自负**：表格已换真值，以为"数字对完了"。

**反省动作**（本轮把三篇论文里每一个数字都对着实验缓存/重跑核了一遍，抓到的问题）：发现论文二表 1 的 3×3 SLSQP gain 误写 +24.12（真值 24.13）；论文二摘要/贡献"rand16 gap≤0.005%、≤0.48%"与实测 −0.023% 冲突（已如实改写）；"per-row greedy 0.09%"实测为 0.07%；论文三摘要"误差≈10⁻⁷ kW"与可复现 study（1.5e-6–7.8e-4 kW）不符（已全改，并把"六数量级"修正为五数量级、"同成本"改为"可比预算"）；5×5 聚类墙时钟本轮重跑 62 s/346 s（原 60 s/317 s，墙钟随负载波动，已按新测值更新并注明）；Jiménez 0.042/0.319 无缓存 → 重测为 0.302→0.037（已替换并缓存）；TI 扫描 29.8/28.1/25.3/21.0/10.7/0.8 与三机链 [30,23.8,0]/[18.6,17.1,0]、32.0%/2.9% 全部精确复现（已缓存）；12 布局证书（均值 0.103/最大 0.477/界 0.12–7.05%）逐格对上；三篇摘要压至 246/237/239 词（WES ≤250）且 humanizer 实测 93/91/89 分、0 AI 词 0 hedge；三篇 .tex 补齐 correspondence/日期占位/copyright/code-availability/author-contribution/competing-interests（WES 必需）。

**另一件事**：push 途中 GitHub 令牌失效（git 与 gh 均 Bad credentials）。本地所有提交完好（唯一未推送提交为 h 口径统一及之后两个提交）；已停止重复尝试，等承泽在 Arena 重连 GitHub 后一次 push 全部。**教训：令牌失效不丢工作——本地 git 历史就是保险。**

## 审计点 #6（2026-08-31，WES 模板与图件复核）

**当时的自负**：认为离线 PDF 能编译、表格数字也已复算，就可以把三篇稿件称作“只差投稿”。

**反省动作**：

1. 对照 Copernicus 当前 manuscript-preparation 示例逐项检查源文件，发现三篇都把元数据放在 `\begin{document}` 前、把 author declarations 放在 appendix 前，并带有作者自定义命令、额外包和 P1 的自定义定理/proof/`\paragraph`。全部改为官方顺序，删除这些源级定义并用标准 LaTeX 内联符号；本地垫片只保留与真实类接口一致的兼容定义。**教训：垫片能编译不等于正式类允许该源文件。**
2. 逐张读取 19 个 PNG 的像素、density 与文件大小，发现原图大多只有 150 dpi，Fig. C4 更只有 100 dpi；`make_figures.py` 还含旧的 Fig. 3/6 硬编码，Fig. C4 没有生成链且标着过期 $4.18\times10^{-4}$ kW。重构为缓存驱动的图链，新增相图和 wd-$300^\circ$ Hessian 原始缓存；所有图以 300 dpi 重画且每张低于 5 MB。**教训：稿件数字、图中文字和作图脚本必须三向对账。**
3. 继续追溯 Fig. C4 的 60.28 kW，发现它来自旧的 8 目标 proxy 试验，而 Table 2/exact 图使用 9 个目标；在同一 9 目标上重算，proxy 最大误差为 **51.8937 kW（0.5168% $P_{\max}$）**，exact 最大误差为 **$7.8209\times10^{-4}$ kW**，比值 $6.64\times10^4$（约 4.8 个数量级）。`exp_inverse.py` 现把两边输入/结果写入版本化 JSON，并在绘图前拒绝不同目标格的比较。**教训：即使每个数各自为真，不同 benchmark grid 的“最大值”也不能直接比较。**
4. 再次核查 WES AI policy：其允许语言层面的 grammar/spelling/readability 辅助，却明确禁止用生成式 AI 生成论文文本或科学解释。本工作流含实质性生成辅助，不能通过一句虚假声明变为 WES 合规稿；必须由作者独立重写、重推导和重核验，或换允许透明披露的期刊。同时，真实 v7.15 类编译和有 DOI 的不可变代码/数据存档仍未完成。**教训：格式完成和科研/出版伦理合规是不同的验收门。**

**结论**：本轮提高了可追溯性和模板兼容性，但把投稿状态从“接近完成”诚实地改为“不可直接投稿”。后续不应以本地 shim、GitHub 工作分支或 AI 辅助文稿冒充 WES 最终投稿物。

## 审计点 #7（2026-08-31，WES 图文位置与回退 PDF 可视化复核）

**当时的自负**：以为只要把 `figure` 环境从 conclusions 后搬到正文，就已经满足 Copernicus 的“图和 caption 靠近首次提及”要求。

**反省动作**：

1. 做 source-level 索引后发现，原先 20 个 figure environment 虽然都有正文引用，但都集中在 conclusions 后；这直接违反官方 manuscript-preparation 指南。P1 的 12 张中还混入了属于 P2（DJS）和 P3（quasi-concavity）的重复结果图，若三篇分别投稿会造成不必要的自我重复。
2. 先将保留图移动到首次讨论段之后，并把 P1 手写的 `Figure 1/2/3` 和 Section 9 图号改为 `\ref`，以免浮动环境重排后引用失真。随后不把“源位置正确”误当成“成品排版正确”：第一次双遍 article+shim 编译的 PDF 仍把若干 `[t]` float 拖到文末。改用标准 LaTeX `[htbp]`，并在 P2 的 certificate、P3 的 bisection/proxy 图后使用 `\clearpage` 清空队列；重新渲染 PDF 后，所有图均在其后续 discussion/conclusions/bibliography 之前出现。这个可视化检查是回退链测试，不是官方 WES 类的证明。
3. P1 现只保留 10 张其自身的交互结构/稳健性图；DJS 图只在 P2，quasi-concavity 图只在 P3。P3 原来只有一个表，导致源码写的“Table 2”在实际输出中成为 Table 1；新增可复现的共同 benchmark Table 1（布局、风况、射线、九目标、Brent 与五节点 proxy 协议），使九目标结果真正成为 Table 2。这样 `table2_tracking.json` 的命名、正文、图注和 Markdown 不再互相矛盾。
4. 最终静态预检确认三篇均使用 `\documentclass[wes, manuscript]{copernicus}`、无作者额外 package/宏/`\paragraph`，作者邮箱一致；每一张保留图均在首次 `\ref` 之后、conclusions 之前。三篇各自两遍回退编译均为 0 LaTeX error、0 未定义引用和 0 未定义文献。P3 还直接断言 exact/proxy 的九个 target 数组逐项相同，最大误差为 $7.8209\times10^{-4}$ / 51.8937 kW，Fig. C4 为 1440$\times$1020 px、约 300 dpi。

**结论**：这一轮修的是出版对象的结构一致性，而不是新增科学证据。真实 `copernicus.cls` 编译、永久 DOI 存档、作者对交叉稿件重叠的判断，以及 WES 对生成式 AI 文本/解释的政策阻塞仍然存在；不能因本地 PDF 好看就把状态改写为“可直接投稿”。

## 审计点 #8（2026-08-31，用户追问“是否完全无法挑剔”后的第四轮反证）

**当时的自负**：P3 已有 Table 1/2、同格 proxy cache、41 点 trace 和本地 PDF，就把“inverse-monotonicity / well-posedness certificate”当成了可投的独立创新。

**反省动作与新发现**：

1. **直接先例漏检，且不是一个。** 重新检索并从 IEEE/OSTI、Crossref、WES 原文核验后，发现 Starke et al. (ACC 2023, doi:10.23919/ACC55779.2023.10156444) 已用动态 yaw outer loop + pitch inner loop 在 LES 中跟踪两条功率轨迹；Oudich et al. (Wind Energy 2023, doi:10.1002/we.2845) 已以 yaw 优化评估 FRR reserve；Sterle et al. (JPCS 2024, doi:10.1088/1742-6596/2767/3/032005) 已做 yaw+induction MPC power tracking；Tamaro et al. 的 WES 2025 及其 2026 缩比风洞 APC 论文（doi:10.5194/wes-11-1607-2026）均直接相关。原来的“领域回避 inverse / first yaw tracking / new operating mode”表述不可成立，全部撤销并在 `NOVELTY_DOSSIER.md` 留档。
2. **把采样当证明是实质性方法错误。** 仓库的 `THEORY.md` 没有九机 FLORIS ray 的连续单调性证明，也没有原稿声称的 `K-monotone` 推导。41 个非递减节点只能是 screen；额外复跑的 401 节点也只能提高同一模型/工况下的数值证据密度。它们均不能给出采样间连续单调、唯一根、导数下界或 inverse-Lipschitz certificate。原稿的“theorem / certificate / guaranteed”叙事已从 P3 删除。
3. **重新检查标量数学。** 连续响应的端点异号/夹值本身已足够让 bracketed root finder 找到一个根；严格单调才给唯一逆映射。此前把“可以 bracket root”和“已经定义唯一 inverse map”混为一谈。现在仅保留有明确前提的标准条件结论，不把它包装成新定理。
4. **重新检查比较设计。** 九个 8192--10022 kW 目标是端点增益的 5--99% 内部网格，不是完整端点区间 [8095.15, 10041.46] kW。五节点 proxy 的离线 5 次评估与 Brent 的每目标 7--11 次调用也不是同一在线预算；目前只报告同 targets 的 implementation-specific residual comparison，不声称速度、实时性或控制优越性。
5. **代码和图的防漂移整改。** `exp_inverse.py` 现在写入 `ray_monotonicity.json`（含 41 和 401 点 raw traces/解释）并将目标协议写入 proxy cache；`make_figures2.py` 的 C1/C3/C4 全部读取缓存，且在绘图前断言 exact/proxy targets 完全相同。复跑结果：最大 Brent residual $0.0007820919527148362$ kW；五节点 proxy $51.89370445068744$ kW（$0.5167945511876381$% endpoint power）；401 点最小相邻增量 0.231771 kW；两机故意 overshoot ray 的最小相邻增量 −2.933336 kW。
6. **写作审查不等于投稿合规。** 新建并执行 `scholarly-clarity-auditor` 规则：每句强断言按 proof/conditional/numerical/benchmark/interpretation 分类，检索 first/certificate/guarantee 等词，且不把“humanizer”当作规避 WES AI policy 的工具。P3 的英文 TeX/Markdown 已按该规则重写；作者仍必须独立重写、核验并决定其政策合规性。

**结论与处置**：P3 当前只能诚实地作为一个带完整缓存的“static ray-inversion benchmark”研究记录，**不能作为独立 WES 研究论文投稿**。要恢复投稿候选资格，必须先有可审计的解析/validated-numerics 单调性与唯一性结果、跨工况/模型/不确定性的严谨测试，以及与动态 APC 的同口径比较。P1/P2 不因 P3 以外的任何旧审计结论自动免检；下一轮应从它们的数学命题、先例和基线分别重审。

## 审计点 #9（2026-08-31，P1/P2 数学、代码语义与最新先例的取证式反证）

**当时的自负**：P3 已降级后，仍默认 P1 的 “C−S 分解/相变/交互能证书” 与 P2 的 “DJS/Jacobi/有保证聚类” 独立成立，只需补充引用和排版即可投 WES。

**反省动作与反证结果**：

1. **模型域被错误扩大。** 旧 P1 的推导把每个受体的赤字写成仅依赖源机自身偏航的可分核，并把 $-\partial w_{ij}/\partial\gamma_i\ge0$ 当成正偏航的自然性质；但 GCH 明确包含 yaw-added recovery 与 secondary steering。后者会使下游机的有效偏航/尾流受更上游偏航影响，故 GCH 不能诚实地被写成旧可分核模型的 special case。更严重的是，5D 串列、受体横向偏置 $-1D$ 的 FLORIS 4.6.6 可复现实例中，下游机固定 $0^\circ$，上游正偏航 $0^\circ\to5^\circ$ 时下游功率 **1651.808\to1605.633 kW（$-46.175$ kW）**。这不是现实风场的一般物理断言，但足以推翻“任意布局/单侧正偏航自动满足恢复单调性”的前提。
2. **旧相变的核心数值在收敛检验中反号。** 三机链旧 headline 点 $(20^\circ,20^\circ,20^\circ)$ 的 $M_{12}$：$h=5^\circ$ 为 $-0.215420$ kW deg$^{-2}$，$h=2.5^\circ$ 为 $-0.248412$，但 $h=1^\circ$ 为 $+0.022315$、$0.5^\circ$ 为 $+0.022367$、$0.25^\circ$ 为 $+0.022381$。因此早先将 $h=5^\circ$ 粗差分称为局部 Hessian 符号、phase flip 或理论验证是不成立的，已撤销。
3. **公式和单位也未达可投稿标准。** 旧直接替代项按 $j\succ i$ 写却声称适用于任意 $i\ne j$，与混合偏导的对称性不兼容；应先固定有向 pair 或加入两种有向项。解析三角导数是弧度导数，而数值表为 kW deg$^{-2}$；此前未明确转换。即便在理想可分模型里，平方和叠加也不能只用“$\phi$ 凸”推出共同受益项正，需要对具体 $\phi$ 连同负的 velocity cross-curvature 做完整不等式。
4. **“证书”不是证书。** 旧 Theorem 2 需要 yaw box 上的 $\sup|M_{ij}|$；程序只在原点加四个随机点采样。有限采样最多是启发式 envelope，不能给全局 gap、cluster loss 或 Jacobi contraction certificate。旧 P1 的 Law 1 也是选择性工作点的数值模式，并非定律。
5. **P2 的代码与算法名不一致。** `exp_djs.py:djs` 在 `ynew` 上就地更新：第 $i+1$ 个一维搜索已看到第 $i$ 个改动，实际是 cyclic Gauss--Seidel，不是论文所述 freeze-then-commit 的并行 Jacobi。取证脚本同条件重现：三机首轮 old in-place / true Jacobi 为 **3295.691 / 3267.736 kW**；3×3 为 **10042.514 / 9927.945 kW**。选定两例三轮后恰好到同一整数格状态，不能证明等价、收敛率、并行实现或时钟优势。
6. **P2 新颖性和归属进一步失败。** 旧稿把 Kuo et al. (2020) 的 random-search 误称为 WGWD。续检直接命中 Shu, Song & Hoon Joo (Applied Energy 2022, doi:10.1016/j.apenergy.2021.117986) 的 sparsified wake digraph + decentralized clusters；Li et al. (2025, doi:10.1080/15435075.2025.2472291) 的真正 WGWD + parallel subproblems；Tu et al. (Applied Energy 2026, doi:10.1016/j.apenergy.2025.127259) 的 generalized serial refinement。故“首个去中心化聚类/首个有机理优化器/首个 guarantee”不能保留。
7. **处置而非遮掩。** 已新增可复现的 `p1_p2_forensic_audit.py` 与 `expcache/p1_p2_forensic_audit.json`，并将 P1/P2 两个 `.tex/.md` 改为明确的 **non-submission forensic records**，移除原先假定可投稿的假定、定理、law、guarantee、certificate、first 叙事。原稿可由 Git 历史追溯，不能再作为对外 research claim 使用。`P1_P2_FORENSIC_STATUS.md` 记录证据、来源和未来重开门槛。

**结论**：P1、P2 与 P3 当前都**不能诚实地作为独立 WES 研究论文投稿**。P1/P2 不应以“补一句 limitations”挽救：需要新的明确定义模型、正确推导、validated derivatives/全局界、预声明的多工况与高保真实验，以及完成后再次作新颖性审计；P2 还须先实现它实际声称的同步并行算法并做 matched-budget 比较。WES 的生成式 AI 文本政策阻塞仍独立存在。此次结论是推进质量而非放弃证据：反例、错误代码语义和实质先例均被永久保留，而不是从仓库清除。

## 审计点 #10（2026-08-31，归档一致性、相邻引文与可复现性复核）

**当时的风险**：即使 #9 已发现 P1/P2 失效，旧的论文源、图脚本、理论摘要或 P3 对“companion interaction study”的措辞仍可能让读者误以为这些结论可被选择性复用；“能编译”也可能被误解为投稿合规。

**核验与处置**：

1. 将 P1、P2 源与 Markdown 改为明确的 `non-submission forensic record`，P3 改为明确的 `non-submission benchmark record`；删除 P3 以已撤销 P1 为物理/理论动机的说法。新增 `P1_P2_FORENSIC_STATUS.md`、`CLAIM_LEDGER_2026-08-31.md`、`ws_submodularity/ARCHIVE_NOTICE.md`，并把 `SUMMARY.md`、`IDEATION.md`、`RESEARCH_CHARTER.md`、`THEORY.md` 与 interaction-structure-miner 技能同步为当前状态。
2. 对旧实验/图脚本加了 archive headers，保留历史 raster/cache 而不篡改其生成时内容；明确它们只能做取证，不能作为 P1/P2 结论或 benchmark 证据。历史 `djs` 的函数 docstring 也改为 in-place cyclic Gauss--Seidel，避免仅靠函数名继续误导。
3. 重新逐条在 Crossref/官方页核验了 Shu 2022、Li 2025、Tu 2026 与 Fleming 2021 元数据；shared `refs.bib` 补入前四者。特别确认 Shu 的 Crossref 作者 family name 为 “Hoon Joo”、given name 为 “Young”，BibTeX 的 `Hoon Joo, Young` 是对应格式。Kuo random-search 与 WGWD 的错误归因不再留在当前论文叙事中。
4. 再次读取 Copernicus 官方 AI policy（https://publications.copernicus.org/for_authors/ai_policy.html）：它允许 grammar/readability 辅助，但明确说 generative AI 不能用于 manuscript text 或 interpretations。故本轮的本地 record 与 PDF 只可做归档/回归检查，不能被包装成 WES submission。
5. 从 `/tmp/p3-clean-venv/bin/python` 完整复跑正式取证脚本：FLORIS 4.6.6、恢复反例 $-46.17498450511289$ kW、$h=5^\circ/h=1^\circ$ 反号、两布局 first-sweep 语义差异均复现；输出 JSON SHA-256 仍为 `63d6cdfa6b8ce634aae266a2a2e1d881db10c50921898dbe335f9feae52b6850`。
6. 对所有改动的 Python 脚本做 `py_compile`；三个 source 做两遍 offline article+Copernicus-local 回退编译。三个 build 都为 **0 LaTex errors、0 undefined references、0 undefined citations、0 overfull boxes**。这只验证当前 shim 回归构建，不验证真实 Copernicus class、排版接受性、科学正确性或投稿资格。

**结论**：现在不会再由当前 README、摘要、源码、技能或可见历史脚本暗示 P1/P2/P3 可直接投稿。剩余风险不是“再润色一下”即可消除：真实类编译、不可变 DOI 存档、作者独立重写和各自的新科学计划仍未完成；P1/P2/P3 的投稿闸门维持关闭。
