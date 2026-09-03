# SPLEEN C1：公开证据、数据合同与新颖性淘汰审计（2026-09-01）

**对象：** von Karman Institute 的 *SPLEEN C1* high-speed low-pressure turbine linear cascade，以及其主 Zenodo 数据库 v5（record `13712768`）和独立 PIV 数据库（record `10253213`）。

**当前处置：** `Question candidate / only G0 passed; G1–G6 incomplete`。SPLEEN 是一个很有价值的公开、真实的高速度低压涡轮**气动—二次空气相互作用**试验体系；它目前不是已被证明具备温度、应力、位移、疲劳寿命或完整流—热—固 MDO 真值的体系，也不是一篇可立即投稿的 AI-MDO 路线。

**本审计回答的问题：** 在不虚构跨仪器配对、不把 AI 标签当成贡献、也不把不同实验体系拼成一台机器的前提下，SPLEEN C1 是否已提供一条可验证、可投稿的 AI 赋能叶轮机械 MDO 路线？

**简短答案：** 还没有。公开资料已足以确认真实的 cavity/purge/wake 气动对象、多个受控工况和丰富流动观测；但不能从这些事实推出完整 MDO，也不能使用以下宽泛主张：

- “首次发现/解释 purge–wake interaction”；
- “首次在 SPLEEN 上预测或优化 PMFR、损失或非定常二次流”；
- “首次以 AI/ML 改进 SPLEEN transition–turbulence closure”；
- “首次用 SPLEEN 做 steady off-design loss surrogate”；
- “以 SPLEEN 验证热—结构—寿命 MDO”。

这些方向已经被直接 SPLEEN 论文覆盖，或者超出了已证实的测量合同。尚未关闭的仅是一个**有待重新定义和逐项证实的窄问题**：若 archive 内文档能给出严格的 cavity/PMFR/wake/instrument/run 对应关系、足够的条件层级和独立留出组，能否构造一个不同于现有论文的、预注册的 aero–secondary-air **operating/measurement decision**。即便该问题最终成立，它也只能先称为气动—二次空气协同运行研究；除非另外获得同一对象的热/结构链条，不得称作全 MDO。

> 本文中“未证实”“未取得”只描述截至 2026-09-01 本审计访问到的公开页面、archive container 行为和本地可用传输路径。它不声称作者未采集数据、文件在任何其他位置不存在，或未来 revision 不会补齐缺口。

---

## 1. 版本、对象和访问范围

| 事实 | 证据类别 | 紧邻来源 | 本审计允许的结论 | 不能扩展成什么 |
|---|---|---|---|---|
| 主数据库 v5 是开放的 CC-BY 数据集，record `13712768`，ZIP advertised size 759.76 MiB（网页显示 796.7 MB）。 | 一手 record metadata。 | [Zenodo v5 record](https://zenodo.org/records/13712768)；[v5 API](https://zenodo.org/api/records/13712768)。 | 数据集公开可见，主 archive 是单个 ZIP。 | 不等同于本地已下载、已校验或逐文件审计。 |
| v5 描述的系列包括：flat endwall / no wake，flat endwall / wake，以及 cavity endwall / wake / purge。描述还列出 pressure、temperature、flow angles、Mach、pressure loss、unsteady blade/endwall pressure 与 quasi-shear-stress。 | 一手 record-level 描述。 | [Zenodo v5 record](https://zenodo.org/records/13712768)。 | 这些是发布者声明的仪器/工况范围。 | 不可推断每一个信号均存在于每一个 condition，或其可通过相同 run ID 直接 join。 |
| v5 notes 明示包含 investigated endwall-cavity geometry 和 secondary-air-system information；且 CAD v2 修正了 v1 CAD stagger-angle 错误。 | 一手版本说明。 | [Zenodo v5 record, Notes](https://zenodo.org/records/13712768)。 | cavity geometry 与 secondary-air documentation 的存在已被 record 元数据证实；后续几何应锁定修正版。 | 不应从错误的 v1 CAD 反推 v5 几何，也不能不查看文件就宣布其字段、单位或 cavity-family 数量。 |
| 早期 v1 record 明确警告 `SPLEENC1_Geometry_Airfoil_2D_CAD_v1` 的 IGES/STEP/Parasolid stagger angle 错误，但 XLSX coordinates 正确，并要求使用新版本中的 CAD v2。 | 一手 record metadata。 | [Zenodo v1 API](https://zenodo.org/api/records/7264762)。 | 存在具体且可追溯的 geometry revision risk。 | “v1 的所有数据都错误”或“v5 无任何版本风险”。 |
| PIV record `10253213` 是独立 CC-BY ZIP，针对同一 C1 cascade；它在 midspan upstream/passage blade-to-blade planes 和距 trailing edge 0.5 axial chord 的 outlet plane（靠近 endwall 的 0–18% span）测量。 | 一手 record metadata。 | [Zenodo PIV API](https://zenodo.org/api/records/10253213)。 | PIV 是同一 C1 体系的独立补充数据资产。 | PIV 的每个文件必然与 v5 任何一条 purge/wake run 成对。 |
| PIV record 明示其工况是 `Cavity Aref`、**without wake generator**、turbulence grid on/off。 | 一手 record metadata。 | [Zenodo PIV record](https://zenodo.org/records/10253213)。 | PIV 可作为 steady reference-cavity / turbulence-level 条件的流场验证资产。 | 不能充当 `WG-on + purge` 非定常系列的独立验证集。 |
| 本地 `urllib` 与 Node HTTPS Range 探测均在 TLS 握手/响应前失败；Zenodo `container` endpoint 可通过网页代理读到已知完整文件路径和部分 listing，但 `prefix`、`path`、`dir`、`page`、`size`、`offset` 查询没有产生经证实的过滤或分页。 | 本次环境的传输观察。 | 主 endpoint：[`/container`](https://zenodo.org/api/records/13712768/files/SPLEEN_HighSpeedTurbineCascade_Database_v5.zip/container)。 | 本环境尚未形成可审计的本地 archive binary 或全量 central-directory manifest。 | 不能称 Zenodo 不支持 Range、archive 不能下载，或文档/文件不存在。 |

### 1.1 已固定的真实物理对象

SPLEEN C1 是一台 23-blade、span 165 mm 的 high-speed linear cascade，代表 geared LPT 的 rotor-hub airfoil；公开测试案例论文给出真弦长 52.285 mm、轴向弦长 47.614 mm、pitch 32.950 mm、stagger 24.40° 等几何量，并说明 cavity/wake adaptation 的试验背景。[SPLEEN C1 test-case paper](https://doi.org/10.3390/ijtpp10010002) 的这一描述支持“同一个真实叶栅试验对象”，不支持将 linear cascade 等价为完整旋转发动机级。

论文也明确提醒线性叶栅的二次流不能完全代表发动机环境；这种几何/边界近似必须保留在任何后续论文的模型范围中。[同上](https://doi.org/10.3390/ijtpp10010002)

---

## 2. 可证实的数据合同与禁止推断

### 2.1 当前最强、但仍不完整的合同

以数据源已明确的控制量和可观测量表示，当前可以审慎写成：

\[
  q=\bigl(e,\,w,\,\mathrm{PMFR},\,M_{\rm out},\,Re_{\rm out},\,TI_{\rm in},\,f^+\bigr)
  \longmapsto
  y_{\rm aero}=\bigl(p,\,\beta,\,\gamma,\,\xi,\,\text{velocity/turbulence fields},\,p'(t),\,\tau_{w,\rm quasi}\bigr),
\]

其中：

- \(e\) 是经过**完整 geometry file 和对应表**验证后才能使用的 endwall/cavity configuration；目前只在 metadata/论文层面确认 flat endwall、cavity endwall 与 PIV 的 `Cavity Aref` 描述；
- \(w\) 是 wake-generator state；
- PMFR 是 purge mass-flow ratio；
- \(M_{\rm out}\)、\(Re_{\rm out}\)、\(TI_{\rm in}\)、\(f^+\) 的具体定义、参考面和不确定度必须以相应 README/技术说明为准；
- \(y_{\rm aero}\) 是流动、压力、损失、角度、湍流和准壁面剪切类观测，不包括未经证实的固体或寿命输出。

这个表达是一个**候选数据合同**，不是已获得二进制后验证的 schema。

### 2.2 论文级条件证据

| 条件/观测 | 一手或同行评议证据 | 本审计的正确用法 |
|---|---|---|
| steady PIV 的 \(M_{\rm out,is}=0.70,0.90,0.95\)，\(Re_{\rm out,is}=70,120\,k\)，以及 `TG` 对应约 2.40% / 无 `TG` 对应约 0.90% inlet turbulence | Okada et al., [*J. Turbomach.* 2024, DOI 10.1115/1.4063674](https://doi.org/10.1115/1.4063674)，其 test matrix 与 PIV record 一致。 | 用于确定 PIV 子集的已发表条件标签；不要把它扩展到所有 v5 文件。 |
| PIV B2B 与 COP 流场、Mach、flow angle、turbulence quantities；PIV 与 5HP/RANS 的比较 | [Okada et al.](https://doi.org/10.1115/1.4063674)。 | 是对该**steady PIV measurement/simulation comparison**的证据；不是 purge/wake transient holdout。 |
| wake generator 可实现 midspan \(f^+\approx0.95\)，并有 0–1% PMFR 的 purge facility range；2026 steady off-design study 中 WG 和 purge system 均为 off | Lopes et al., [*IJTPP* 2026, DOI 10.3390/ijtpp11010014](https://doi.org/10.3390/ijtpp11010014)。 | 证明设施/变量的存在和该文具体 steady 子集，不保证 archive 中每一个笛卡尔组合。 |
| `WG-on + cavity purge` 的时间平均气动实验在 \(M=0.90\)、\(Re=70k\)、\(f^+=0.95\) 下研究 cavity geometry 和两级 purge flow；测量 blade pressure、outlet deviation/loss 等 | Lopes et al., [*J. Turbomach.* 2024, DOI 10.1115/1.4063878](https://doi.org/10.1115/1.4063878)。 | 证明已发表的平均气动真值与直接的科学覆盖；不可仅从文章文字反演 archive file/run keys。 |
| `WG-on + cavity purge` 的 phase-averaged fast-response-probe 研究，在 \(M=0.90\)、\(Re=70k\)、\(f^+=0.95\) 和不同 PMFR 下，映射 outlet energy loss、TI 和 flow angles | Lopes & Lavagnoli, [*J. Turbomach.* 2025, DOI 10.1115/1.4067674](https://doi.org/10.1115/1.4067674)；其 publisher metadata/Crossref abstract。 | 证明非定常二次流对象已被直接研究；不替代未来方案所需的 frozen independent split。 |

### 2.3 当前禁止推断的量

下列量没有被上述公开记录证明为 SPLEEN 的同条件输出，因而不得放入该体系的 MDO objective/constraint：

\[
T_{\rm metal},\quad q''_{\rm solid},\quad \sigma_{\rm vm},\quad u_{\rm blade},\quad
\text{HCF/TMF/creep life},\quad \text{rotor stage efficiency},\quad \text{cycle fuel burn}.
\]

SPLEEN 主 record 出现 `temperature` 一词不能自动变成金属温度或 conjugate heat transfer (CHT) solid solution。线性叶栅的 aerodynamic/secondary-air truth 也不能仅凭共同题名与 NASA C3X、GE-E3/Pak-B、FAN-02、MEXICO 或其他项目拼接成新的多物理样本。

### 2.4 进入定量建模前必须找到的键

在 archive 内说明文件经逐文件审计之前，下表全部保持“未通过”。

| 必须项 | 当前状态 | 若缺失，哪些主张不可做 |
|---|---|---|
| 每条记录的 `run/session ID`、时间戳/phase convention、采样率和仪器时钟 | 未证实。 | 跨仪器配对、phase-resolved fusion、causal lag、时域误差评价。 |
| `cavity geometry ID ↔ file ↔ PMFR ↔ wake/TG state ↔ M/Re` 对应表 | 未证实。 | cavity-family design effect、purge operating map、grouped holdout。 |
| raw/filtered/phase-averaged/derived 数据层级和处理脚本 | 未证实。 | 重现性、避免 train–test information leakage、重新计算 loss/unsteadiness metrics。 |
| 单位、坐标系、reference pressure/temperature、loss definition 与不确定度传播 | 论文层面部分可见，archive 级逐文件未证实。 | 可比的 objective、跨仪器比对、物理导数/敏感度声称。 |
| independent repeated runs 或真正独立的 condition/design family | 未证实。 | 泛化、鲁棒优化、统计显著性和外推声称。 |
| 可本地冻结的 archive revision、hash 和内容 manifest | 未完成。 | 端到端可复现 training/validation artifact。 |

---

## 3. 已完成的敌对新颖性核验

下表不是普通参考文献表，而是主张—前例的逐项相邻核验。它排除宽泛路线，并保留各文章实际覆盖的边界。

| 直接相邻工作 | 已核验的对象和输出 | 对新路线的结果 |
|---|---|---|
| Lopes, Simonassi & Lavagnoli, [2024, DOI 10.1115/1.4063878](https://doi.org/10.1115/1.4063878), *Time-Averaged Aerodynamics of a High-Speed Low-Pressure Turbine Cascade With Cavity Purge and Unsteady Wakes* | 在同一高速度 LPT cascade 的 cavity purge、unsteady wakes、\(M=0.90\)、\(Re=70k\)、\(f^+=0.95\) 下，比较 average blade/outlet aerodynamics、secondary flows 与 loss breakdown。 | **关闭**“首次研究 cavity purge–wake 平均损失/平均气动”“仅把 PMFR 放进代理后优化”的主张。 |
| Lopes & Lavagnoli, [2025, DOI 10.1115/1.4067674](https://doi.org/10.1115/1.4067674), *Unsteadiness in the Secondary Flows of a High-Speed Low-Pressure Turbine Cascade With Unsteady Wakes and Purge Flow* | 同一类 `wake + variable PMFR` 条件，phase-averaged fast-response virtual probe 映射 outlet energy loss、TI 与 angles；摘要报告 purge 会增强二次流结构和 loss fluctuation extent。 | **关闭**“首次发现/预测/解释 wake–purge secondary-flow modulation”及其仅换模型名称的变体。 |
| Lopes et al., [2026, DOI 10.3390/ijtpp11010014](https://doi.org/10.3390/ijtpp11010014), *Off-Design Aerodynamics of the SPLEEN C1 Cascade* | steady inlet，\(M_{out}=0.70–0.95\)、\(Re_{out}=65–120k\)；实验与 RANS/MISES，已经做 profile/secondary loss decomposition、separation/transition 机理和模型校准。 | **关闭**“首个 SPLEEN steady off-design loss model/surrogate”“泛化 Mach–Re 预测”的主张。 |
| Metti et al., [GT2025-153288 / DOI 10.1115/1.4069487](https://doi.org/10.1115/1.4069487), *The Impact of Transition and Turbulence Modeling on the SPLEEN High-Speed Low-Pressure Turbine Cascade* | 多个 transition-sensitive RANS/URANS closures 对照实验，并明确给出 preliminary trained data-driven transition/turbulence-model results。 | **关闭**“首次以 AI/ML 学习 SPLEEN closure”或普通 data-driven closure validation。任何更窄 ML 主张都须先逐段比对其 trained-model method、训练目标、工况与验证。 |
| Okada et al., [2024, DOI 10.1115/1.4063674](https://doi.org/10.1115/1.4063674), *Particle Image Velocimetry Measurements in a High-Speed Low-Reynolds Low-Pressure Turbine Cascade* | PIV 已在 C1 steady reference-cavity configurations 中与 5HP/RANS 比较，覆盖 B2B/COP field、wake deficit 与 turbulence characteristics。 | **关闭**“首次在 SPLEEN 用 PIV 验证流场/常规 PIV–probe fusion”的宽泛说法。 |

### 3.1 为什么“加 AI、BO 或 MOO”不能重开问题

上表已经覆盖对象、变量与物理输出的中心部分。把 optimizer 换为 NSGA-II、Bayesian optimization、active learning 或 neural operator，或把 regression 改名为 digital twin，不能自动形成新的机制。它们至多是实现方式；若缺少一个未被这些直接研究回答的、可反驳的科学/工程决策，G1 和 G2 均不通过。

截至本审计的严格状态是：针对精确词串 `SPLEEN C1 + ML/MOO/active learning` 的若干网络检索存在“spleen”解剖学歧义，因而没有得到高质量的穷尽性负面结论。反过来，已定位的 GT2025 data-driven closure 工作足以淘汰宽泛 AI claim，但**不能证明所有可能的窄 AI 问题都不存在**。

---

## 4. G0–G6 门控快照

| Gate | 当前状态 | 已有证据 | 未满足条件 / kill criterion |
|---|---|---|---|
| G0 — 主张完整性 | **通过，仅限问题记录。** | 对象、已发表物理范围、证据级别和不能推断的领域已被显式分开。 | 任何将其升级为“完整 MDO”“新 AI closure”或“性能结果”的话，立即因证据类别漂移而失败。 |
| G1 — 后果先于新颖性 | 未通过。 | purge mass flow 与 loss/unsteadiness 的工程相关性存在。 | 必须定义真实决策：谁据此改变哪个 cavity/secondary-air operating choice、代价/约束是什么、且该决策不能只是重述已有 PMFR study。没有可审计 system-level bleed/cycle/thermal cost，不得声称全发动机效益。 |
| G2 — 敌对新颖性 | 未通过。 | §3 已关闭多个宽泛方向。 | 在固定一个窄假设和评价指标后，必须再次对 DOI 10.1115/1.4063878、1.4067674、1.4069487、10.3390/ijtpp11010014 的全文、引用链和后续论文逐项检索。若其核心决策已被覆盖，则关闭。 |
| G3 — 数学/计算有效性 | 未通过。 | 可写出候选变量—输出表。 | 先取得定义、单位、坐标、dependency graph、processing hierarchy 与 missingness；任何 interaction derivative、ANOVA/Möbius、causal 或 robust bound 主张都须先声明 regularity、conditioning 和反例/negative control。 |
| G4 — 验证梯 | 未通过。 | steady PIV 与 5HP/RANS 是某一子集的 measurement comparison。 | 需要与最终问题匹配的独立验证：至少冻结 condition/design group holdout；若声称行为随 cavity/PMFR 改变，则留出不能共享同一试次/预处理信息的 cavity/PMFR/wake group。PIV 不可被误当作 WG-on purge 的独立验证。 |
| G5 — 公平比较与可重现 | 未通过。 | record DOIs、版本和 advertised MD5 已记录。 | 必须取得本地 binary、计算 SHA-256、生成 file manifest、冻结 split/seeds/tuning budget/baselines/exclusions，并公开处理环境。当前 TLS/endpoint 行为使这一步尚未完成。 |
| G6 — 署名与投稿资格 | 未开始。 | 无。 | 先有通过 G0–G5 的结果，再由作者独立核验和写作，并直接读取目标期刊的当前 AI、数据许可和 authorship policy。 |

**因此 status 不升级。** `Question candidate` 意味着值得继续寻找可证伪的问题和数据键，并不意味着已有论文题目、算法结果或投稿资格。

---

## 5. 唯一允许的重入路径（不是当前研究承诺）

只有满足以下顺序，才允许把 SPLEEN 从问题记录推进到研究候选：

1. **冻结 artifact。** 下载对应 revision 的 archive；记录 DOI、record ID、获取时间、license、advertised checksum 和本地 SHA-256。不以网页 listing 代替 binary manifest。
2. **先审计 schema，后建模。** 抽取 README/technical notes，形成 `file → raw/processed status → instrument → run/session → cavity → WG/TG → PMFR → M/Re → units → uncertainty` 表。必须把 version-corrected CAD 和 v1 error 分开。
3. **证明共同条件。** 只有在上述表明确关联时，才可将不同 pressure/probe/PIV/film/other signals组成同一 condition；不能从相似文件名、相同论文、近似日期或共享机构推断配对。
4. **固定一个不同于 §3 的问题。** 它必须预先写成可被证伪的 decision hypothesis，而非“做一个更好的网络”。例如，若且仅若存在未被已发表论文比较的 cavity/PMFR/wake cell hierarchy，才可检验一个明确的 robust-feasibility rule 是否在留出条件中改变接受/拒绝的运行选择。这个例子不是贡献声明，也不是已经可行。
5. **预注册验证。** 定义 target metric、loss/unsteadiness 的测量定义、baseline、condition- or session-group split、final untouched test set、tuning budget、seed 和失败阈值。非独立的同一扫描/同一条件切片不能被标为 OOD test。
6. **重新做 G2。** 新问题的精确变量、目标、约束和预测器一旦固定，必须再次核验同一作者群的后续文献、引用它们的工作、相关专利/技术报告和不同术语下的相邻方法。

### 5.1 立即关闭的条件

任一条件出现时，SPLEEN 必须降为 `Archive only / reference benchmark`，而非用更强形容词掩盖缺口：

- archive 只包含一种可用 cavity geometry，或没有足够独立 intervention 层级；此时没有 geometry co-design 问题；
- 没有 run/instrument matching key；此时没有跨模态数据融合或校准问题；
- 只有同条件内重复/切片，无法构造独立 holdout；此时不能作泛化、鲁棒 decision 或 AI superiority claim；
- 已发表工作已用实质相同的 action、objective、condition range 和 validation ladder 回答拟议窄问题；
- 需要温度、应力、寿命或系统性能才可定义的目标，但这些量在同一对象中没有真值/可信耦合模型；此时不得继续称 MDO。

---

## 6. 与其他公开体系的边界：不做虚假拼接

| 体系 | 已知价值 | 为什么不能和 SPLEEN 拼成一个 MDO dataset |
|---|---|---|
| NASA C3X / Mark-II | NASA 公共报告给出 internally/film-cooled vane 的 pressure、temperature、heat-transfer 和多参数试验矩阵；例如 [NASA CR-182133](https://ntrs.nasa.gov/citations/19890004383)。 | 几何、材料、冷却构型、工况和 sample identity 均不是 SPLEEN C1。它可作 CHT verification context，不能制造 SPLEEN 的金属温度或应力标签。且 C3X cooling MOO 已有直接前例，不能用作通用 AI-MDO 叙事。 |
| 2026 cantilever turbine-cascade FSI 论文 | 同一弹性叶栅上有 dynamic strain + passage pressure 的真实 FIV 实验，[Tan et al., DOI 10.1016/j.ast.2025.110930](https://doi.org/10.1016/j.ast.2025.110930)。 | 本审计未定位公开的 raw-data archive；更重要的是它不是 SPLEEN 的同一硬件/工况。不能借其应变结果为 SPLEEN 补结构边。 |
| MEXICO/New-MEXICO wind rotor | 物理实验覆盖 pressure、loads、PIV，New-MEXICO 还覆盖 acoustic measurements 和多项干预。 | 官方 Mexnext 状态页说明只有部分数据公开，完整 measurement/rotor information 受 NDA 条件限制：[Mexnext status](https://www.mexnext.org/resultsstatus/)。它又是不同风机对象，不能与 SPLEEN join。 |
| UNAFLOW floating-wind experiment | 开放 CC-BY archive 含受控 surge motion、airfoil polars、rotor force、wake hot-wire/PIV：[Zenodo](https://zenodo.org/records/4740006)；是很好的 aerodynamic–motion interaction reference。 | 平台 surge 是外部施加的输入，而不是同一对象的被测结构响应；它与 SPLEEN 无共同 design/run key，不能补 SPLEEN 的结构或热真值。 |

继续发散寻找公开验证体系是必要的；这些体系之间的断边也必须如实保留。

---

## 7. scholarly-clarity 与 adversarial 审读记录

### 7.1 主张台账摘要

| 结论 | 类别 | 支撑 |
|---|---|---|
| SPLEEN 是公开的真实 high-speed LPT cascade 气动—secondary-air 测试体系。 | 一手 record / 论文事实。 | §1 的 Zenodo records 与 test-case paper。 |
| 主 v5 发布者说明 cavity geometry 与 secondary-air documentation 存在。 | 一手 record metadata 事实。 | [v5 record notes](https://zenodo.org/records/13712768)。 |
| PIV 子集不能自动验证 WG-on/purge 子集。 | 范围逻辑判断。 | PIV record 指定 `Cavity Aref`, no WG；必须有完整 run map 才能反驳此判断。 |
| 宽泛 purge–wake、steady loss、AI closure 路线已被直接前例占据。 | 文献邻接判断。 | §3 的五篇直接论文和相邻 scope。 |
| 目前不是完整 MDO 或投稿候选。 | gate 结论。 | §2 缺失量与 §4 G1–G6。 |
| 若且仅若合同与新颖性门槛后续通过，可能存在一个窄 aero–secondary-air operating/measurement question。 | 条件性 future work。 | §5 的重入条件，而非当前结果。 |

### 7.2 Citation-adjacency check

- Zenodo source 仅用于其 record-level contents、license、version notes 和 declared scope；没有用它证明未读 archive member 的字段语义。
- 2024/2025/2026 SPLEEN 论文仅用于其公开写出的条件、观测和已完成的分析；没有把 abstract 中未出现的 raw-data pairing 写成事实。
- C3X、MEXICO、UNAFLOW 只用来界定各自资产边界，不用作 SPLEEN 的替代真值。

### 7.3 red-flag pass

已检查 `first`, `novel`, `solved`, `guarantee`, `certificate`, `proves`, `exact`, `state of the art`, `all`, `always`, `never`。本文没有以这些词构成无来源的正向研究主张；对“首次”只以“不可使用的宽泛主张”方式出现，并有 §3 相邻文献支撑。

### 7.4 敌对审读

| 审稿角色 | 最可能的反驳 | 当前回答 / 必须完成的工作 |
|---|---|---|
| LPT experimentalist | “Zenodo 写了 document，为什么还说合同不完整？” | document existence 与逐文件 run pairing 是不同命题。先审计 README/technical notes 和 binary manifest。 |
| CFD/transition specialist | “ML closure 仍可有新网络。” | 新网络不是机制。必须与 Metti et al. 的 trained model、目标、条件和验证直接区分，并展示独立 decision benefit。 |
| MDO reviewer | “只有 purge 和 loss，为什么不叫 MDO？” | 目前最多有一个 aerodynamic–secondary-air operating-design/measurement space；没有同对象 solid/thermal/life truth 时，不使用 full MDO 标签。 |
| data scientist | “PIV、probe、pressure 都是同一项目，为什么不能合训？” | 同项目不等于同试次。缺少 matching key 前，合训会引入不可审计 pairing assumption。 |
| editor | “论文贡献到底是什么？” | 当前没有投稿贡献；本文件是一个防止错误立项的 evidence-and-kill record。只有 §5 全部通过后才可重新回答。 |

**审计结论：** SPLEEN C1 值得保留为高价值的公开气动—secondary-air interaction benchmark 和问题源，但当前严格状态必须保持为 `Question candidate`。它不是失败的研究方向，也不是已完成的论文路线；下一步是用完整 archive documentation 验证或淘汰那个唯一剩余的窄问题，而不是开始训练或制造优化结果。
