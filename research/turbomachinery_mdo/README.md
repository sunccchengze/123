# AI 赋能叶轮机械多学科设计优化：取证式候选台账

**状态：`Archive only / 尚未形成 Research candidate`**
**审查日期：2026-09-01（Asia/Shanghai）**
**适用范围：郭振东、宋立明老师及课题组公开可核验的研究边界。GE-E3 与 Pak-B 是已审计的首批资源；FAN-02 是已审计的真实离心风机 FSAI 实验线索；SPLEEN C1 是已审计的公开高速度 LPT 气动—二次空气相互作用线索。现有资源的 `Archive only`/release-incomplete/`Question candidate` 处置不排除继续以同一 G0–G6 门槛审计其他公开耦合验证体系。**

这不是论文草稿、投稿承诺或“首创”声明。它是一个否定性但可复查的研究立项记录：在严格区分数据实际包含的变量、已经发表的近邻工作和验证阶梯后，目前不能诚实地把现有两套公开数据拼接为“真实叶片级 AI-MDO”。

## 一页结论

1. **团队能力与课题方向是明确匹配的。** 宋立明教授官方页列出“透平机械多学科精细优化设计与数据挖掘”“随机不确定性量化与不确定性优化设计”“内部复杂流动换热冷却”等方向；郭振东副教授官方简介列出叶轮机械智能设计优化、智能流场预测、数据挖掘、UQ 与鲁棒/可靠性优化。详见 [证据与检索日志](EVIDENCE_AND_SEARCH_LOG_2026-09-01.md#1-公开能力边界)。
2. **能力匹配不等于数据能支持每一种论断。** GE-E3 是同一叶栅/级几何与工况变量下的流动场资料；Pak-B 是另一对象上孔布局 SDF 到端壁表面温度场的资料。现有公开资料没有证明二者存在共同设计向量、共同样本编号，或 CFD–CHT–结构/寿命的可验证闭环。
3. **把二者分别训练、融合、做多保真/鲁棒优化或普通端壁布局优化不能作为新方向。** 同一团队的 MSFO 已在 GE-E3 叶片优化和涡轮端壁气膜布局上验证多/单保真融合；团队的 SDNO 已以 Pak-B 的孔数外推和 Sellers 叠加原理为中心。详见 [候选台账](CANDIDATE_LEDGER_2026-09-01.md#3-已关闭路线)。
4. **“热—应力—蠕变/TMF/寿命 + 制造偏差 + AI”也不能仅改名重启。** GT2023 和 GT2025 的 Siemens 工作已分别覆盖内部冷却燃机叶片的应力、蠕变应变、位移与寿命代理，以及 airfoil stacking/rotation、壁厚、肋位置、冷却供气和热气边界偏差下的 3-D Transformer neural-operator lifing。
5. **最后一个暂存问题 Q-IO 也已关闭。** 沿 SDNO 的被引链核验到 Chen et al. (2025) 的气膜 interaction decomposition / error-source tracking / nonlinear superposition，以及 Yao et al. (2025) 的 vortex-encoded AI 密集孔布局修正；Zhang (2023) 和 Qiu (2024) 又已覆盖气膜/叶片的主动加点。它们使 Q-IO 不能再把“孔（排）交互的物理解释、AI 修正或追加 CFD”作为新核心；余下的 error-ranking/拒答是无 Pak-B 真值合同支撑的通用 reliability wrapper。故目前连 `Question candidate` 也没有，更不可能称为 MDO。详见 [Q-IO 关闭审计](CANDIDATE_LEDGER_2026-09-01.md#4-q-io已关闭的审计问题保留为反例)。
6. **“unpaired data fusion / OT / latent alignment”不是补救。** 不配对资料的 statistical matching 至多能在额外、可辩护约束下给出部分识别集合；MDO 则要求耦合模型与共同设计变量。当前 GE-E3/Pak-B 连这类约束的可验证来源也没有，因此不能让算法臆造跨数据集物理关系。详见 [R9](CANDIDATE_LEDGER_2026-09-01.md#3-已关闭路线) 与 [取证](EVIDENCE_AND_SEARCH_LOG_2026-09-01.md#31-不能用unpaired-data-fusion补出-mdo-耦合)。
7. **高发散探索已完成首轮图谱，但没有绕过门槛。** 新增的 25 条路线覆盖场接口、损伤路径、临界区切换、随机场、瞬态运行、制造、冷却、拓扑、因果场学习、逆设计和 MDO 数据图；其中仅 5 条仍是待原文级反证的窄线索，2 张卡片带有单学科 `S` 标记（L1 与 `R` 重叠；L3 还需要范围外 paired RANS/URANS 真值），19 条为已关闭、阻断或仅属工具。没有一条同时通过共同耦合对象（G0）和敌对新颖性（G2），故状态仍是 `Archive only`。详见 [高发散候选图谱](CANDIDATE_ATLAS_2026-09-01.md)。
8. **FAN-02 证明了一个真实 FSAI 测量体系值得继续追踪，却尚未提供可重放的公开测量数据合同。** 当前 Zenodo record 的 `/files` 清单只有 3 个 STEP 与 8 个传感器坐标 TXT，未列出论文所述 PIV、压力、振动、声学时序或共同 run key。它暂列为未来 release/contact-dependent reference，不被误写成已可训练、可独立验证或可优化的 benchmark。详见 [FAN-02 release-content audit](FAN_02_RELEASE_AUDIT_2026-09-01.md)。
9. **SPLEEN C1 是值得继续审计的真实气动—二次空气 interaction benchmark，但不是当前的完整 MDO 路线。** 主 v5 record 公开声明 cavity/purge/wake、flow/loss/pressure 类观测及 cavity/secondary-air documentation；独立 PIV archive 是 steady reference-cavity/no-wake 子集。已发表 SPLEEN 工作直接覆盖 purge–wake 平均/非定常二次流、steady off-design loss 以及含 preliminary data-driven transition/turbulence model 的 closure 研究。当前仍缺逐试次 pairing、raw/processed hierarchy、独立 holdout 和同一对象的热—结构—寿命真值，故仅为 `Question candidate / only G0 passed`。详见 [SPLEEN C1 evidence-and-kill audit](SPLEEN_C1_EVIDENCE_KILL_AUDIT_2026-09-01.md)。

## 文件导览

| 文件 | 作用 |
|---|---|
| [CANDIDATE_LEDGER_2026-09-01.md](CANDIDATE_LEDGER_2026-09-01.md) | 既有候选、直接近邻、G0–G6 状态、处置与可杀死条件。 |
| [CANDIDATE_ATLAS_2026-09-01.md](CANDIDATE_ATLAS_2026-09-01.md) | 新增 25 条跨方法/跨学科路线的机制、近邻、最小验证、强基线、G0–G6 风险和 kill criterion；不是论文题目清单。 |
| [EVIDENCE_AND_SEARCH_LOG_2026-09-01.md](EVIDENCE_AND_SEARCH_LOG_2026-09-01.md) | 已核验的官方页、原始论文/会议页、代码/数据目录，以及检索查询边界（含图谱的新增敌对检索）。 |
| [REENTRY_REQUIREMENTS.md](REENTRY_REQUIREMENTS.md) | 若未来获得共同耦合真值后，什么条件下才能重新立项为真实 MDO。 |
| [F99_W3_MEASUREMENT_VALIDATION_MATRIX_2026-09-01.md](F99_W3_MEASUREMENT_VALIDATION_MATRIX_2026-09-01.md) | Francis-99 Workshop 3 的文档级测量—派生量—不确定性—留出验证矩阵；明确标为 archive-unverified，不能替代 ZIP/schema 审计。 |
| [FAN_02_RELEASE_AUDIT_2026-09-01.md](FAN_02_RELEASE_AUDIT_2026-09-01.md) | FAN-02 论文级实验覆盖与当前 Zenodo release 文件清单的逐项分离；当前仅能作几何/传感器布局参考。 |
| [SPLEEN_C1_EVIDENCE_KILL_AUDIT_2026-09-01.md](SPLEEN_C1_EVIDENCE_KILL_AUDIT_2026-09-01.md) | SPLEEN C1 的 record/version/condition contract、直接相邻论文、G0–G6、公开性边界与可杀死的重入条件；当前是 `Question candidate`，不是完整 MDO。 |
| [SELF_AUDIT_2026-09-01.md](SELF_AUDIT_2026-09-01.md) | 对本轮关闭结论与新增证据审计的主张类别、引文邻接、interaction 假设和对抗性复读；不是投稿审查通过证明。 |
| [tools/](tools/README.md) | 不依赖网络的 provenance-manifest 工具及临时伪文件测试；供未来合法取得 binary 后先核验版本，不解释物理语义。 |

## 严格术语

本文档只在下列全部成立时使用“真实叶片级 MDO”：

- 一个可追溯的共同设计向量 \(x\) 同时影响至少两个学科；
- 学科间至少有一个真实耦合链，例如 \(x\to\) 外/内流与热边界 \(\to T_{metal}\to\sigma\to\) 寿命，而不是把无关样本的标量并排；
- 每个关键输出有真值、求解器验证或独立实验的明确来源；
- 优化后的候选能够在未参与训练的数据或独立求解中回算；
- 所谓“安全”“鲁棒”“寿命提升”等结论有相应的约束、统计与验证支撑。

仅有两个分别来自涡轮领域的数据集、两个代理，或一个加权目标，都不满足上述定义。

## 立即允许与禁止的工作

**允许（取证、复现准备）：**

- 固定公开数据版本、下载清单、checksum、MAT schema、样本分割和许可；
- 对已有 SDNO/MSFO 做可复现基线，而不改名为新方法；
- 写明变量—输出—学科耦合图，识别数据泄漏、split 不一致和不可验证环节；
- 将已关闭路线的新增直接前例、数据版本证据和审计边界持续补入台账；任何全新候选都必须从 G0/G2 重新开始，而非复用 Q-IO 名称。

**禁止（在当前资源下）：**

- 将 GE-E3 与 Pak-B 的独立预测结果拼成 CFD–CHT–FEA–寿命 MDO；
- 以缺失的金属温度、冷却流量/压损、材料、应力、寿命或制造标签填充目标函数；
- 把 SDNO、MSFO、普通 FNO/U-Net、NSGA-II、BO、多保真、UQ 或 safe/conformal wrapper 重命名为新机制；
- 声称已运行 CFD、CHT、FEA、优化或外部验证。本仓库尚未下载原始大型数据、训练模型或生成仿真结果。

## 数据可得性澄清

通过网页层面的目录访问，已确认 MindScience/OSInfra 公开列出了 GE-E3 与 Pak-B 文件；这纠正了“完全不存在公开链接”的误解。**但可见目录不等于已获取、校验或可重现实验。** 当前命令行直接 TLS 下载仍返回 `SSL_ERROR_SYSCALL`，且没有任何原始 MAT 文件写入本仓库。两套资料的样本数/分割描述还存在互相矛盾之处，必须先冻结实际二进制版本。详见 [§2.5](EVIDENCE_AND_SEARCH_LOG_2026-09-01.md#25-数据可达性与未解决版本冲突)。

FAN-02 的当前 Zenodo release 具有不同的、已实际读取的内容缺口：record `17909944` 的 `/files` API 列 3 个 STEP 和 8 个传感器坐标 TXT，而非论文级流、压、振、声测量数据。它不能用来弥补 GE-E3/Pak-B 的断开数据合同；其完整判断见 [FAN-02 release-content audit](FAN_02_RELEASE_AUDIT_2026-09-01.md)。

## 审查纪律

- “未找到”仅表示在列出的日期、数据库和查询下未定位到同一对象；不是世界范围的无先例证明。
- 任何新方法先写出问题、真值、理论命题、负对照、最近三篇直接前例和停止条件，再开始训练。
- 本目录与旧风电 P1/P2/P3 归档完全分离；不得将旧术语、结论或论文包装迁移到叶轮机械项目。
- 若未来拟投稿，作者必须独立理解、复算和自行撰写投稿稿件，并复核目标期刊届时有效的 AI、作者和数据政策。
