# 研究记录的清晰度与主张审计（2026-09-01）

**审计对象：** `README.md`、`CANDIDATE_LEDGER_2026-09-01.md`、`CANDIDATE_ATLAS_2026-09-01.md`、`EVIDENCE_AND_SEARCH_LOG_2026-09-01.md`、`REENTRY_REQUIREMENTS.md`、`F99_W3_MEASUREMENT_VALIDATION_MATRIX_2026-09-01.md`。

**使用的本地工作流：** `scholarly-clarity-auditor` 与 `interaction-structure-miner`。它们是仓库内的检查清单；本文件不是人工导师审批、同行评审、投稿合规证明或“humanizer”规避记录。

**结论：** 这些文件可作为一个清晰的 `Archive only` 取证记录继续保留。它们不是论文草稿，未达到 `Research candidate`，更不构成提交资格。

---

## 1. 主张—证据台账

| 保留的表述 | 证据类别 | 支撑 | 不能扩展成什么 |
|---|---|---|---|
| GE-E3 与 Pak-B 未被公开证据连接为共同设计向量上的 CFD–CHT–FEA–寿命链。 | 基于公开接口的范围判断。 | 官方数据页、MindScience README/`dataset.py`，以及缺失字段/共享 ID 的明确记录。 | 不能断言任何私有数据永远不存在。 |
| Pak-B 当前公开训练接口读取 `sdf`、`Temperature`、`Grids_x`、`Grids_y`，并默认随机置换 padding SDF channels。 | 一手代码事实。 | `dataset.py` 的已记录读取与 preprocessing 行为。 | 不能由此把 `Temperature` 称为金属温度、流量、压损、应力或寿命。 |
| Chen et al. 2025 I/II、Yao et al. 2025 对 Q-IO 的物理 interaction 核心构成实质直接近邻。 | 书目/摘要事实 + 编辑判断。 | 出版商页和 Crossref 摘要中明确的 decomposition、error-source tracking、vortical interaction、nonlinear superposition、vortex-encoded AI。 | 不能说它们复现了 Pak-B 的每一个样本、split 或未发表实验。 |
| Q-IO 在当前约束下关闭。 | 研究门槛决定，而非普遍数学定理。 | 上述直接前例、R7 的通用-wrapper 禁止、Pak-B 未审计数据合同。 | 不能说全球不存在同类窄问题；未来不同机制/数据合同必须另起 G0/G2。 |
| OT、latent alignment 或 unpaired data fusion 不能把 GE-E3/Pak-B 变成可验证 MDO。 | 一般识别理论 + MDO 定义下的范围判断。 | statistical matching 的 partial-identification 文献与 MDO coupled/shared-variable 要求；当前资料缺少可验证的共同锚点。 | 不否定未来在新增共同变量、物理约束或 paired truth 下做部分识别研究的可能性。 |
| 当前没有运行训练、CFD/CHT/FEA、优化或数据实验。 | 工作区事实。 | 本轮操作日志与无 MAT binary 的记录。 | 不能报告误差、速度、覆盖率、Pareto 或工程收益。 |

## 2. 邻近引文检查

| 邻近主张 | 已检查的来源 | 仅使用的明确内容 | 遗留风险 |
|---|---|---|---|
| 多排交互的分解、误差来源与涡机制已发表。 | Chen et al. 2025 I，DOI `10.1063/5.0276858`。 | 出版商/Crossref 摘要说 decomposition theory 经实验与数值验证、逐排贡献/error source、kidney-vortex row-to-row interaction。 | 付费正文未精读；未推断其没有或具有所有 Q-IO 模块。 |
| 非线性二维 superposition correction 已发表。 | Chen et al. 2025 II，DOI `10.1063/5.0293895`。 | 摘要说以 vortex-induced velocity/turbulent diffusion 量化 row interaction，并从 single-row 延至 multi-row。 | 不把双排/多排的范围扩大为任意高孔数定理。 |
| 涡编码 AI 已用于密集孔 superposition。 | Yao et al. 2025，DOI `10.1063/5.0260945`。 | 摘要说 vortex-encoded AI、four-channel U-Net、Sellers operations、dense layouts 与 high-prediction-error areas。 | 后验误差区域不等价于事前 calibrated abstention；该差异也没有被冒称为新颖性证明。 |
| 气膜中的 ML + UQ/敏感度不是空白。 | Wang et al. 2022/2023，DOI `10.1016/j.ijheatmasstransfer.2022.123353` / `10.1063/5.0132989`。 | MLP/ANN surrogate 与 MC/Sobol 的输入参数不确定性传播。 | 不将 input UQ 错称为 surrogate OOD/model-error calibration。 |
| 主动加点/查询不是剩余贡献。 | Zhang et al. 2023，DOI `10.3389/fmech.2022.973293`；Qiu et al. 2024，DOI `10.1016/j.applthermaleng.2024.122481`。 | 前者在 endwall-like 气膜洞中做 sequentially adaptive sampling + BO + PSP 验证；后者在高温叶片多源随机因素下使用 active-learning sampling。 | 这不是 Pak-B 的逐样本协议，但足以阻止将“主动追加 CFD”本身卖作新机制。 |

## 3. interaction-structure-miner 检查

| 必要项 | 当前状态 | 对结论的限制 |
|---|---|---|
| 数学对象 | 仅定义抽象集合函数 `F(S,z)`；`S` 是孔集合、`z` 是空间位置。 | 这是论证低阶观测不能无条件识别高阶集合项的形式边界。 |
| 变量单位、排序和固定孔身份 | 未核验。 | 不可对实际 Pak-B 字段求导、估计 Möbius 项或赋予图边物理意义。 |
| 嵌套子布局、空布局基线、case IDs | 未核验。 | 不可把不同样本的低孔/高孔数据当成同一布局的子集干预。 |
| 物理依赖图与正则性 | 未建立。 | 未进行 mixed partial、有限差分、局域性或单调性主张。 |
| 数值反例/网格收敛 | 未运行。 | 没有任何数值 interaction 结果、定理证明或优化保证。 |

该检查支持的是**停止不当物理解读**，不是一个新的 interaction 方法或投稿级理论贡献。

## 4. 红旗与可读性检查

对审计对象人工检查了 `首次`、`新颖`、`保证`、`证书`、`证明`、`完全`、`所有`、`总是`、`永远`、`state of the art` 等销售化/绝对化词汇的语境。

- 正则红旗检索的命中均是“不得声称首次/保证”等否定语境、来源范围限定或本段的审计说明；未保留“首次”“已解决”“保证”“安全证书”“state of the art”一类未受条件约束的中心主张。
- “关闭”“不能”均限定为**当前提案、当前公开资源和现有证据**，而非关于领域全体文献或私有数据的全称命题。
- “未定位/未裁定”明确标注为检索或访问边界，未被转换成无前例证明。
- 将过长的 Q-IO 历史拆为“原问题、前例、为何残余差异不足、kill-criterion 审计、G0–G6 终态”，使读者可区分来源事实、逻辑限制和编辑决定。
- 2026-09-01 已用 GitHub Markdown API（GFM 模式）成功渲染本目录 6 个 Markdown 文件；再以 `github-slugger@2` 检查 6 个本地 fragment link，均解析到目标标题。此为格式/链接检查，不验证网页外链的持续可达性或引文事实。
- 同日对 44 个非二进制外链做只读 `curl --head --location` 传输探测，并刻意排除 2 个此前失败的 MindScience 数据下载路径。仅 GitHub 项目链接返回成功；其余 43 个跨 DOI、Crossref、出版社、学校站点等不同域名都在此 shell 环境报同一 `OpenSSL SSL_connect: SSL_ERROR_SYSCALL`。该跨域一致的环境级 TLS 失败不能证明任一引用失效，且不再对这些 URL 做无差别重试；已由 `fetch_page`/网页检索实际读取过的来源仍按日志中的取证状态表述。

## 5. 对抗性复读

| 审稿角色 | 最强质疑 | 当前答案 |
|---|---|---|
| 气膜/传热专家 | “孔间 interaction、Sellers 偏差、涡机制为什么新？” | 不是新；Chen、Yao、Yang、Gao 已使该叙事关闭。 |
| 数值分析者 | “从低孔布局能否识别高阶项？是否有收敛或误差证书？” | 不能无条件识别；没有实际 data contract、数值实验或证书。 |
| 数据科学者 | “calibration/abstention/query allocation 是否只是成熟的 reliability pipeline？” | 是当前的剩余风险，且没有领域特异机制和独立真值合同，因此不以此立项。 |
| 数据融合/因果专家 | “为何不用 OT、生成模型或 shared latent space 对齐两套资料？” | 没有共同对象、共同 \(x\)、配对真值或可验证的物理桥接约束；所得 coupling 只能是不可检验的先验。partial identification 也需要明确约束，不能提供唯一的物理耦合。 |
| 实验/验证专家 | “优化候选在哪里回算？Temperature 的物理语义是什么？” | 没有回算；公开接口只支持端壁表面 `Temperature`，不越界命名。 |
| 编辑 | “MDO 的共同设计和多学科耦合在哪里？” | 不存在于当前 GE-E3/Pak-B 公开合同；结论是 Archive only，而不是勉强投稿。 |

## 6. 审计后的行动约束

1. 不以任何 Q-IO 同义名训练模型、写论文或声明一项新方法；
2. 若数据传输问题合法解决，先产生 version/hash/schema/split manifest，而不是跳到性能实验；
3. 若未来允许新的耦合数据或 CFD/CHT/FEA 资源，先用 `REENTRY_REQUIREMENTS.md` 的数据合同和 G0–G2 开启**不同**的问题；
4. 任何投稿文本须由作者独立理解、核查并按届时期刊政策自行撰写。本审计不替代该责任。

---

## 7. 高发散候选图谱的二次审计

### 7.1 可保留的、精确限定的表述

| 表述 | 为什么可以保留 | 不能扩展成什么 |
|---|---|---|
| 新图谱列出 25 条路线。 | `CANDIDATE_ATLAS_2026-09-01.md` 的总览表有 25 个唯一 ID：F1–F5、T1–T5、P1–P5、L1–L5、W1–W5。 | 不是声称已经穷尽整个叶轮机械/AI/MDO 文献。 |
| 其中 5 条为 `R`，2 张卡片含 `S`，另有 19 条为 `B/C/A`。 | 状态是对本轮的研究处置，不是方法真伪或发表价值的普遍判定。`R` 为 F1/F3/F4/P1/L1；含 `S` 的是 L1/L3，故 L1 在前两类中重叠。 | `R` 不是“有希望发表”；`S` 更不是“已满足 MDO”。 |
| F3 的新颖性门槛因 equivalent-fatigue-load 与 damage-ROM/load-path 文献而提高。 | 新增来源的摘要/开放正文明确讨论 damage/failure equivalence、结构不确定性，及高维 load-path 的耗散/BO 选择。 | 不从不同结构/材料例子推断已在涡轮 CHT–FEA–life 链上完成同一实验。 |
| F1、F3、F4 的“最小合法验证”需要同一共同设计上的 coupled truth。 | 这由本项目对“真实 MDO”的术语定义及各方法所需下游决策检验推出。 | 不是说只有一种合法实验；它列的是不低于该强度的必要证据类型。 |
| L1/P1 即使通过各自的单学科实验，也不自动升级为 MDO。 | GE-E3/Pak-B 的断开数据合同仍未改变。 | 不把 OOD、因果表示、PH 或 cooling-surface field prediction 写成热—结构—寿命 MDO。 |

### 7.2 引文邻接与反例检查

- **F1：** Coelho (2008)、CPOD (2010)、Yano (2020) 分别占据 MDO 接口压缩、多目标 QoI/Pareto ROM、气动 PDE 输出误差控制。故图谱没有把“goal-oriented/interface/Pareto”组合称首创；F1 的唯一残余对象是经独立校准的高维接口误差是否足以翻转真实下游决定。
- **F3：** 除 general scenario reduction、random-field optimization、fatigue active learning 外，新增 `Equivalent fatigue load` 和 Goury et al. (2016) 是关键负对照。故其卡片明确规定：若“joint damage distribution + hotspot identity + design variation”不能与这些对象逐式区分，关闭。
- **F4/P1：** hotspot ROM、普通热优化、TDA/PH 与 Pareto topology 都被当作相邻/排除证据，而不是用作“领域尚未研究”的论据。其 proposed event/topology labels 先要求 threshold/mesh negative controls，防止后验叙事。
- **L1：** IRM/causal representation、causal-graph MDO、turbomachinery GNN 和 geometry/condition neural fields 都是强基线或范围反例。只有实际 binary 显示可解释的干预结构后，才允许使用因果措辞；随机环境标签必须是 negative control。

### 7.3 结构与写作红旗检查

- 图谱刻意将 **“最小合法验证”** 与 **“当前能做的工作”** 分离；前者不是资源承诺，后者仍禁止训练、CFD/CHT/FEA 和性能报告。
- 所有 `certificate`、`safe`、`causal`、`damage-equivalent` 等强词均附有条件、校准边界或 kill criterion；没有将形式不等式、toy PDE 或摘要检索写成工程保证/理论证明。
- 一处草拟时产生的零宽字符已在本地清除；未保留不可见的语义变体或文档混淆字符。
- 图谱的来源登记将“开放正文”“出版社摘要”“开放预印本”分开。其引用只支撑登记表中明确的题目/摘要事实；准备论文前必须全文级复核。

### 7.4 审计结论

高发散并未改变本项目的核心负结论：**当前没有一个经 G0/G2 同时通过的 AI 叶轮机械 MDO 研究候选。** 它的正面价值是将“继续探索”限制为五条有明确 first-disproof 的窄线索，并把 20 条已关闭、阻断或降级路线保存为可回查反例。任何下一步若跳过原文级邻接核验、binary manifest 或 coupled-truth 合同，均违反本审计。

---

## 8. Francis-99 Workshop 3 文档矩阵：增量清晰度审计

**本节审计对象：** `F99_W3_MEASUREMENT_VALIDATION_MATRIX_2026-09-01.md`，以及为索引和来源登记而改动的 `README.md`、`EVIDENCE_AND_SEARCH_LOG_2026-09-01.md`。

**审计性质：** 应用仓库本地 `scholarly-clarity-auditor` 的 claim-ledger、citation-adjacency、red-flag 和 adversarial-read 流程；它不是外部 `Supervisor-Skills` 审阅、作者身份认证、同行评审或投稿许可。

### 8.1 主张—证据台账

| 保留的表述 | 分类 | 邻近证据 | 必须保留的限制 |
|---|---|---|---|
| 当前 V1 API 列出指定 F99 ZIP 的 ID、PID、advertised MD5 和大小。 | 一手元数据事实。 | Matrix §1 中的 [DataverseNO current V1 API](https://dataverse.no/api/datasets/:persistentId/versions/1.0?persistentId=doi:10.18710/XNWZIC)。 | API 不是本地 checksum；不称已下载或已读取 ZIP。 |
| Workshop report 说明预期 archive 文件类别和实验协议。 | 文档性实验/文件说明。 | Matrix §1/§2 中的 [Workshop 3 report](https://dataverse.no/api/access/datafile/268902)。 | 不将其改写成实际 archive inventory 或已知 schema。 |
| hydrofoil、runner 和 Agnalt fitted model 的量被拆分为 direct measurement context 与 derived targets。 | 证据分类/解释。 | Matrix §2 中分别紧邻 `W3`、`B18`、`A18` 的来源缩写和 direct links。 | 不把 model-derived frequency/damping、normalized FRF 或 pressure table 升格为 independent structural/life truth。 |
| F99-W3 可继续作为固定对象 FSI benchmark 的取证线索，却不是 MDO data contract。 | 条件性范围判断。 | Matrix §3–§4 所列共同设计、binary/schema、coupled truth 和 holdout 缺口。 | 不说它没有科研价值，更不说它永远不能支持未来不同问题。 |

### 8.2 引文邻接检查

- `F99_W3_MEASUREMENT_VALIDATION_MATRIX_2026-09-01.md` 的 §1 每一条 metadata/file-availability 主张在同一表格行附直接 API/report link；不以 landing-page UI 代替 current API。
- §2 在表前定义可点击的 `W3`、`B18`、`A18`，并在每一对象行的来源性描述处标记其适用缩写；§2.1 的 hardware/protocol assertion 也标有相应来源。该布局刻意阻止将 runner 的协议移植到 hydrofoil，或将 report 的 100-period STFFT 写成 Agnalt 论文的 50-period protocol。
- §5 的 claim ledger 再次逐条附来源，且把“本地没有 binary”“fit 不是 holdout”“固定对象不是 MDO”写成范围限制而非引用无法支撑的领域全称。
- 本轮只将来源用于其已读取/可见的明确内容。引用可达性仍受本环境 TLS 限制；链接格式检查不等于重新下载文献、ZIP 或其所有补充材料。

### 8.3 红旗与可读性检查

- 对新增 matrix 及本节的核心结论逐项检查 `first`、`novel operating mode`、`solved`、`guarantee`、`certificate`、`proves`、`exact`、`state of the art`、`all`、`always`、`never`，以及 `首次`、`新颖`、`保证`、`证书`、`证明`、`完全`、`所有`、`总是`、`永远`、`可投稿`。
- 命中只允许出现在否定/限定、来源性事实、文档标题、或预注册的 grouped-holdout 协议中；不保留无条件的“首创”“已解决”“精确验证”“可投稿”中心主张。
- 矩阵先明确 `direct / declared / derived / unresolved`，随后才写验证设计，避免一句话同时将 paper result、archive 内容和未来模型结果折叠在一起。

### 8.4 对抗性复读与未解决风险

| 角色 | 应当追问的反例 | 审计后的处理 |
|---|---|---|
| 数据管理人 | “file overview 是否证明 ZIP 的真实目录和 units？” | 否；matrix 把 `md5sum`、`unzip -l`、schema/rawness/units manifest 列为模型前硬门槛。 |
| FSI 实验者 | “30 repeats、FRF 和 unexcited peak 是同层级原始数据吗？” | 否；matrix 保留 repeat storage、peak extraction、time history 和 calibration 的未知项。 |
| 结构动力学审稿人 | “已发表的 34-parameter fit 能否证明外推？” | 否；同一 60 个 amplitude/phase data points 的 fit 不能替代 frozen condition/sensor holdout。 |
| MDO 审稿人 | “固定硬件的工况扫描为何不是多学科设计优化？” | matrix 要求共同可制造设计、耦合 truth 和 independent design-level recalc；缺任一项均不得称 MDO。 |
| 编辑 | “这是否已经是一项可投稿研究？” | 否；这是原始数据到达前的可反驳证据分类，且明确没有计算、优化或性能结果。 |

**尚未消除的核心风险：** F99 ZIP 没有本地可信 bytes；无 local MD5、`unzip -l`、内部 schema/units/rawness/repeat map；seven-FRF/velocity relation 未解；five-/six-condition 与 100-/50-period protocol 不能合并；lock-in 区缺足够的独立 damping truth。因此 matrix 的通过只表示写作中的证据类别与语言边界相符，不表示 archive 可复现、研究路径成立或投稿就绪。

### 8.5 作者与政策边界

若将来使用任何 F99 资料形成研究或投稿，具名作者仍须独立核验原始数据、代码、物理解释和目标期刊当时的作者/AI/data policy，并自行撰写承担责任的论文文本。本地审计清单不能替代这些义务。

---

## 9. FAN-02 release-content audit：增量清晰度审计

**审计对象：** `FAN_02_RELEASE_AUDIT_2026-09-01.md`，以及对本目录 `README.md`、`CANDIDATE_LEDGER_2026-09-01.md` 和 `EVIDENCE_AND_SEARCH_LOG_2026-09-01.md` 的相邻索引更新。

### 9.1 主张—证据台账

| 保留的表述 | 分类 | 邻近证据 | 不能扩展成什么 |
|---|---|---|---|
| 当前 FAN-02 `/files` endpoint 有 11 个 entries，且内容为 3 STEP + 8 sensor-position TXT。 | 一手 manifest 事实。 | [Zenodo file API](https://zenodo.org/api/records/17909944/files)；独立审计 §2 逐项列 key、bytes 和 advertised MD5。 | 不说已下载/本地 hash，也不推断其他 revision 或私有/companion 存档。 |
| 论文描述多模态 FSAI 实验，但当前清单没有列出支撑该分析的测量文件。 | 论文描述与 manifest 范围的比较。 | [FAN-02 overview](https://www.mdpi.com/2504-186X/11/1/10) 与上述 API 相邻呈列。 | 不质疑实验、作者或未来数据计划；只判断当前 public payload 不能证明数据合同。 |
| 当前不能作跨模态训练、grouped holdout 或 MDO 回算。 | Gate/G0–G5 的范围判断。 | 明确的 run key、raw/derived measurements、conditions/calibration、design intervention、replay/holdout 缺项表。 | 不说 FAN-02 没有科学价值或永远不能成为 benchmark。 |
| 通用离心风机壳体厚度/质量—声学 surrogate optimization 不可作为未来默认方案。 | 邻接前例带来的编辑边界。 | 2012 与 2019 centrifugal-fan vibroacoustic optimization 的直接链接与限定范围。 | 不把两篇前例误说成已穷尽所有 FSAI 机制。 |

### 9.2 引文邻接、红旗与对抗性复读

- 每项外部事实相邻链接到 record metadata、file endpoint、overview paper 或具体前例；没有用论文 abstract 替代文件清单，也没有用 file name 替代测量内容。
- 对 `first`、`novel`、`guarantee`、`certificate`、`proves`、`exact`、`all`、`always`、`never` 及其中文对应词做了语境检查。保留的“当前”“未列出”“不能”均锚定在 record/revision、文件清单和本项目数据合同，不是全称领域判断。
- **实验者的反例：**真实测量可存在于未公开/后续资源中；文本明确承认这一点。**数据管理人的反例：**API list 可以更新；re-entry 要求重冻结 revision/manifest。**MDO 审稿人的反例：**CAD 可供设计；但缺少 objective/constraint truth 和 independent replay，不能跳到优化主张。**新颖性审稿人的反例：**未找到完全相同 FAN-02 优化不是新颖性证明；文本因此把 generic route 置于前例边界下。

### 9.3 审计结论

FAN-02 增补没有改变“继续发散、但不降低门槛”的研究策略。它保留了一个真实 FSAI 体系的可追踪价值，同时以当前 release 内容阻止一个不可复现的模型/优化故事进入候选阶段。该审计不是投稿审查通过、不是实验复现，也不替代将来对完整数据与前例全文的独立核验。

---

## 10. SPLEEN C1 evidence-and-kill audit：增量清晰度审计

**审计对象：** `SPLEEN_C1_EVIDENCE_KILL_AUDIT_2026-09-01.md`，以及 `README.md`、`CANDIDATE_LEDGER_2026-09-01.md` 的相邻索引更新。

**审计性质：** 已应用仓库本地 `doctoral-research-gatekeeper` 和 `scholarly-clarity-auditor` 的 claim-ledger、citation-adjacency、red-flag 与 adversarial-read 流程。它不是外部 `Supervisor-Skills` 审阅、人工导师认可、同行评审或投稿合规证明。

### 10.1 主张—证据台账

| 保留的表述 | 分类 | 邻近证据 | 不可扩展为 |
|---|---|---|---|
| SPLEEN C1 是公开、真实的 high-speed LPT cascade 气动—二次空气相互作用测试体系。 | 一手 record/同行评议 test-case 事实。 | Zenodo v5/PIV records 与 `10.3390/ijtpp10010002`。 | 不等价于完整旋转发动机级、全 MDO 或已下载的数据。 |
| v5 record 声明 cavity geometry 与 secondary-air-system documentation；v1 CAD 存在可追溯 stagger-angle 版本风险。 | 一手 record metadata 事实。 | v5/v1 Zenodo record/API 链接。 | 不在未读 archive members 前宣称字段、单位、cavity-family 数量或正确的 file-to-run mapping。 |
| PIV 是同一 C1 的 steady `Cavity Aref`, no-WG, TG on/off 子集，不能自动充作 WG-on/purge 独立验证。 | metadata 范围事实 + 逻辑判断。 | PIV record `10253213` 与 `10.1115/1.4063674`。 | 不把“同项目/同叶栅”写成跨仪器逐试次配对。 |
| 宽泛的 purge–wake 平均/非定常机理、steady off-design loss 和 ML closure 主张已受直接 SPLEEN 前例约束。 | 原文/abstract scope 事实 + 编辑新颖性判断。 | `10.1115/1.4063878`、`1.4067674`、`10.3390/ijtpp11010014`、`1.4069487`。 | 不声称穷尽一切窄问题；只关闭与前例对象、变量、输出和验证实质相同的宽泛提法。 |
| SPLEEN 目前仅是 `Question candidate / only G0 passed; G1–G6 incomplete`。 | Gate 结论。 | 缺失的 run map、raw/processed hierarchy、independent holdout、本地 binary manifest 与真正的 decision consequence。 | 不写成失败、无价值，或已经可以投稿的路线。 |

### 10.2 Citation-adjacency 与 red-flag 检查

- 新文件有 16 个唯一外链；均为 Zenodo record/API、DOI、NASA NTRS 或 Mexnext 官方页面。没有将搜索结果 URL 用作引文，也没有把 record-level 描述升级成未读 archive member 的 schema。
- `10.1115/1.4067674` 的具体条件/输出取自 Crossref/publisher abstract，且文字明确标为该证据范围；`10.1115/1.4069487` 的 data-driven transition/turbulence statement 取自 ASME abstract，不将其未读完整训练细节臆测为事实。
- 已检查 `首次`、`新颖`、`完成`、`完整`、`证明`、`保证`、`first`、`novel`、`solved`、`guarantee`、`certificate`、`proves`、`exact`、`state of the art`、`all`、`always`、`never`。命中的“首次”仅在被前例关闭的提法中出现；其他词均处于范围限制、未完成状态或本审计方法说明中，没有无条件的正向成果主张。
- `git diff --check` 已通过。外链 inventory 是语法/来源类别检查，不替代本环境无法完成的 shell TLS 链接可达性检查或下载校验。

### 10.3 对抗性复读和残余风险

| 角色 | 最强反驳 | 审计后处理 |
|---|---|---|
| LPT experimentalist | record 表示有 technical documents，何以说条件合同未通过？ | document existence 与 file/run/instrument matching 是不同命题；先取得并审计 README、technical notes 和 binary manifest。 |
| CFD/ML reviewer | 仍可换一个新网络做 SPLEEN。 | 网络名称不是机制；必须逐项与已含 preliminary data-driven model 的 `1.4069487` 区分，并展示独立决策价值。 |
| MDO reviewer | purge、loss 和多个工况已是多学科优化。 | 当前最多为 aero–secondary-air operating/measurement space；没有同对象 thermal-solid-life truth 时不得称 full MDO。 |
| data scientist | PIV、probe、pressure 同属一个项目，合训合理。 | 同项目不证明同试次；缺 matching key 前，合训属于不可审计的 pairing assumption。 |
| editor | 为何保留而不立即关闭？ | 已关闭的是宽泛命题；仍允许用完整文档来检验是否存在不同、可反驳的窄 decision question。若没有独立 intervention/holdout 或已被相邻文献覆盖，按 audit 的 kill criteria 降为 `Archive only`。 |

**审计结论：** 此增补保持了“继续发散寻找真实耦合体系”与“不降低证据标准”之间的边界。它记录 SPLEEN 的真实公开价值和明确的前例压力，但不把 archive-access 限制、检索歧义或项目同源性误写成数据缺失、文献空白或可投稿 AI-MDO。
