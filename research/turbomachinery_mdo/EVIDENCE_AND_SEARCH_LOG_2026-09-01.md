# 证据与检索日志（截至 2026-09-01）

**用途：** 记录本轮推理依赖的公开来源、可访问边界、查询和不确定性。
**规则：** 摘要、搜索片段和 README 只用于其明确写出的事实；没有全文或原始数据时不扩展成更强论断。网页检索不能证明全球“无先例”。

---

## 1. 公开能力边界

| 日期 | 来源 | 核验到的内容 | 结论边界 |
|---|---|---|---|
| 2026-09-01 | [宋立明官方研究领域页](https://gr.xjtu.edu.cn/songlm/zh_CN/zdylm/994200/list/index.htm) | 明列：透平机械多学科精细优化设计与数据挖掘；涡轮优化设计系统及数据挖掘平台；随机 UQ 与不确定性优化；内部复杂流动换热冷却。 | 是团队公开研究方向的第一手描述。 |
| 2026-09-01 | [宋立明官方主页/数据集页](https://gr.xjtu.edu.cn/songlm/) | 简介写明叶轮机械气动热力学、优化设计理论/平台、UQ、智能流场预测；公开列 GE-E3 和 Pak-B 数据。 | 能力与公开数据的主要官方入口。 |
| 2026-09-01 | [郭振东官方主页](https://gr.xjtu.edu.cn/guozhendong/) | 公开简介写明叶轮机械智能设计优化、智能流场预测、数据挖掘及 UQ/鲁棒性/可靠性优化。 | 是其公开能力边界。其“研究领域”子页当前未填实质条目，故不额外归因。 |
| 2026-09-01 | [宋立明代表性论文页](https://gr.xjtu.edu.cn/songlm/zh_CN/zdylm/994197/list/index.htm) | 列有 2012 transonic turbine-stage 自动多目标/多学科优化、GT2017 高温叶片 aero-thermal MDO、2017–2018 端壁冷却/气动热/非轴对称端壁研究等。 | 排除“团队首次做叶轮机械 MDO/高温叶片气动热优化”的宽泛创新叙述。 |
| 2026-09-01 | [李军公开研究领域页](https://gr.xjtu.edu.cn/junli/zh_CN/zdylm/988398/list/index.htm) | 公开列透平气热性能 UQ、寿命评估/RDO、热端部件气热性能和冷却结构布局；列 GT2014 气动多目标优化及 GT2014 气动/冷却 CHT MDO。 | 作为共同作者/团队公开历史的交叉核验；不代替对具体论文全文的核验。 |

---

## 2. 数据与开源实现证据

### 2.1 GE-E3

| 来源 | 明示内容 | 用于什么 | 不用于什么 |
|---|---|---|---|
| [宋立明官方数据页](https://gr.xjtu.edu.cn/songlm/) | GE-E3 第一级高压涡轮单通道（S1、R1）；96 个几何变量 + 4 个边界条件变量；使用 Numeca 三维流场；页面同时写 5000 样本、4000 训练、900 验证。 | 确认对象、变量类别和公开数据存在。 | 不能无视 5000 vs 4900 的不一致而宣称精确样本数。 |
| [MindScience `turbine_uq` README](https://raw.githubusercontent.com/mindspore-ai/mindscience/legacy-master/MindFlow/applications/research/turbine_uq/README.md) | 输入：设计参数 \(x\)、工况 \(\alpha\)、坐标 \(p\)；输出 \(p,T,V_x,V_y,V_z,\rho\)；README 写 4900、4000/900，后处理性能并使用 UQ/NSGA2。 | 确认开源应用是流动基本变量到气动性能/UQ 的链。 | 不能把 CFD 温度字段等同 CHT 金属温度、应力或寿命。 |
| [OSInfra 数据目录](https://download-mindspore.osinfra.cn/mindscience/mindflow/dataset/applications/research/turbine_uq/) | 目录列 `designStruct_100_6000.mat`（2.3 MiB）、`sampleStruct_128_64_6000.mat`（2.9 GiB）、`normalization.npz`、hub/shroud 文件。 | 确认可见文件名、大小及版本冲突。 | 目录文件名不是 MAT 的已验证 row count；未下载的 2.9 GiB 不可当作已处理。 |

### 2.2 Pak-B

| 来源 | 明示内容 | 用于什么 | 不用于什么 |
|---|---|---|---|
| [宋立明官方数据页](https://gr.xjtu.edu.cn/songlm/) | Pak-B 端壁气膜孔布局；1/2/3/5 孔各 600、10 孔 110；总体写 2510：2000 training、500 validation、10 fine-tuning test。 | 当前版本描述的优先证据。 | 没有说明压损、冷却流量、金属温度、应力或寿命标签。 |
| [MindScience `superposition` README](https://raw.githubusercontent.com/mindspore-ai/mindscience/legacy-master/MindFlow/applications/research/superposition/README.md) | 以 Sellers 公式抽象构造 SDNO；写 1/2/3/5 各 600，并称 10/15/20 各 110、总 2730。 | 确认 legacy 应用的算法与旧数据叙述。 | 不能与当前官方页混用；15/20 孔当前目录未出现。 |
| [MindScience `dataset.py`](https://raw.githubusercontent.com/mindspore-ai/mindscience/legacy-master/MindFlow/applications/research/superposition/src/dataset.py) | 只从 MAT 读取 `sdf`、`Temperature`，读取 `Grids_x`、`Grids_y`；padding 到 10 SDF channels，默认对每个样本随机置换通道。 | 强证据：该公开代码路径没有读取压力、流量、压损、应力或寿命；也提示 SDF channel identity / randomization 必须纳入复现 manifest。 | 不证明原始商业 CFD 的每个未公开中间量都永远不存在；只界定当前公开复现接口。 |
| [OSInfra 数据目录](https://download-mindspore.osinfra.cn/mindscience/mindflow/dataset/applications/research/superposition_spno/) | 当前列 `pakb_{1,2,3,5,10}_hole_{train,test}.mat`；无 15/20 文件；文件大小可见。 | 证明当前下载目录和 legacy README 冲突。 | 目录本身不是字段/样本 shape 的二进制验证。 |

### 2.3 FAN-02：论文级 FSAI 覆盖与当前 release 内容

| 来源 | 明示内容 | 用于什么 | 不用于什么 |
|---|---|---|---|
| [Zenodo record metadata](https://zenodo.org/api/records/17909944) | published revision 6、open/CC-BY-4.0 的 FAN-02 record metadata。 | 固定当前审计的 record/DOI 和 release 身份。 | 不以 metadata description 代替完整 file inventory 或本地下载校验。 |
| [Zenodo current `/files` API](https://zenodo.org/api/records/17909944/files) | 2026-09-01 直接读取的完整 `entries` 数组含 11 项：`Housing_Structure.stp`、`housing_structure_advanced.stp`、`Housing_WallPressure_Window.stp`，以及 8 个 sensor-position TXT；总 advertised size 30,565,019 bytes。 | 一手证明**当前 record manifest 列出的**内容只有几何和传感器位置。 | 不把文件名、advertised MD5 或 API 清单说成本地 bytes、测量 schema，或全局不存在性证明。 |
| [FAN-02 overview, *Journal of Imaging*, 2026](https://www.mdpi.com/2504-186X/11/1/10) | 400-mm/12-blade enclosed centrifugal fan 的 PIV/HWA、叶片压力、LSV、sound-intensity 和 microphone 等论文级测量描述，并以“whole or in part”限定数据可用性。 | 证明一个真实 FSAI 测量链值得追踪，并与当前 release 的缺口作范围比对。 | 不把论文描述升级为当前 Zenodo 已包含原始时序、共同 run key、结构声学 mesh 或可重复 split。 |

**当前范围结论。** `/files` inventory 中没有列出 PIV/HWA、压力/LSV/声学数据、工况/校准/同步表、共同 run ID、流体域/结构声学 mesh 或设计干预表。因此，当前 release 不满足跨模态学习、grouped holdout 或设计回算所需的数据合同。该句只描述当前 record/revision；它不否定实验，也不排除未来或另行发布的数据。逐项转录、re-entry 条件与前例边界见 [FAN-02 release-content audit](FAN_02_RELEASE_AUDIT_2026-09-01.md)。

### 2.4 当前本地可达性

- 本轮通过网页抓取读取了 OSInfra 目录，但未写入任何 MAT 文件到本仓库。
- 有针对性地尝试下载轻量 GE-E3 `designStruct_100_6000.mat` 到 `/tmp` 以检查 schema；命令行 TLS 协商返回 `curl: (35) OpenSSL SSL_connect: SSL_ERROR_SYSCALL`，因此没有可读取的文件。此尝试不触及 2.9 GiB field 文件。
- 为排除单一客户端设置，另做了一次**不下载 payload**的替代传输诊断：强制 HTTP/1.1/TLS 1.2 的 `curl -I` 仍报 `SSL_ERROR_SYSCALL`，`wget --spider` 报 `GnuTLS: The TLS connection was non-properly terminated`。之后未作无差别重试。
- 结论是“**网页层可发现、当前 CLI 本地传输未成功**”，不是“数据不存在”，也不是“数据已获得”。

### 2.5 数据可达性与未解决版本冲突

这两条矛盾必须在任何公开实验前作为 `manifest` 固化：

```text
GE-E3: 官方页：5000 samples + 4000 train + 900 validation
       开源 README：4900 samples + 4000 train + 900 validation
       数据文件名：..._6000.mat

Pak-B: 官方页：2510 samples，1/2/3/5/10 holes
       legacy README：2730 samples，1/2/3/5/10/15/20 holes
       当前目录：仅 1/2/3/5/10 holes 文件
```

正确顺序是：**获取许可允许的实际 binary → hash → MAT keys/shapes → sample ID/split → manifest → baseline**。在此之前，不报“数据规模”“OOD 结果”或训练数字。

---

## 3. 直接/高度相邻前例

| 日期 | 来源 | 已核验的关键内容 | 对本项目的排除或边界 |
|---|---|---|---|
| 2026-09-01 | [Wang et al., 2024, *Journal of Turbomachinery*, DOI 10.1115/1.4064228](https://doi.org/10.1115/1.4064228)；[Crossref 记录](https://api.crossref.org/works/10.1115/1.4064228) | EMFS/MSFO：以 DBSCAN 识别 MFS 失准区，组合全局 MFS 与局部 SFS；摘要明说在 GE-E3 blade optimization 与 turbine-endwall film-cooling-layout design 测试。作者为 Wang、Song、Guo、Li、Feng。 | 直接排除使用相同公开对象宣称一般的多保真/单保真融合、局部替代、代理筛选优化。 |
| 2026-09-01 | [Wang et al., 2024, *Physics of Fluids*, DOI 10.1063/5.0239483](https://doi.org/10.1063/5.0239483)；[出版商页](https://pubs.aip.org/aip/pof/article/36/12/126110/3323873/Enhancing-generalization-in-endwall-film-cooling) | SDNO 对 Pak-B 端壁布局用 SDF 与 Sellers 型“decomposition–calculation–superposition”；训练 1–5 孔、预测 10–20 孔的组合外推。 | 数据/算法路线最直接近邻。 |
| 2026-09-01 | [Chen et al., 2025 I, *Physics of Fluids*, DOI 10.1063/5.0276858](https://doi.org/10.1063/5.0276858)；[Crossref 摘要](https://api.crossref.org/works/10.1063/5.0276858) | 对多排气膜提出并以实验、数值验证 decomposition theory；拆分各排贡献以追踪 error source，并将双排四种横向间距下的非线性误差关联到 kidney-vortex 行间相互作用。 | Q-IO 不能把“交互分解/误差来源/局域涡机制”当成新物理理论。该前例是双排，不被误写成 Pak-B 的逐样本同协议。 |
| 2026-09-01 | [Chen et al., 2025 II, *Physics of Fluids*, DOI 10.1063/5.0293895](https://doi.org/10.1063/5.0293895)；[Crossref 摘要](https://api.crossref.org/works/10.1063/5.0293895) | 基于 Part I 的行间非线性相互作用，建二维 analytical superposition prediction；以涡诱导速度、湍流扩散处理交互，摘要报告从单排向多排扩展。 | 排除将 interaction-aware superposition correction 作为 Q-IO 独特工程机制。 |
| 2026-09-01 | [Yao et al., 2025, *Physics of Fluids*, DOI 10.1063/5.0260945](https://doi.org/10.1063/5.0260945)；[Crossref 摘要](https://api.crossref.org/works/10.1063/5.0260945) | 为密集孔气膜 superposition 提出 vortex-encoded AI；四通道 U-Net 与 Sellers operation 结合，摘要报告改善 high-prediction-error areas 并扩展到 dense layouts。 | Q-IO 的“局域 interaction 表示 + AI 修正密集布局失效”已有直接领域近邻；后验误差区域不等于事前 calibrated error ranking。 |
| 2026-09-01 | [Yan et al., 2025, *Physics of Fluids*, DOI 10.1063/5.0274462](https://doi.org/10.1063/5.0274462)；[Crossref 摘要](https://api.crossref.org/works/10.1063/5.0274462) | 物理信息网络以时域/频域/residual 三分支处理孔型、孔排结构和气动参数，并加权 Sellers 下游高误差区；摘要报告多排外推。 | 排除“误差敏感区 + 残差修正 + 多排外推”的泛化包装。 |
| 2026-09-01 | [Yang et al., 2021, *International Journal of Thermal Sciences*, DOI 10.1016/j.ijthermalsci.2020.106774](https://doi.org/10.1016/j.ijthermalsci.2020.106774) | 对 effusion cooling 的多孔布局以卷积机器学习量化 superposition effect；摘要称在规则阵列训练、随机孔排布验证，并以卷积核解释邻孔贡献。 | 是 Q-IO “高阶/邻孔 interaction 可被机器学习量化”的直接威胁。摘要未足以判定它是否做 error-ranking、abstention 或 CFD-query allocation，须精读。 |
| 2026-09-01 | [Gao et al., 2025, *Processes*, DOI 10.3390/pr13010143](https://doi.org/10.3390/pr13010143) | 针对涡轮外环多排气膜，基于能量守恒与主流温度校正改进 Sellers 叠加；在不同孔间距、吹风比的实验中讨论多行累积误差和相互作用。 | 不能把“传统叠加漏掉孔相互作用”或“用物理修正解释其失效”当作 Q-IO 新机制。 |
| 2026-09-01 | [Wang et al., 2022, *International Journal of Heat and Mass Transfer*, DOI 10.1016/j.ijheatmasstransfer.2022.123353](https://doi.org/10.1016/j.ijheatmasstransfer.2022.123353) | 用 MLP + MC/Sobol 对多排 trench 气膜 superposition 的孔位、trench 几何和 compound angle 输入不确定性做 UQ。 | 排除“多排 superposition + ML + UQ/sensitivity”宽泛说法。该文摘要描述的是输入参数传播，不可误说已证明或未证明 Q-IO 所需的 surrogate-discrepancy/OOD error ranking。 |
| 2026-09-01 | [Wang et al., 2023, *AIP Advances*, DOI 10.1063/5.0132989](https://doi.org/10.1063/5.0132989) | 用 ANN + MC/Sobol 分析半球涡发生器气膜的几何/工况不确定性与敏感度。 | 同样排除普通 ANN/MC/Sobol 气膜 UQ；它不是可无证据替代的模型误差或 OOD reliability 评价。 |
| 2026-09-01 | [Cai et al., 2025, *International Journal of Heat and Mass Transfer*, DOI 10.1016/j.ijheatmasstransfer.2024.126559](https://doi.org/10.1016/j.ijheatmasstransfer.2024.126559)；[Cai et al., 2026, *Journal of Fluids Engineering*, DOI 10.1115/1.4070957](https://doi.org/10.1115/1.4070957) | 前者将 deep active subspace、CNN surrogate 与风扇孔气膜的 factor exploration/optimization 结合；后者用 active subspace 量化 RANS turbulence closure 参数的不确定性并优化模型参数以降低 CFD 误差。 | 排除“气膜 + active subspace + UQ/模型不确定性 + optimization”的宽泛路线；同样不能把它们的 turbulence-model uncertainty 与跨孔数 surrogate OOD error 混为一谈。 |
| 2026-09-01 | [Zhang et al., 2023, *Frontiers in Mechanical Engineering*, DOI 10.3389/fmech.2022.973293](https://doi.org/10.3389/fmech.2022.973293) | 在横向压力梯度的 endwall-like 流动环境中，对 shaped film-cooling hole 用 sequentially adaptive sampling + surrogate/BO 优化，并以 PSP 实验验证优化结果。 | 排除把“气膜主动加点/追加 CFD + 代理优化 + endwall 环境”作为 Q-IO query-allocation 或一般端壁优化的新颖性。它不是 Pak-B 孔数外推的同协议。 |
| 2026-09-01 | [Qiu et al., 2024, *Applied Thermal Engineering*, DOI 10.1016/j.applthermaleng.2024.122481](https://doi.org/10.1016/j.applthermaleng.2024.122481) | ALNN 以 Bayesian/combined active-learning sampling 提升小样本高温燃机叶片多源随机因素下的 thermal-fluid-structure performance 代理，并据此评估 LCF probabilistic life。 | 直接削弱“主动查询分配 + 叶片多物理/可靠性”作为方法卖点；当前 GE/Pak 又没有其所需 thermal-fluid-structure/life 真值。 |
| 2026-09-01 | [Zhang et al., 2024, *International Journal of Numerical Methods for Heat & Fluid Flow*, DOI 10.1108/HFF-10-2023-0620](https://doi.org/10.1108/HFF-10-2023-0620) | 在另一套线性叶栅数据上，以 Swin-Transformer U-Net 预测端壁气膜效率、压力、密度和速度，并报告了实验对照。 | 不能把“端壁多物理场 AI 代理 + 多目标应用”泛化表述为新；它不能填补 GE-E3/Pak-B 之间的共享变量/耦合真值缺口。 |
| 2026-09-01 | [Abdallah et al., GT2023, DOI 10.1115/GT2023-100746](https://doi.org/10.1115/GT2023-100746) | 内冷大型燃机叶片；AI 加速 stress、creep strain、displacement 和 Creep/TMF/HCF lifing 计算；高保真 FEA 的单算例耗时 1–8 天。 | 直接否定“首次用 ML 做叶片应力/蠕变/TMF/HCF 寿命代理”叙述。 |
| 2026-09-01 | [Abdallah et al., GT2025-151212 官方 session page](https://asme-turboexpo.secure-platform.com/a/solicitations/243/sessiongallery/18784/application/151212) | 标题与摘要明示 3-D Transformer neural operator；改变 stacking、rotation、压力/吸力面壁厚、internal-rib location、冷却供气和热气边界；目标为 creep/TMF 与 lifespan。 | 直接否定把几何/制造偏差、热边界、冷却供气、寿命预测、Transformer/NO 组合称为新机制。 |
| 2026-09-01 | [He et al., 2022, *Int. J. Heat Mass Transfer*](https://www.sciencedirect.com/science/article/abs/pii/S0017931022006196) | CHT CFD + cGAN + MOGA 优化 full-coverage film cooling；同时考虑高温负载与冷却布局。 | 排除“深度学习 + CHT + 多目标气膜布局优化”的宽泛提法。 |
| 2026-09-01 | [film-hole stress concentration optimization, 2024](https://www.sciencedirect.com/science/article/abs/pii/S0017931024003776) | FEA + surrogate 优化孔形以降低 stress concentration，并用 PSP 检验部分候选的 film effectiveness。 | 排除“孔形 + 应力集中 + 气膜性能代理优化”的宽泛提法。 |
| 2026-09-01 | [Gopakumar et al., 2026, CP for surrogate UQ](https://iopscience.iop.org/article/10.1088/2632-2153/ae2e7b) | 高维时空 surrogate 的模型无关 conformal UQ；明确 coverage 是 marginal、依赖 exchangeability，且实用性取决于 score。 | 不能把高维场 conformal calibration、OOD wrapper 或“certificate”宣称为新；跨孔数分布漂移尤其不能假设可交换。 |
| 2026-09-01 | [Sequential surrogate modeling + conformal inverse design, 2025](https://www.sciencedirect.com/science/article/abs/pii/S0951832025009822) | learner–assessor 双 surrogate 和 conformal interval 过滤 inverse-design 候选。 | 排除“两个代理 + conformal 筛选”作为单独的创新。 |
| 2026-09-01 | [SafeOpt-MC, 2021](https://link.springer.com/article/10.1007/s10994-021-06019-1)；[hidden-constraint aircraft design search record](https://www.researchgate.net/publication/382144379_Bayesian_optimization_with_hidden_constraints_for_aircraft_design) | 安全 BO、多个约束、二元/分类 hidden constraint 已是成熟/持续发展方向。 | Q-F 类“失败感知安全 Pareto”不能仅靠标签来源或 GP classifier 声称新颖。 |

### 3.1 不能用“unpaired data fusion”补出 MDO 耦合

| 日期 | 来源 | 已核验的关键内容 | 对本项目的边界 |
|---|---|---|---|
| 2026-09-01 | [Ahfock et al., 2016, *Computational Statistics & Data Analysis*, DOI 10.1016/j.csda.2016.06.005](https://doi.org/10.1016/j.csda.2016.06.005)；[开放摘要](https://pmc.ncbi.nlm.nih.gov/articles/PMC5423529/) | statistical matching 中，变量不被联合观测会使多数模型不可识别；可行做法是在明确的部分识别模型和附加约束下估计 identified set，而不是凭空估计唯一联合关系。 | 是 R9 的理论反例：不能凭 GE-E3/Pak-B 的不配对边际资料学习一个可验证的气动—热—结构耦合。该文不是 turbomachinery/MDO 前例，故不夸大为直接同题论文。 |
| 2026-09-01 | [Martins & Ning, *Engineering Design Optimization*, MDO chapter](https://mdobook.github.io/html/mdo/) | MDO 的分析要求 coupled models/solvers；shared design variables 同时影响多组件，必须被共同优化，孤立组件的 assumed boundary conditions 不能替代耦合模型。 | 支撑本台账采用的术语门槛：两个不同对象的独立 surrogate 不能因 latent alignment 或 OT 而自动变为 MDO。 |

### 3.2 需要二次核验的文献书目信息

本日志故意不补写未直接抓到 DOI 的条目。所有旧团队 conference paper 的页码/DOI、以及 2025–2026 的预印本状态，未来若进入论文候选阶段必须从出版商或 Crossref 逐条复核。无 DOI 的标题匹配不能充当正式投稿引用。

---

## 4. 本轮敌对检索查询与结果范围

查询使用网页/出版商索引；结果是日期受限的线索，不是 exhaustiveness proof。

| 查询（或等价关键词组合） | 观察到的关键结果 | 对应处置 |
|---|---|---|
| `"A Novel Multi-Fidelity Surrogate for Efficient" turbine 2024 Wang GE-E3 Pak-B` | 定位 MSFO 原文/摘要；明确 GE-E3 和 endwall layout 测试。 | 关闭 R2。 |
| `"GT2025-151212" turbine blade transformer neural operators` | 定位官方 ASME session 与技术项目。 | 关闭 R5 的宽泛版本。 |
| `"Surrogate Models for 3D Finite Element Creep Analysis Acceleration"` | 定位 GT2023 论文和完整摘要。 | 关闭“首次 lifing surrogate”。 |
| `"film cooling" "neural operator" topology extrapolation` | SDNO、meta-FNO 和多个更近 cooling NO 工作。 | 不能将 SDF/NO/孔数外推立为新机制。 |
| `"turbine endwall film cooling" "machine learning" optimization uncertainty` | GA/CGAN/UQ/BO/CHT 等大量直接相邻工作。 | 关闭普通优化/UQ。 |
| `"film cooling" "high-order interaction"`、`"film cooling" ANOVA interaction surrogate`、`"film cooling" Shapley interaction machine learning` | 定位 Yang et al. 2021 的 ML superposition-effect quantification；再沿 SDNO 的被引链定位 Chen 2025 I/II 的 interaction decomposition / nonlinear superposition 和 Yao 2025 的 vortex-encoded AI。 | Q-IO 的物理 interaction 核心已被直接领域前例实质覆盖，触发关闭；不能声称首次量化、解释或修正孔相互作用。 |
| `"film cooling" "active learning" uncertainty surrogate`、`"film cooling" "out-of-distribution" uncertainty`、`"film cooling" abstention surrogate`、`"film cooling" "risk coverage"`、`"film cooling" "conformal prediction"` | 定位 Zhang et al. 2023 的气膜 sequentially adaptive sampling + BO/PSP，以及 Qiu et al. 2024 的高温叶片 active-learning sampling；还定位 MC/Sobol 输入 UQ 和稀疏测点重构线索。未在可访问网页中定位到与 Pak-B/SDNO 同时具备孔数外推、**代理误差**排序、拒答和查询分配的可确认直系论文。 | “未定位”不是无前例证明；输入 UQ 不能偷换为 OOD model-error reliability；剩余组合只是无数据合同的通用 wrapper，不能重开 Q-IO。 |
| SDNO 被引链：OpenAlex `cites:W4404998913`（2026-09-01） | 数据库当时返回 5 条记录，其中 Chen et al. 2025 I/II 直接引用 SDNO；另有 2025 endwall flow 论文。 | 这是追踪线索，不是穷尽的 citation database。以其发现的 Chen I/II 已另由 AIP/Crossref 摘要核验。 |
| `"safe Bayesian optimization" "hidden constraints" simulator failure multiobjective optimization` | SafeOpt/hidden constraints/failure-aware SAO/多约束 BO。 | Q-F 只保留为外部线索，不立项。 |
| `conformal prediction surrogate-based multiobjective design optimization failure-aware` | CP for high-dimensional surrogates、sequential conformal inverse design 等。 | 不能把 CP wrapper 写成新方法。 |
| `"unpaired data" "multidisciplinary design optimization"`、`"partial identification" Pareto optimization unpaired data`、`"data fusion" "multidisciplinary design optimization" surrogate` | 定位到一般 statistical matching/partial-identification 与已有 MDO data-fusion 文献；未定位到能令两个无共同对象、无共同 \(x\) 的涡轮数据自动产生物理耦合的可验证机制。此“未定位”不是原创证明。 | 关闭 R9：若无显式共享变量、共同真值或额外物理/实验约束，任何 cross-dataset coupling 均不可由本数据反驳。 |
| `"high-order interaction" neural operator compositional generalization PDE` | 泛化的 feature-interaction/operator-composition 方法很多。 | 不为已关闭 Q-IO 补造通用方法学差异；若未来新问题要使用它们，须重新从 G0/G2 审核。 |
| 中文：`叶轮机械 智能设计优化 智能流场预测 不确定性量化 郭振东` | 定位郭振东官方简介及相关成果线索。 | 固定能力边界，不假称官方页未写的细节。 |

---

## 5. 外部资源线索（明确超出当前限定）

| 资源 | 已核验价值 | 为什么不能替代当前项目 |
|---|---|---|
| [NASA EEE 2-stage HPT CFD Tecplot results](https://data.nasa.gov/dataset/eee-2-stage-hpt-cfd-tecplot-results) + [NASA `turbo-design`](https://github.com/nasa/turbo-design) | 公开 HPT CFD 参考/重构几何示例。`turbo-design` 明示重构几何与 1970–1980 年代原始硬件可能在半径、扭转、型线不同。 | 流场/几何参考不等于共同变量下的 CHT/FEA/lifing 数据。 |
| [JDecke/ubend-cfd](https://huggingface.co/datasets/JDecke/ubend-cfd) + [数据论文](https://pmc.ncbi.nlm.nih.gov/articles/PMC10460948/) | 约 8950 成功二维 CHT、28 几何变量、流/固温度场和可区分的网格/收敛失败。 | 非叶片；无应力/寿命/外热流；许可 CC-BY-NC-4.0；只能是未来方法学负载测试。 |

---

## 6. 审计限制

1. 本环境没有 Scopus/Web of Science 全文检索权限，也没有每一篇近邻的付费全文；未来候选须补充由作者/图书馆获得的全文精读。
2. 外部网页可以更新或下线。提交前需要保存许可允许的元数据快照、DOI、访问日期和 source version。
3. 搜索结果中的百分比、速度和性能从未被当作本项目自己的结果；本项目没有执行训练或仿真。
4. 这个日志保存的是研究立项证据，不是可提交的 manuscript text。

---

## 7. 高发散候选图谱：新增敌对检索（摘要/网页层，2026-09-01）

本节对应 [高发散候选图谱](CANDIDATE_ATLAS_2026-09-01.md)。它记录的是“哪些相邻工作使一条宽泛路线不能直接立项”，**不是**对文献全集的穷尽声明，也不是对下列论文全部技术细节的全文复核。

| 检索簇（或等价查询） | 本轮定位并只使用的明确事实 | 对候选空间的影响 |
|---|---|---|
| `goal-oriented model reduction MDO interface POD Coelho 2008`；`goal-oriented model reduction nonlinear PDE aerodynamics` | Coelho et al. (2008) 的出版社页明确写 POD + MLS 用于 2-D wing 的 fluid–structure MDO 并减少学科间交换数据；Xiao et al. (2010) 的 CPOD 摘要明确比较多种 ROM 的 Pareto sets；Yano (2020, DOI `10.1002/nme.6395`) 明确给出参数化非线性 aerodynamic PDE 的 goal-oriented RB、DWR/output error estimate 与输出驱动 snapshot。 | F1/F2/F5 不能把“目标导向接口压缩、输出误差或接口采样”作为新机制。F1 只保留为高风险 `R`，且必须提出不同于普通 output-bound 的决策反转对象与校准合同。 |
| `damage equivalent scenario reduction fatigue thermal loading reduced order model path dependent damage`；`equivalent fatigue load uncertain structures`；`load paths reduced order models damage Bayesian optimization` | 已定位到：Bertsimas & Mundru 的 objective/constraint-aware scenario reduction；Pulsipher et al. (2022) 将 random fields 纳入 continuous space/time optimization；`Equivalent fatigue load approach for fatigue design of uncertain structures` 以 damage/failure equivalence 压缩复杂载荷且考虑结构不确定性；Goury et al. (2016, DOI `10.1007/s00466-016-1290-2`) 用耗散驱动和 Bayesian optimization 选择高维时变加载路径构建 damage ROM。 | F3 的“损伤等价/路径依赖/场景压缩”已遇到直接威胁。若未来不能严格区分**跨设计的损伤分布 + governing-hotspot identity**与 existing equivalent-load、problem-dependent reduction、load-path ROM，F3 必须关闭。当前无 CHT–FEA–life 真值，故不实现。 |
| `turbine thermal hotspot switching surrogate optimization maximum temperature location non-smooth`；`hotspot thermal reduced order model` | 已有工作明确以目标 hotspot 减少 thermal model order 并提供 error-bound 叙事；一般热优化/thermal management 中 hotspot location 随设计变化的现象和预测已有大量近邻。 | F4 不能卖“关注 hotspot”或“预测 hotspot position”；仅可保留“预注册、网格稳定且改变 downstream constraint 的切换事件”这个更窄的待反证对象。 |
| `topological data analysis film cooling flow temperature field persistent homology`；`persistent homology flow estimation` | PH/TDA 已被用于流道连通性/流动图像估计；相应论文也指出 persistence parameters 本身难以直接关联物理属性。persistent homology、Pareto topology 与 topology-aware BO 也已有独立方法簇。 | P1 不可把 TDA 或 persistence diagram 当作物理解释。只有先验定义的 cooling-state mechanism、阈值/网格鲁棒性、独立流动诊断和优于经典场统计量的盲测才有可能保留为单学科线索。 |
| `causal invariant representation CFD turbomachinery field surrogate OOD geometry boundary conditions`；`invariant causal representation OOD graphs` | IRM/非线性 invariant-causal representation 已要求多环境及识别假设；Wu et al. (2019) 已将 causal graph 用于 MDO 辅助降维/分解；Blechschmidt & Mimic (2026, DOI `10.1115/1.4069140`) 已以 mesh GNN 从 steady RANS 预测 time-averaged URANS full field。另有 geometry/condition neural-field surrogate 直接处理 aerodynamic flow OOD/mesh invariance。 | L1 不可宣称发现因果或提出首个 OOD flow surrogate。它只能在实际 GE-E3 binary 证实的 intervention/case-map、整几何/整工况组合 holdout、随机环境标签负对照和公平 ERM/GroupDRO/IRM baseline 后，作为**单学科**探索；没有热/结构桥接时不是 MDO。 |
| `GE-E3 vane hot streak swirl CHT cGAN MOGA`；`film cooling superposition uncertainty active learning` | GE-E3 first-stage fully film-cooled vane 的 hot streak + swirl CHT 已公开；He et al. (2022) 的摘要明确为 GE-E3 1st-stage vane 的 96 CHT cases、cGAN、276-bit hole layout、5% maximum surface temperature + coolant mass-flow 双目标 MOGA。 | T1 已由同对象、同类热载荷、CHT + DL + optimization 的直接前例关闭。不能把热条带/旋流/孔布局换名重开。 |
| `KADMOS CMDOWS ontology digital thread MDO evidence contract`；`causal graph MDO` | KADMOS/formal graph、CMDOWS/workflow、digital thread/ontology/data-integration 及 causal-graph MDO 都有直接或高度相邻框架。 | W1/W2 仅能作为项目治理与 future data contract；没有新、可反驳的 coupled decision theory 和 paired truth 时不是论文核心。 |

### 7.1 新增来源的范围限定

- 对 F1/F3/F4/P1/L1 的详细卡片、强基线与 kill criteria 只在 [图谱 §3、§5、§6、§8](CANDIDATE_ATLAS_2026-09-01.md) 中使用；它们是**未来进入 G0–G6 前的反证门槛**，没有产出实验数字或理论证明。
- `Equivalent fatigue load`、Goury load-path ROM、Coelho/CPOD/Yano、Pulsipher random-field optimization 等来源为 F3/F1 提高了而非降低了新颖性门槛。它们不被误称为“叶轮机械同题复现”，但足以阻止通过词汇拼接宣布空白。
- 本轮未下载 GE-E3/Pak-B binary、未运行 CFD/CHT/FEA/训练/优化、未安装科学计算依赖；任何后续结果必须先满足 §2.4 的 manifest 要求。

---

## 8. Francis-99 Workshop 3：文档级 FSI 证据与 archive 边界

本节只登记已读取的**数据元数据、workshop report 和论文**。它不把页面可见性、文件声明、API MD5 或出版物中的 fitted parameter 当成已取得的 archive binary、已验证 schema 或独立泛化结果。逐项测量/派生量/不确定性/留出设计见 [F99-W3 矩阵](F99_W3_MEASUREMENT_VALIDATION_MATRIX_2026-09-01.md)。

| 日期 | 来源 | 已核验的明确内容 | 不扩展成 |
|---|---|---|---|
| 2026-09-01 | [DataverseNO dataset current V1 API](https://dataverse.no/api/datasets/:persistentId/versions/1.0?persistentId=doi:10.18710/XNWZIC)；[dataset metadata API](https://dataverse.no/api/datasets/:persistentId/?persistentId=doi:10.18710/XNWZIC) | 当前 API 版本列表显示已发布 V1.0；current file manifest 列 `f99w3_exp_excitation.zip`（dataFile `268899`、file PID `doi:10.18710/XNWZIC/4SWESY`、7,140 B、advertised MD5 `9b73267f5424cc9624c73bf1449d115f`，并含 `restricted:false` / `fileAccessRequest:true` 字段）。 | 不能说本地已经下载、实算 MD5、列出 ZIP，或以 API 字段保证本环境的实际传输。 |
| 2026-09-01 | [Workshop 3 report（DataverseNO file ID 268902）](https://dataverse.no/api/access/datafile/268902) | 文档性 file overview 说明 hydrofoil archive 的预期高层文件类别；正文描述受迫 stepped-sine FRF、无 MFC 激励的涡响应、30 次重复、hydrofoil instrumentation，以及 runner 的 R1–R4 pressure、五个 BEP 工况、STFFT uncertainty 描述。 | 不能说预期文件已经在 ZIP 内逐个读取，或文件内含原始 time histories、明确列名、单位、repeat IDs 与不确定度列。 |
| 2026-09-01 | [Bergan et al., 2018, *International Journal of Fluid Machinery and Systems*](https://doi.org/10.5293/IJFMS.2018.11.2.146) | 提供 hydrofoil 受迫/无受迫响应、lock-in 与 damping-sensitive 边界的已发表实验背景。 | 不能让其代替当前 Dataverse archive 的具体版本、数值列或训练/验证 split。 |
| 2026-09-01 | [Agnalt et al., 2018, *Shock and Vibration*](https://doi.org/10.1155/2018/5796875)；[Crossref metadata](https://api.crossref.org/works/10.1155/2018/5796875) | 正确书目信息是 2018，且论文以 six near-BEP conditions 的 pressure–accelerometer amplitude/phase information 拟合 34 个模型参数，并用 10,000 次 MCM 表达 fitted-parameter intervals；文章没有报告一个预先隔离的独立 holdout。 | 不把 model-fitting residual、`R²` 或 MCM parameter interval 叫作 external validation，也不把其 derived mode quantities 改写为 full structural stress/life truth。 |
| 2026-09-01 | 本环境的受限获取记录；没有可保存的 ZIP bytes。 | 对 file ID `268899` 的既有传输诊断未产生可信 binary；截至本日志时间点，没有 local MD5、`unzip -l`、checksum manifest 或 parsed schema。 | 不能从一次环境传输失败判断 archive 不存在、访问永远不可能，或反过来把文档说明当作替代品。 |

当前处置为 `archive evidence audit`，不是 `Research candidate`。若未来出现合法、可审计的 binary 获取渠道，强制顺序仍是：下载 provenance → local MD5/SHA-256 → `unzip -l`/integrity → schema/units/rawness/repeat manifest → grouped split；在此之前不训练、不拟合、不生成 benchmark 数字。
