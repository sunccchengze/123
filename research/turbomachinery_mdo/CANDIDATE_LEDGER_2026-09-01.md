# 候选—前例—淘汰台账：AI 赋能叶轮机械 MDO

**版本：2026-09-01**
**判定框架：** 本仓库的 [`doctoral-research-gatekeeper`](../skills/doctoral-research-gatekeeper/SKILL.md) G0–G6；它是透明的本地工作流，不是声称获得外部导师审批。
**总体状态：** `Archive only / 尚未形成 Research candidate`。

---

## 1. 事实层：团队研究边界与不可越过的基线

### 1.1 经公开资料核验的能力边界

| 公开来源 | 可核验事实 | 本项目中的正确用法 | 不能由此推出的内容 |
|---|---|---|---|
| 宋立明官方研究领域页 | 列有多学科精细优化/数据挖掘、优化设计系统、随机 UQ/不确定性优化、内部复杂流动换热冷却。 | 证明本题与团队长期的叶轮机械、UQ、优化与冷却能力相接。 | 不能自动证明某一新算法没有被团队或他人做过。 |
| 郭振东官方简介 | 公开写有叶轮机械智能设计优化、智能流场预测、数据挖掘、UQ、鲁棒性/可靠性优化。 | 证明 AI + 流场 + UQ/RDO 的能力边界。 | 不能把个人简介替代具体论文、数据或验证证据。 |
| Song et al., 2012；团队官方代表论文页 | 已有 “Automated Multi-objective and Multidisciplinary Design Optimization of a Transonic Turbine Stage”。 | 任何“首次团队进行叶轮机械 MDO”的宽泛表述均不可用。 | 不判定所有未来 MDO 细分机制均已穷尽。 |
| Song et al., GT2017；官方代表论文页 | 已有知识驱动高温叶片气动热多学科优化。 | 任何“首次 AI/知识驱动高温叶片气动热 MDO”的宽泛表述均不可用。 | 不替代对具体新机制的论文级检索。 |
| Wang et al., *J. Turbomach.*, 2024 (MSFO) | 以 GE-E3 叶片优化和涡轮端壁气膜布局作为验证对象，提出多/单保真代理融合优化。 | 排除 GE-E3/Pak-B 上普通多保真、DBSCAN 局部融合、HF/LF 网格融合、代理筛选等路线。 | 不证明所有 fidelity-aware 方法都无差异；差异必须事先精确定义和验证。 |
| Wang et al., *Physics of Fluids*, 2024 (SDNO) | Pak-B 端壁孔数外推；SDF 输入；Calculate Net + Superposition Net；以 Sellers 叠加机理辅助 Transformer neural operator。 | 排除“孔数外推 + SDF + 叠加神经算子”作为新机制。 | 不证明所有可靠性/失效审计问题已解决；但不能只给 SDNO 再套一个通用置信区间。 |

所有链接、DOI 和原文级摘录边界见 [证据日志](EVIDENCE_AND_SEARCH_LOG_2026-09-01.md)。

### 1.2 最小真实 MDO 证据图

设 \(x\) 是**同一个**可制造设计；\(a\) 是工作条件；\(y_A,y_T,y_S,y_L\) 分别为气动、热、结构和寿命输出。一个可验证的叶片级 MDO 至少应有：

```text
x, a ──► CFD / 气动场 ──► 热边界或流量分配
  │                                │
  ├────────────────────────────────┘
  ▼
CHT（金属温度、热通量、冷却压损/流量） ──► FEA（应力/变形） ──► lifing
  │                                       │
  └──► 有共享样本 ID 的验证、独立回算 ◄────┘
```

当前公开材料最多支持两个断开的片段：

```text
GE-E3: x_GE, a_GE ──► 3-D 流动基本物理场 ──► 后处理气动性能
Pak-B: x_Pak（孔布局 SDF） ──► 端壁表面 Temperature 场
```

目前没有公开证据证明 \(x_{GE}=x_{Pak}\)，没有 Pak-B 的压损/质量流量/金属温度/应力/寿命标签，也没有 GE-E3 与 Pak-B 之间可审计的热—结构传递。因此它们的并列不能变成上图的耦合边。

---

## 2. 数据能力与版本风险账本

| 数据资产 | 已公开、可核验的内容 | 不能当作已具备的内容 | 对 MDO 的结果 | 当前状态 |
|---|---|---|---|---|
| GE-E3 HPT 流场 | 官方页称第一高压涡轮单通道（S1 + R1）；96 几何 + 4 边界变量；Numeca 3-D CFD。MindScience README 写入 \(x,\alpha,p\) 并输出 \(p,T,V_x,V_y,V_z,\rho\)，且可后处理性能。 | CHT 固体域、冷却孔/内部流路、金属温度、材料、应力/变形、蠕变/TMF/HCF 标签、实验闭环。 | 是**气动/流场代理**资源；不是单独的耦合 MDO 真值。 | 未下载二进制；字段和样本行数待 header 校验。 |
| Pak-B 端壁气膜 | 官方页称孔数可变的高自由度布局和端壁表面温度场。开源 `dataset.py` 只读取 `sdf`、`Temperature`、`Grids_x`、`Grids_y`。 | 冷却质量流量、压损、外部/内部完整流场、CHT 金属温度、材料、热应力、寿命、共享 GE-E3 变量。 | 是**单一端壁热场**代理资源；不是“气动—热—结构 MDO”数据。 | 未下载二进制；公开版本描述有冲突。 |
| FAN-02 enclosed centrifugal fan FSAI release | 直接 [Zenodo `/files` API](https://zenodo.org/api/records/17909944/files) 当前列 3 个 STEP 几何与 8 个传感器位置 TXT；论文另描述真实风机上的流、压、振、声测量。 | 当前清单未列 PIV/HWA、压力/LSV/声学测量、共同 run ID、工况/校准表、结构声学输入、设计干预或独立回算。 | 当前只能作 geometry/sensor-layout reference；不能训练跨模态 FSAI 模型、做 grouped validation 或称为 MDO benchmark。 | `release-content incomplete`；不是对实验或未来 release 的否定。详见 [FAN-02 audit](FAN_02_RELEASE_AUDIT_2026-09-01.md)。 |
| NASA EEE CFD/重构几何 | 可作为未来公开 HPT 流场参考，并有 `turbo-design` 说明。 | 共同设计变量的 CFD–CHT–FEA–寿命样本闭环；原始硬件的无差异几何。 | 不能自动补齐 GE/Pak 的耦合断边。 | 不在当前限定资源内；未下载。 |
| U-bend CHT 数据 | 成功 CHT 解、流/固温度字段、28 几何变量及部分网格/求解失败记录。 | 叶片外流、气膜端壁、结构应力/寿命、真实燃机 MDO 标签。 | 未来可作“仿真工作流/失败标签”负载测试；不可外推为叶片 MDO。 | 不在当前限定资源内；未下载。 |

### 2.1 必须先冻结的版本冲突

这不是枝节：如果训练/验证 split、孔数或总样本数不确定，任何 “OOD”“few-shot”“数据效率”结果都没有可重复的基线。

| 冲突 | 目前可见证据 | 允许的结论 | 禁止的结论 | 解决动作 |
|---|---|---|---|---|
| GE-E3 样本数 | 官方数据页写“5000 个样本、4000 训练、900 验证”（算术上为 4900）；MindScience README 写 4900；目录文件名为 `*_6000.mat`。 | 存在可公开访问的 GE-E3 打包数据与描述不一致。 | “GE-E3 精确有 N 个样本”或基于未核验 split 报告泛化。 | 下载轻量 `designStruct` 后做 MAT header/shape/checksum；再以原始 field MAT 的实际行数冻结 manifest。 |
| Pak-B 总数和孔数 | 官方页写 2510、仅 1/2/3/5/10 孔；legacy README 写 2730、包括 15/20 孔；当前目录只列 1/2/3/5/10 的 train/test 文件。 | legacy README 不能被视为当前数据真相。 | 同时援引 2510 与 2730；声称已对 15/20 孔作测试。 | 下载后对每个 MAT 记录字段、shape、样本数、hash；按实际二进制生成一个版本化 manifest。 |
| Pak-B 通道/样本语义 | 公开 `dataset.py` 的 `padding_data` 将每样本 SDF 通道 padding 至 10，并在默认参数下随机置换通道；代码未显示 case ID 或 0 孔 reference field。 | 当前开源训练接口具有孔通道 permutation 的实现细节，且空布局基线是否存在尚未证实。 | 直接把 `sdf` 当成带不变孔 ID、可作集合 Möbius 分解的样本；假定存在无孔温度场。 | binary manifest 必须记录原始 channels、shuffle seed/语义、case IDs（若有）和 0 孔/参考温度的来源。 |
| Pak-B 嵌套子布局关系 | 当前页面和 README 说按孔数分别生成样本，但未证明某个 10 孔案例的 1/2/3/5 孔案例是其对应子集，也未公开该对应表。 | “有低孔数样本”不等于“观测了同一布局的低阶交互”。 | 声称已从非配对不同布局中估计某一高孔数案例的物理 Möbius/ANOVA interaction component。 | 核验 layout generator、case IDs 与 subset mapping；若不存在，只能研究预测性 risk score，不能解释为已识别的物理高阶项。 |
| FAN-02 论文—release 范围差异 | overview 论文说明多类 FSAI 测量；record `17909944` 当前 `/files` inventory 为 3 STEP + 8 sensor-position TXT。 | 当前 release 提供 CAD/位置，不足以推出论文级测量记录、同步关系或 schema 已公开。 | “论文写有实验，所以当前 dataset 已能训练/验证”；或反过来声称数据永远不存在。 | 若新 release 出现，冻结 revision 与 manifest，先审计 rawness、units、run/session ID、clock/calibration 与 paired modality map。 |
| 下载可达性 | 网页抓取可列 OSInfra 目录；命令行 `curl` 在本环境 TLS 协商时返回 `SSL_ERROR_SYSCALL`。 | 链接公开可见但本环境尚未形成可复现本地数据副本。 | “数据已下载/运行”；将网页目录当作数据校验。 | 不进行无差别重试；仅在决定进行合格复现后，换可审计传输路径并记录文件 hash。 |

---

## 3. 已关闭路线

关闭表示：**不能以当前宽泛提法作为新论文核心。** 它不否认未来可能存在一个定义清楚、机制不同、验证足够的窄问题。

| ID | 曾考虑的路线 | 直接近邻或致命缺口 | Gate 判定 | 处置 |
|---|---|---|---|---|
| R1 | “融合 GE-E3 与 Pak-B 的 AI 多学科优化” | 两套数据对象/变量/样本断开；没有 CHT–FEA–寿命真值。把结果并列不是耦合。 | G0 失败；G4/G5 无法独立验证。 | **关闭。** 只能称两个单学科 benchmark，不能称 MDO。 |
| R2 | GE-E3/Pak-B 上的普通 multi-fidelity、粗细网格、局部融合或 surrogate screening | Wang et al. 2024 MSFO 已在**同一 GE-E3 与端壁气膜布局应用**上做 MFS+SFS 自适应融合优化。 | G2 直接先例；若没有不同理论命题和公平强基线则 G1/G5 亦失败。 | **关闭。** 不得用名称、采集函数或网络替换制造表面差异。 |
| R3 | “首个 AI 高温叶片气动热/CHT MDO” | 团队已有高温叶片气动热 MDO、端壁冷却/气动热研究；外部已有 CHT + DL + MOGA 叶片气膜优化。 | G2 失败；若仅用 Pak-B 表面温度则 G0/G4 也失败。 | **关闭。** |
| R4 | GE/Pak 上的普通 UQ、RDO、NSGA-II/GA 端壁布局优化 | 团队官网和论文已有 UQ/RDO、端壁不确定性、MSFO；领域内已有 EA/BO/GA/CGAN 气膜优化。 | G2 失败。 | **关闭。** |
| R5 | “制造偏差 + 热边界 + 应力/蠕变/TMF/HCF/寿命 + Transformer/NO” | Abdallah et al. 2023 与 GT2025-151212 直接覆盖内部冷却燃机叶片的 lifing 代理、几何和边界偏差；Qiu et al. 2024 又结合 active-learning sampling、thermal-fluid-structure 代理与 LCF probabilistic-life 评估。当前 GE/Pak 没有其所需结构/lifing 真值。 | G0、G2、G4 三重失败。 | **关闭。** 除非未来逐项证明问题定义、真值、理论机制、验证梯完全不同。 |
| R6 | U-bend 失败记录 + safe/failure-aware Pareto | U-bend 不是叶片，且无结构寿命；SafeOpt/hidden constraint BO/conformal surrogate UQ 已高度相邻。 | 当前 G2 未通过；不符合限定数据与工程主张。 | **不立项。** 只保留外部方法学线索。 |
| R7 | “对 SDNO 加 OOD detector/conformal interval 后做可靠优化” | 高维场 CP、OOD surrogate UQ、conformal inverse design 已有直接通用方法；Pak-B 未提供优化后的独立 CFD 回算预算。 | G2 未通过；G4/G5 缺少优化闭环。 | **关闭。** 不能以 wrapper 立项。 |
| R8 | Q-IO：以“高阶孔 interaction → error ranking / abstention / CFD-query allocation”作为论文核心 | Chen et al. 2025 I/II 已对多排气膜提出并验证 decomposition/error-source tracking 与非线性涡相互作用模型；Yao et al. 2025 已以 vortex encoding + AI 修正密集孔布局 superposition；Zhang 2023 和 Qiu 2024 又分别覆盖气膜 sequential adaptive sampling 与叶片 active-learning sampling。剩余的可靠性/查询层既无 cooling-specific 新机制，也没有 Pak-B 的可审计 nested layout 与独立真值合同。 | G2 核心物理叙事被直接近邻覆盖；G4 未通过；残余层落入 R7 的通用 wrapper。 | **关闭。** 不把“尚未找到完全相同四件套论文”误写成新颖性。 |
| R9 | 以 partial identification / optimal transport / unpaired data fusion “补出” GE-E3–Pak-B 耦合后再做 MDO | statistical matching 的非联合观测问题本来就只可在明确 maintained assumptions 下做 partial identification；MDO 的共同系统模型又要求耦合模型与 shared design variables。GE-E3/Pak-B 当前没有相同对象、共同 \(x\)、跨学科锚点、成对样本或可验证耦合规律。 | G0/G3/G4 失败。任意 learned coupling 都是不可由现有数据反驳的先验选择。 | **关闭。** 不能用 OT/生成模型/latent space 把断边伪造成测得耦合。 |

---

## 4. Q-IO：已关闭的审计问题（保留为反例）

**关闭日期：2026-09-01。**
**结论：** Q-IO 不能在“仅公开 GE-E3/Pak-B、无新增 CFD/CHT/FEA 资源”的条件下作为论文候选，更不能被称为 MDO。这里的“关闭”是对这一个已定义提案的编辑与研究门槛判定；**不是**声称世界上绝不存在任何与其措辞相似的窄问题。

### 4.1 原问题与原先的边界

**原暂用名称：** *Compositional extrapolation audit for film-cooling layout surrogates*。

其原始问题是：对训练仅见低孔数、预测高孔数的端壁气膜代理，是否能识别“由未观测高阶孔相互作用导致、因此不应自动相信”的布局，并把该不确定性转化为拒答或追加真值求解的优先级？

将布局表示为孔集合 \(S\)，空间位置为 \(z\)，输出为 \(F(S,z)\)。形式上可以写 Möbius/ANOVA 分解：

\[
  \Delta_A F(z)=\sum_{B\subseteq A}(-1)^{|A|-|B|}F(B,z),\qquad
  F(S,z)=F(\varnothing,z)+\sum_{\varnothing\ne A\subseteq S}\Delta_A F(z).
\]

若真值只覆盖 \(|S|\le m\)，一般情况下 \(|A|>m\) 的交互项不能由低阶观测唯一确定：可构造两个在全部低阶布局上相同、在高孔数布局上不同的集合函数。这个结论只是一个**定义性不可识别性边界**；它不证明 Pak-B 已提供 \(F(\varnothing,z)\)、固定孔身份、成对 nested subset，或可辨认的物理高阶项。公开 `dataset.py` 还会在默认设置下随机置换 padding 后的 SDF 通道。

因此，即使在关闭前，Q-IO 也从未有资格声称“安全证书”“真实金属温度/寿命改善”或 MDO；它最多是一个待证的单学科代理可靠性问题。

### 4.2 关闭触发：直接的 2025 前例已覆盖其物理核心

下表只写已从出版社页面或 Crossref 摘要核验的内容；并不把未获全文的细节臆测成事实。

| 已核验前例 | 页面/摘要明确内容 | 对原 Q-IO 的影响 |
|---|---|---|
| [Chen et al., 2025 I, *Physics of Fluids*, DOI 10.1063/5.0276858](https://doi.org/10.1063/5.0276858) | 对多排气膜提出并以实验与数值验证 decomposition theory；将各排贡献拆开以追踪 error source；在四种横向间距的双排构型中，将非线性误差归因于 kidney vortices 的行间相互作用。 | 直接消解“提出/解释气膜孔（排）交互与误差来源”的物理核心新颖性。它是双排，不等于高孔数 Pak-B 的完全相同数据协议；但已足以使 Q-IO 不能将 interaction decomposition/local mechanism 作为新理论卖点。 |
| [Chen et al., 2025 II, *Physics of Fluids*, DOI 10.1063/5.0293895](https://doi.org/10.1063/5.0293895) | 基于 Part I 建立非线性二维 superposition 模型，以涡诱导速度量化行间交互；摘要报告无额外模型参数地从单排扩展到多排，并给出相对误差与耗时。 | 消解“interaction-aware correction / 可扩展 superposition”作为独特工程机制的空间。不能把一般的集合分解符号改名后与它并列投稿。 |
| [Yao et al., 2025, *Physics of Fluids*, DOI 10.1063/5.0260945](https://doi.org/10.1063/5.0260945) | 为密集孔气膜 superposition 提出 vortex-encoded AI：四通道 U-Net 与 Sellers operation 结合；摘要报告改善高预测误差区域并扩展到 dense layouts。 | 对“用局域涡/交互表示 + AI 修正密集布局失效”的组合形成直接近邻。其报告的是后验真实误差区域，而非 Q-IO 声称的事前 calibrated ranking；这个差别不足以自动构成新颖性。 |
| [Yan et al., 2025, *Physics of Fluids*, DOI 10.1063/5.0274462](https://doi.org/10.1063/5.0274462) | physics-informed 网络用时域、频域与 residual branches 处理孔型、孔排结构和气动参数，并专门加权 Sellers 下游高误差区；摘要报告多排 extrapolation。 | 再次排除把“定位误差敏感区 + 残差修正 + 多排外推”包装为独特贡献。 |
| [Yang et al., 2021, *International Journal of Thermal Sciences*, DOI 10.1016/j.ijthermalsci.2020.106774](https://doi.org/10.1016/j.ijthermalsci.2020.106774)；[Gao et al., 2025, *Processes*, DOI 10.3390/pr13010143](https://doi.org/10.3390/pr13010143) | 前者用卷积 ML 量化 effusion-cooling 多孔 superposition effect、分析邻孔贡献并在随机布局上验证；后者以能量守恒/主流温度修正分析多排 Sellers 累积偏差。 | 早已使“ML 量化 interaction”“随机多孔布局泛化”“Sellers 失效的物理修正”不能再作为 Q-IO 的独立贡献。 |
| [Wang et al., 2022, *International Journal of Heat and Mass Transfer*, DOI 10.1016/j.ijheatmasstransfer.2022.123353](https://doi.org/10.1016/j.ijheatmasstransfer.2022.123353)；[Wang et al., 2023, *AIP Advances*, DOI 10.1063/5.0132989](https://doi.org/10.1063/5.0132989) | 分别用 ML 代理 + MC/Sobol 对 trench / 涡发生器气膜的输入几何、工况不确定性和敏感度进行传播分析。 | 排除“气膜 surrogate + UQ + sensitivity”的宽泛叙事。它们主要是输入不确定性传播，不能偷换成模型误差或 OOD reliability；但该语义区分本身也不是一项新方法。 |
| [Zhang et al., 2023, *Frontiers in Mechanical Engineering*, DOI 10.3389/fmech.2022.973293](https://doi.org/10.3389/fmech.2022.973293)；[Qiu et al., 2024, *Applied Thermal Engineering*, DOI 10.1016/j.applthermaleng.2024.122481](https://doi.org/10.1016/j.applthermaleng.2024.122481) | 前者在 endwall-like 横向压力梯度中做 film-cooling surrogate/BO 的 sequentially adaptive sampling 并 PSP 验证；后者对高温叶片多源随机因素做 active-learning sampling、thermal-fluid-structure performance 代理和 LCF probabilistic-life 评估。 | “固定 CFD 预算的追加样本/主动查询”并非空白；Pak-B 既无前者的 CFD/PSP 闭环，也无后者的热—流—结构/寿命真值。 |

**判定理由。** Chen I 的 “decomposition + error-source tracking + row-to-row vortical interaction” 与 Yao 的 “vortex-encoded AI + dense-layout superposition correction” 共同击中了 Q-IO 原方案必须依赖的领域特异物理核心。把剩余文字收窄为“经校准的真实误差排序、拒答与固定预算查询分配”只会留下一个通用 reliability/active-learning 外壳，正是已关闭路线 R7 所禁止的重命名。

### 4.3 为什么“尚未检出完全相同四件套”不能重开它

本轮未从可访问网页定位到一篇同时具备“Pak-B 孔数外推 + 真实场误差排序 + selective abstention + 固定 CFD 预算 query allocation”的论文。这个未命中**不**证明该组合新颖，原因有四：

1. 新颖性要求正向证明一个不可替代的、领域特异的机制，而不是靠检索空白拼接四个已知模块；Q-IO 当前没有这样的机制；
2. calibrated risk/coverage、ensemble/MC-dropout、split conformal、OOD score 和主动查询分配均是通用 surrogate-reliability 工具；而 Zhang et al. 2023 已在气膜中使用 sequentially adaptive sampling，Qiu et al. 2024 已在高温叶片多物理/寿命任务中使用 active-learning sampling，不能因换成 Pak-B 就自动成为贡献；
3. Pak-B 当前没有经核验的 binary manifest、case ID、0-hole reference、nested subset mapping 或可留出的独立高孔数 calibration/test 合同，故连“分数是否排序真实未来误差”都不能诚实实验；
4. 即便上述可靠性实验成立，输出仍是端壁表面 `Temperature` 场的单学科代理风险，而不是 GE-E3/Pak-B 的耦合设计决策或叶片 MDO。

若未来有不同的数据合同和一个**先于实验定义、可被反驳且不能由 Chen/Yao/SDNO/通用 reliability baseline 替代的机制**，它必须作为全新的问题从 G0 与 G2 重审；不得把它再命名为 Q-IO 来绕过本次关闭。

### 4.4 原 kill criteria 的审计结果

| 原条件 | 2026-09-01 结果 | 处置 |
|---|---|---|
| 1. SDNO 或后续工作已经在相同 Pak-B protocol 上做同等 failure/OOD ranking、拒答或 query allocation | **未裁定。** SDNO 正文不可访问；不能从摘要推断其没有这些实验。 | 不是关闭的依据，也不能作为 Q-IO 的正面证据。 |
| 2. 同一离散孔布局/流体热场中已有 interaction-aware 方法验证相同机制 | **实质触发。** Chen I/II 与 Yao 均是多排/密集孔气膜、nonlinear interaction、error/correction 的直接领域前例。它们并非 Pak-B 的逐样本复刻，但已覆盖原方案赖以声称物理新意的机制。 | 关闭其物理 interaction 主张。 |
| 3. Pak-B 无法合法取得，或 schema/split 不能审计 | **尚未裁定永久不可得；当前未通过验证。** 本地无二进制且 TLS 传输失败。 | 已足以阻断实验立项；不将技术下载失败写成数据永久不存在。 |
| 4. 没有 nested subset mapping，却需要把分数解释为已识别物理高阶 interaction | **未满足前提。** 公开接口未展示 mapping，且尚未有原始 MAT 可核验。 | 物理解读不得使用；退化成纯 risk score 又落入 R7。 |
| 5–6. 分数胜过强基线，并在独立真值上降低热点风险 | **没有实验，未检验。** | 不允许用假设结果维持候选状态。 |
| 7. 能改变可复查的追加仿真/设计接受决策 | **没有已验证的决策实验。** | 不允许从问题动机跳到工程价值。 |

### 4.5 G0–G6 终态快照

| Gate | 终态 | 依据 |
|---|---|---|
| G0 主张完整性 | 问题可以表述，但不是可区分贡献。 | 残余机制只是通用 reliability pipeline。 |
| G1 工程后果 | 未证实。 | 无追加 CFD、无优化闭环、无 MDO 输出。 |
| G2 敌对新颖性 | **关闭。** | 2025 气膜 interaction decomposition、vortex-encoded AI、nonlinear correction 形成实质直接覆盖。 |
| G3 理论/计算 | 仅有不可识别性边界，非投稿级新定理。 | 缺少可证伪的专属假设与数据支撑。 |
| G4 验证 | **未开始且当前不可启动。** | 无本地二进制/manifest、无 nested layout / 独立真值合同。 |
| G5 公平与复现 | **未开始。** | 不能冻结 split、seed、基线或数据许可。 |
| G6 投稿资格 | 不适用。 | 没有可以投稿的研究结果。 |

---

## 5. 真实叶片 MDO 的重开条件（不是当前项目计划）

如果未来允许引入新的公开数据或计算资源，最小的研究对象不应只是“又训练一个大网络”，而应先获得一个可审计的共同设计和真值体制：

| 层 | 最低材料 | 当前 GE-E3/Pak-B 是否提供 |
|---|---|---|
| 共享输入 | 一个可制造 \(x\)：外形/端壁/冷却布局/厚度或内部通道 + 工况与容差。 | 否；GE-E3 与 Pak-B 分离。 |
| 气动 | 与 \(x\) 对应的流量、损失、压力/热边界。 | 部分，仅 GE-E3 气动/流场。 |
| 热 | 同一 \(x\) 的冷却流量/压损、气膜、固体金属温度或 CHT 热通量。 | 否；Pak-B 仅端壁表面 `Temperature`。 |
| 结构 | 同一 \(x\) 的材料、约束、应力/位移或可验证 FEA。 | 否。 |
| 寿命 | creep/TMF/HCF 或明确寿命模型、参数与失效判据。 | 否。 |
| 真值验证 | 未参与训练的 coupled cases、solver verification、实验或独立高保真层。 | 否。 |

即使补齐这些数据，GT2025 已使“3-D Transformer/point-cloud 预测偏差下 lifing”不新。未来真正的机制必须先逐项区别于它：**问题定义、可观察真值、理论对象、设计决策、验证梯和失败条件**，而不只是网络名称或更大的训练集。

详见 [REENTRY_REQUIREMENTS.md](REENTRY_REQUIREMENTS.md)。

---

## 6. 当前决定

- 不启动模型训练、CFD/CHT/FEA、优化或论文写作；
- 不把 GE-E3/Pak-B 的独立结果包装为 MDO；
- 不以“更高精度”“更快”或“AI+多学科”取代新颖的、可证伪的中心命题；
- Q-IO 的敌对 G2 审计已完成并触发关闭；下一步若继续，只能完成公开数据版本 manifest 作为可复现性基础，或由研究负责人明确允许扩展资源后从全新问题定义重新开始。
- FAN-02 保留为真实 FSAI 实验体系的 future-release/reference lead；在公开 release 提供可审计的 paired measurements、run map 与独立验证协议前，不启动其模型、优化或论文路线。

这是一项严格的停止决定，而不是对团队能力或问题重要性的否定。
