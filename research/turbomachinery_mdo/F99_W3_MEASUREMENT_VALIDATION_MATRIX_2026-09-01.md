# Francis-99 Workshop 3：测量—派生量—不确定性—留出验证矩阵

**记录日期：** 2026-09-01（Asia/Shanghai）
**用途：** 为公开 FSI 基准做可反驳的证据分层；不是研究计划、训练记录、优化结果或投稿主张。
**当前处置：** `Archive evidence audit`。F99-W3 的 hydrofoil 是值得继续审计的公开 FSI 线索；它和 runner 均**尚未**构成可投稿的 AI 赋能叶轮机械 MDO 路线。

> **先说结论。** 当前公开元数据和 workshop 报告足以说明：同一 hydrofoil 试验包含受迫频响、无受迫涡脱落响应和重复试验；同一 Francis runner 试验包含随工况变化的机载压力测量，并有一篇把压力与一个加速度计信号共同拟合为声学—机械模型的论文。这是有价值的 FSI 验证背景。它不是共同设计向量上的多设计样本，也不是独立的 stress/life 真值，更不能把同一数据上的参数拟合称为留出验证。

---

## 1. 版本、文件和获取状态

| 项目 | 当前可核验事实 | 证据类别与来源 | 仍不能推出的内容 |
|---|---|---|---|
| 数据集版本 | DataverseNO 当前 API 的版本列表只返回一个已发布的 `V1.0`（dataset version ID `5574`）；其当前文件清单仍列出 `f99w3_exp_excitation.zip`，数据文件 ID `268899`、file PID `doi:10.18710/XNWZIC/4SWESY`、7,140 B、MD5 `9b73267f5424cc9624c73bf1449d115f`、`restricted:false`。 | [DataverseNO current V1 API](https://dataverse.no/api/datasets/:persistentId/versions/1.0?persistentId=doi:10.18710/XNWZIC)；一手元数据。 | API 声明不是本地文件校验；不能因 `restricted:false` 或页面可见而说本环境已成功取得 binary。 |
| 页面—API 不一致 | 先前读取的带 `version=1.0` 文件落地页显示过“已在 current version 删除或替换”的提示；但当前已发布 V1 API 明确列出同一 file ID、PID、大小和 MD5，且版本列表没有另一 current version。 | 文件落地页与上述 current API；界面/元数据冲突。 | 不能把旧落地页提示当作“当前文件不存在”的证据；也不能仅凭当前 ID/PID/MD5 宣称已核验某个历史存储副本的字节一致性。 |
| 本地取得状态 | 本地没有得到可信 ZIP。普通 CLI TLS、Node HTTPS、Jina ZIP 文本化、以及一次 Chromium 浏览器上下文的显式 Range 请求均未得到文件字节；最后一种在浏览器侧为 `TypeError: Failed to fetch`。 | 本轮传输日志；环境事实。 | 没有本地 MD5 比对、`unzip -l`、解压或逐列 schema 审计；不得把下文的 workshop 文件说明改写为 ZIP inventory。 |
| 文档所述 archive 结构 | Workshop PDF 说明该 ZIP **应**包含：`Francis-99.txt`、七个 `FRF_[X]ms.txt`、`noExcitation.txt`。 | [Workshop 3 report（当前 PDF file ID 268902）](https://dataverse.no/api/access/datafile/268902)，其文本提取读取到第 11/19 页的 “File overview”；文档性声明。 | 未读取 central directory 前，不能断言内部文件名、数量、大小、编码、列名、单位或是否与当前 ZIP 完全相同。 |

### 1.1 当前的数据合同边界

- Workshop PDF 把 hydrofoil 与 Francis runner 定义为**两个测试对象**：前者用于基础 FSI，后者用于应用型 runner FSI。它们可共享 workshop 背景，但不是同一几何、同一载荷链或可直接合并的样本表。[Workshop report](https://dataverse.no/api/access/datafile/268902)
- 当前 ZIP 标签和描述是 “Experimental data of the hydrofoil”。因此，runner 的压力表、论文拟合结果或任何后续 runner 文件，均不能被假定为该 ZIP 的实际内容。
- 当前 API 同时带有 `fileAccessRequest:true`。在本地成功取得并校验前，本记录将它视为平台设置字段，不把它解释为无需条件的实际传输保证。

---

## 2. 测量—派生量—不确定性—留出验证矩阵

表中“可设计的留出”是**预注册式验证要求**，不是已经做出的实验，也不是对 archive 内部行结构的假设。为避免把不同论文/报告的协议静默混合，表内 `W3` 指 [Workshop 3 report](https://dataverse.no/api/access/datafile/268902)，`B18` 指 [Bergan et al. (2018)](https://doi.org/10.5293/IJFMS.2018.11.2.146)，`A18` 指 [Agnalt et al. (2018)](https://doi.org/10.1155/2018/5796875)。缩写只定位来源；不把文档说明升级为 archive 字节审计。

| 对象 / 证据层 | 已由来源明确说明的直接测量或声明性文件内容 | 可由该来源支持的派生量 | 已说明的不确定性与处理 | 最小的独立留出验证设计 | 当前禁止的跃迁 |
|---|---|---|---|---|---|
| **Hydrofoil：主结果文件** | Workshop PDF 将 `Francis-99.txt` 描述为 hydrofoil 主结果：discharge、damping factor、natural frequency、试验段入口 gauge pressure；并称每一行来自该 discharge 下 30 次重复。试验使用磁流量计；文档将其 calibration uncertainty 说为约 0.1%（W3）。 | 按单一 discharge 汇总的阻尼比和湿态固有频率趋势；入口压力可作为该试验条件的记录量。 | 30 次重复说明存在统计基础，但该 PDF 没有给出该文本文件的列名、每行是否为均值/估计值、置信区间算法、pressure 单位或 covariance 处理。 | 以**整个 discharge/velocity 条件**为 group，而非把重复行随机拆分。用训练条件拟合的参数/代理预测从未参与选择的一个完整 velocity 条件的 damping 与 natural frequency，并预先报告 coverage、误差和失败条件。 | 不把重复聚合值说成原始时域信号；不将 hydrofoil 的 damping 当作 Francis runner 的 damping；不从这些量推出 stress、fatigue life 或几何优化收益。 |
| **Hydrofoil：受迫 FRF** | Workshop PDF 说明七个 `FRF_[X]ms.txt` 分别对应不同 discharge；文件名表示 bulk velocity，内容为 tested frequency、amplification factor、phase delay；每条 FRF 由 30 次重复组成。测试采用 stepped-sine，约 60 个激励频率/measurement，流速写为 0–25 m/s、每 5 m/s 一档（W3；hydrofoil 的 lock-in/damping 讨论另见 B18）。 | Bode/Nyquist 曲线；由曲线形状识别的 damping 与 natural frequency。相对幅值在 resonance 处被归一化为 1，因此绝对振幅不是该文件可直接验证的对象。 | stepped-sine 的目的为避免跨越 resonance 时的瞬态影响；多次重复用于 damping/frequency 的统计评估。公开描述没有冻结 FRF 的每次重复保存方式、驱动电压、绝对位移/应变标定和不确定度列。 | 留出**完整 FRF 的整速度条件**，且在模型选择前固定频率窗口、拟合器、峰值/相位准则和参数边界。另把未受迫数据保留为机制负对照，而非加入同一损失函数。 | 不把 normalized relative amplitude 当作绝对结构响应；不以随机频点拆分冒充外推；不把七个文件与“0–25 m/s、5 m/s 间隔”的六个名义速度自动调和。 |
| **Hydrofoil：无 MFC 激励** | `noExcitation.txt` 被描述为不同 discharge 下的 trailing-edge deflection amplitude 与 vibration frequency，代表未加 MFC 激励时的 hydrofoil 响应；文档把它称为 vortex-shedding interaction 的指示（W3；相应 lock-in 边界见 B18）。 | 给定 flow condition 的无受迫最大尾缘位移及对应主振动频率；可作为受迫 FRF 之外的独立响应类型。 | 文档描述的是 “maximum amplitude with a corresponding frequency”，故至少是摘要性/派生性量；未说明 time history、重复次数、置信区间、峰值提取规则或传感器间一致性。 | 预先锁定 lock-in 区和非 lock-in 区，用未参与调参的**连续速度段**验证：模型能否同时拒绝错误的共振解释、并复现幅频趋势。若无时间序列或明确重复结构，只能做描述性外部比较。 | 不把“vortex-shedding indication”升级为已识别的因果载荷；不由最大值记录推导 damping；不称其为独立 life/strain 真值。 |
| **Runner：workshop 压力表** | Workshop PDF 给出四个 flush-mounted runner pressure sensors（R1–R4）的坐标和传感器类型；五个 BEP 工况记录 `Q`、`nED`、`QED`、`H`、guide-vane angle、speed。表 3/4 给出 fundamental 和 second-harmonic guide-vane-passing pressure amplitudes，单位为相应 head 的百分比。 | 不同工况、sensor location 和 RSI harmonic 下的归一化压力载荷；可用作结构分析的 prescribed pressure-loading benchmark。 | 文件说明：压力链静态 dead-weight calibration；动态不确定度因链路共振高于 10 kHz 而被假定很低；幅值误差含 95% measurement uncertainty 和 STFFT 得到的 95% amplitude variation。该 PDF 写 100 RSI periods、50% overlap（W3）。 | 将一个或多个**整工况**留出，且保留全部 R1–R4/harmonic 作为关联向量；以冻结的 pressure-field reconstruction 预测留出工况的相位和幅值。若没有相位或原始时间序列，就不能声称预测了完整 excitation field。 | 不把四点 pressure table 说成全 blade pressure field、位移、应力或疲劳真值；不以同一表拟合后再回报同一表的误差作为独立验证。 |
| **Runner：Agnalt 等的 pressure–accelerometer 模型** | 论文说明四个 runner-hub pressure sensors 与一个邻近入口的 accelerometer；六个近 BEP 测量（BEP1–BEP6）提供 5 个传感器的 amplitude/phase 信息，共 60 个数据点。其模型把 total pressure 拆为 convective 与 acoustic components，并联立两个 acoustic-mechanical modes（A18）。 | 论文内的模型参数、convective/acoustic pressure shapes、两个估计 eigenfrequencies 和 damping laws。文章报告：34 个参数以加权非线性最小二乘拟合；参数不确定度用 10,000 次 Monte Carlo simulation 给 95% intervals（A18）。 | 压力传感器：静态 calibration、1 Hz repeatability、in-air vibration sensitivity；accelerometer 数据手册的 1% relative uncertainty；STFFT 用 50 RSI periods、每个窗口相同相位起点。论文还明确承认低 head 的首点 phase 不拟合，且 measurement count/frequency step 可能限制精度。 | 只有拿到有 provenance 的 amplitude/phase 数据和冻结代码后，才可进行 group leave-one-condition-out：不在留出转速/头条件重拟合 34 参数，预测所有 pressure 与 acceleration 的复数响应；另留出一个 sensor 做空间外推检查。所有拟合、选择和置信区间均不得接触留出点。 | 不能将同一 60 点上的 `R²` 或 residual plot 叫 external validation；不能把 pressure-model 的结果误称为逐点测得的 structural mode 或 stress truth；不能假定论文的六工况和 workshop 表的五工况可一一拼接。 |

### 2.1 物理测量链的已知与未知

| 项目 | 有来源支持的陈述 | 尚未核验、因此不能写入模型输入的陈述 |
|---|---|---|
| Hydrofoil 构型 | 150 mm × 150 mm test section；250 mm chord、12 mm thickness，距 leading edge 150 mm 后渐缩至 4.5 mm；aluminum alloy；zero angle of attack；双侧 MFC 以 180° phase-separated sine 驱动弯曲；尾缘附近有 semiconductor strain gauges 和 LDV（W3；B18）。 | MFC force/voltage calibration、实际阻尼 estimator、每个 velocity 的原始 drive/response time histories、strain-to-stress transfer、材料参数和边界约束的可复现数值值。 |
| Runner 构型 | Francis-99 为 1:5.1 model；14 stay vanes、28 guide vanes、15 blades + 15 splitters；runner inlet/outlet diameters 0.63/0.347 m。压力计为 R1–R4，且报告提醒 bolt assembly、trailing-edge gap、crown holes/cable channels 可致非对称与 strain 不确定性（W3；A18）。 | 未公开并经本地审计的 full geometry/mesh/constraint/material/bolt pretension；全表面动态压力、同步 strain/位移历史、可直接用于 life calculation 的应力或材料模型。 |
| 论文—workshop的测量协议 | 两者都描述压力 calibration、RSI amplitude、振动敏感性与重复/统计处理（W3；A18）。 | Workshop 写 100 periods/50% overlap，Agnalt 论文写 50 periods/same relative start；在获得原始 provenance 前，不能悄然选取其中一个当作唯一实际协议。 |

来源：hydrofoil 与 workshop runner 信息见 [Workshop 3 report](https://dataverse.no/api/access/datafile/268902)；hydrofoil damping/lock-in 边界见 [Bergan et al., 2018 PDF](https://www.jstage.jst.go.jp/article/ijfms/11/2/11_146/_pdf)，DOI [`10.5293/IJFMS.2018.11.2.146`](https://doi.org/10.5293/IJFMS.2018.11.2.146)；runner pressure–accelerometer model、uncertainty与拟合限制见 [Agnalt et al., 2018, *Shock and Vibration*](https://onlinelibrary.wiley.com/doi/10.1155/2018/5796875)，DOI [`10.1155/2018/5796875`](https://doi.org/10.1155/2018/5796875)。

---

## 3. 已确认的边界、矛盾和负对照

### 3.1 不能混合的证据

| 不允许的替换 | 原因 | 正确处理 |
|---|---|---|
| 用 hydrofoil 的 FRF/damping 验证 runner 的结构响应 | 两者的结构、安装、激励、传感器、流动和目标均不同。 | 分成两个 benchmark card；若未来研究要转移方法，必须把 transfer 当作待测假设并留出整个对象。 |
| 用 runner 的机载 pressure amplitude 取代 runner stress/strain/life 真值 | pressure loading 与 structural response/life 间仍缺 geometry、material、constraint、full load mapping和独立 structural measurement。 | runner 当前最多为 pressure-loading / harmonic-response validation context。 |
| 把 Agnalt 的 fitted eigenfrequency/damping 当作由独立 holdout 测得的完整 truth | 这些值由同一测量集上的 34 参数模型拟合而来；文章本身将它们描述为 estimates。 | 报告它们为 published derived targets，并要求 condition/sensor group holdout 或独立实验才能评价泛化。 |
| 把 `noExcitation.txt` 的峰值记录当作 FRF 或 damping measurement | 文档只说明最大尾缘响应及相应频率；这不是受控输入—输出 FRF。 | 用作无受迫/lock-in 负对照，且保持其峰值摘要的证据级别。 |
| 把 workshop 指定的 FSI topic 当作设计空间 | 公开资料提供的是一个固定硬件和若干工况，不是系统性 geometry/material/cooling design database。 | 在没有新的可审计共同设计—真值案例前，不称为 MDO dataset。 |

### 3.2 必须保留的未解决项

| 未解决项 | 证据 | 对后续工作的影响 |
|---|---|---|
| ZIP 的真实文件表、列、单位、编码与 rawness | Workshop 的 file overview 只给高层说明；本地没有 ZIP bytes。 | 任何 parser、split、模型、图表或数值结果均不得启动。 |
| “七个 FRF”与 0–25 m/s、5 m/s 步长的关系 | 前者意味着 7 个 separate-discharge files；后者列出 6 个名义速度。 | 不能擅自补出第七速度或将文件名映射到速度。 |
| workshop 的五个 BEP 条件与 Agnalt 的六个条件 | Workshop table 从 `Q=0.134 m³/s` 起；论文另含 `Q=0.107 m³/s`，并有不同的 `BEP` 命名/覆盖。 | 在有原始文件、date/case identifiers 和处理代码前，只能并列叙述，不能合并为一个 11 点或 6 点训练表。 |
| STFFT protocol difference | Workshop：100 periods + 50% overlap；论文：50 periods + same relative position。 | 不可无说明地沿用其中之一估计 uncertainty；它是需要版本/源文件核验的 protocol item。 |
| lock-in 区的独立阻尼真值 | 已读 hydrofoil 文献提示约 9–12 m/s 的无受迫涡响应显著，而可靠的 independent damping estimates 不足；受迫 FRF 还出现 excitation-amplitude sensitivity。 | 该区域可以是敏感 FSI negative control，但不是无保留的 independent truth；不把该现象用作“新机制”或直接优化依据。 |

---

## 4. 当前能成立的验证阶梯

| 层级 | 能够以现有公开文档支持的工作 | 必需的反例 / 留出 | 当前不够支持的结论 |
|---|---|---|---|
| L0 — provenance | 冻结 current API 的 dataset/file PID、大小、MD5、license 与文档版次；记录 UI/API 不一致。 | 重新读取 current version JSON，并在取得 bytes 后比对本地 MD5。 | “archive 已审计”或“可复现数据已在本地”。 |
| L1 — 文件/schema | **仅在** ZIP 获取后：`md5sum`、`unzip -l`、每个文件的 header/encoding/units/rawness/repeat identifier manifest。 | 解析失败、列数/单位与 PDF 不一致、缺少 expected files 都必须写入 manifest。 | 由 workshop PDF 代替实际 schema。 |
| L2 — 单对象 FSI 描述 | hydrofoil：受迫与无受迫响应分开描述；runner：pressure harmonic 与拟合派生参数分开描述。 | 留出完整 velocity/condition groups；状态/振幅敏感区与非敏感区都要报告。 | 跨对象泛化、完整 FSI closure、结构寿命或 MDO。 |
| L3 — 模型验证 | 对一个固定对象，以冻结 schema、grouped split、校准/coverage 和预定义 failure mode 验证。 | hydrofoil 的 lock-in/非 lock-in negative controls；runner 的 condition/sensor holdout，且不得在留出点调参。 | 一个同数据 fit 的 `R²`、视觉曲线相似或单一 published parameter 即可证明模型可用。 |
| L4 — 设计决策 / MDO | 需要多个可制造设计、共同 operating conditions、aero/structural truth、明确 objective/constraint 与未参与训练的回算。 | 独立 designs、independent physics/experiment、强基线和完整失败样本。 | 基于固定 hydrofoil 或固定 runner 的工况扫掠被称作叶片级多学科设计优化。 |

---

## 5. 主张台账与对抗性复读

### 5.1 本文件保留的主张

| 表述 | 证据类别 | 邻近来源 | 不得扩展成 |
|---|---|---|---|
| 当前 DataverseNO V1 API 列出具有指定 ID/PID/MD5/size 的 hydrofoil ZIP。 | 一手元数据事实。 | [current V1 API](https://dataverse.no/api/datasets/:persistentId/versions/1.0?persistentId=doi:10.18710/XNWZIC)。 | 本地 checksum 已验证或 archive 内容已读取。 |
| Workshop PDF 说明 hydrofoil archive 的预期高层文件类别，并说明 30 次重复、FRF 与无激励响应。 | 文档性/实验说明事实。 | [Workshop 3 report](https://dataverse.no/api/access/datafile/268902)。 | ZIP 内部实际清单、列语义或原始时序已经审计。 |
| Agnalt 等给出由 pressure–accelerometer data fitting 得到的 acoustic/convective、frequency 和 damping estimates，并报告 MCM intervals。 | 已发表的模型派生结果。 | [Agnalt et al.](https://onlinelibrary.wiley.com/doi/10.1155/2018/5796875)。 | 独立 structural truth、逐点应力或无条件的 numerical-validation target。 |
| 当前 F99-W3 资料可用于严格的固定对象 FSI benchmark 审计，但不形成 MDO 数据合同。 | 基于测量对象、设计变量缺失与验证链的范围判断。 | 上述数据/论文资料及本文件 L4 所列缺口。 | F99 永远不能支持任何未来不同问题；或数据集没有科研价值。 |

### 5.2 红旗检索与审稿人质疑

对本文件人工检查了 `first`、`novel operating mode`、`solved`、`guarantee`、`certificate`、`proves`、`exact`、`state of the art`、`all`、`always`、`never`，以及 `首次`、`新颖`、`保证`、`证书`、`证明`、`完全`、`所有`、`总是`、`永远`、`可投稿`。命中只出现在否定/限定、来源性事实或明确的留出协议语境；没有将 archive、拟合或文档描述宣传为无条件的研究成果。

| 对抗性角色 | 最强质疑 | 本记录的回答 |
|---|---|---|
| FSI 实验专家 | “30 次重复是否等于可用的原始重复样本？” | 否。文档只证明重复存在；binary manifest 必须确认每个文件保留的是原始重复、平均/拟合结果还是别的汇总。 |
| 结构动力学专家 | “为什么不用 published frequency/damping 直接标定并声称验证？” | 它们是与同一测量联合拟合的派生 estimates；同数据拟合只能检验残差，不替代 condition/sensor holdout 或独立试验。 |
| 数值分析者 | “能否从七条 FRF 曲线证明 lock-in damping 的普适规律？” | 不能。步骤、激励振幅、协议和未受迫响应的 schema 仍未核验；已知 amplitude sensitivity 和 lock-in gap 要求负对照。 |
| MDO 审稿人 | “哪里有共同设计向量与跨学科优化真值？” | 当前没有。固定硬件上的工况与激励扫掠不等于多设计的 aero–structure–life MDO。 |
| 编辑 | “这是不是已可投稿的 AI 路线？” | 不是。这是将可能误用的数据/论文证据切分为可验证层级的审计记录。 |

---

## 6. 任何后续升级前的强制顺序

1. 以未尝试、可审计的合法 binary 传输路径取得 ZIP；保存 source PID、时间、bytes、MD5 和 SHA-256。
2. 先运行 `md5sum` 对照 `9b73267f5424cc9624c73bf1449d115f`，再运行 `unzip -l` 和 archive integrity test。
3. 对每个实际文件生成 schema/rawness/units/repeat/case-id manifest；将文档预期和实际内容逐项比对。
4. 冻结对象级 grouped split、拟合器、基线、负对照、指标与停止条件；任何 numerical result 都必须在此之后。
5. 只有出现共同设计变量、跨学科耦合真值、独立回算以及敌对新颖性审计后，才可另起一项 MDO 候选评估；不得将该步骤回填为 F99-W3 已经具备的条件。
