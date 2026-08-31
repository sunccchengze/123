# 风电场偏航优化「交互结构」研究包 · 当前状态

**会话：Arena 01a053b1-123｜更新：2026-08-31｜技术状态：WES/Copernicus 源文件预检、图文就近布局复核和本地双遍回归已完成；投稿状态：**`不可直接投稿`**。**

本项目包含三份相互关联的单作者研究草稿。P1/P2 仍作为 Wind Energy Science（WES）候选稿继续独立审查；P3 已在第四轮新颖性与证据审计后降级为静态数值 benchmark 记录，不应作为独立 WES 研究论文投稿。数值结论来自 FLORIS 4.6.6 的稳态尾流模型实验；它们不是风洞、LES 或现场实测结论。新颖性检索档案、实验缓存、作图脚本和稿件源文件均保存在本目录树中。

> **作者信息核验提醒**：三篇源文件当前作者字段为 `Chengze Sun`，通讯邮箱为 `2253710052@stu.xjtu.edu.cn`。投稿前应由作者本人核对该英文姓名是否与其拟投稿的法定/惯用署名完全一致；本代理不应替作者猜测或改写作者身份。

## 研究主张（均须由作者逐项核验后负责）

| # | 主张 | 当前可复算的数值证据 | 残余边界 |
|---|---|---|---|
| 1 | **互补/替代相结构（C--S 分解）** | 三机链的 $M_{12}$ 从原点的 $+0.674$ kW deg$^{-2}$ 变至 $(20^\circ,20^\circ,20^\circ)$ 的 $-0.215$ kW deg$^{-2}$；cc 与 empirical-Gauss 套件中也有相应翻转。 | 这是 FLORIS 模型类中的结构分析；尚未由新实验验证。 |
| 2 | **最优点解耦与交互能证书** | 统一 $h=5^\circ$ 重算中，最优点的非对角/对角 Hessian 比为 0.008--0.069，基线/一般点为 0.22--0.87；12 个随机布局的 Boolean-greedy gap 均值 0.1029\%、最大 0.4772\%，均不超过其采样交互能证书。 | “Law 1”是经验规律及部分机制解释，并非一般模型的完全定理。 |
| 3 | **P3：静态射线反演 benchmark（非独立投稿主张）** | 在同一九个**内部**目标（观测端点增益的 5--99%，8192--10022 kW）上，Brent 括根法需 7--11 次 root-solver 评估、最大模型残差 $7.8209\times10^{-4}$ kW；五节点 proxy 切片为 51.8937 kW（端点功率的 0.5168\%）。41/401 节点 trace 均未见 3×3 射线的相邻下降。 | 直接 APC/yaw tracking 先例已存在；有限节点不是单调性证明、唯一逆映射证书或动态控制验证。P3 当前不可作为独立 WES 研究稿提交。 |

## 已完成的可验证技术整改

### WES/Copernicus 源文件

三篇 `.tex` 均已完成以下静态整改：

- 使用 `\documentclass[wes, manuscript]{copernicus}`；标题、作者、affiliation、通讯信息、日期字段和 `\firstpage` 均移入 `\begin{document}` 后、`\maketitle` 前，符合 Copernicus 示例顺序。
- 删除稿件源中的额外 `\usepackage`、自定义 `\newcommand`、自定义 `proof` environment、`\newtheorem` 和禁止的 `\paragraph`。符号已内联为标准 LaTeX；表格规则已由 `booktabs` 命令替换为 `\hline`。
- P1 的定理、推论和 Law 标签保留为普通编号加粗陈述，不再依赖作者定义的环境。
- 图环境和 captions 已移至各自首次讨论段之后，不再集中在 conclusions 后：P1 保留 10 张交互结构/稳健性图，P2 保留 4 张算法图，P3 保留 4 张静态射线数值 benchmark 图。P1 中重复的 DJS 和 quasi-concavity 图只保留在其所属的 P2/P3 稿件，避免跨稿重复图件。标准 `[htbp]` float placement 及 P2/P3 的 `\clearpage` 在本地回退 PDF 中使图件不会被后续 discussion、conclusions 或 bibliography 越过。
- P3 新增了共同 benchmark 的 Table 1，使九目标 exact-inversion 表在实际 LaTeX 输出中编号为 Table 2；其 proxy 对比明确限于该同一组九个 target。
- 三篇文末顺序均为：code/data availability → appendix → `\noappendix` → author contribution → competing interests → acknowledgements → bibliography，且 bibliographystyle 位于 bibliography 前。
- `research/tools/latex_wasm/copernicus_local.sty` 仅为本地 article 回退验证补齐了真实类已提供的 `amsmath`、`natbib`、`graphicx` 与 `\noappendix` 接口；它**不是**投稿模板，也不应提交给 WES。

### 图件与数值可追溯性

- 19 张结果 PNG 已由脚本以 **300 dpi** 重生成，并逐图读取 PNG 元数据复核；全部约 300 dpi、每张远低于 5 MB，合计约 2.5 MB。其中 18 张当前被三篇稿件引用；未引用的 `fig12_quasiconcavity.png` 保留为历史生成物而不作为 P1 的重复投稿图。
- Fig. 1 相图限定显示在 $0$--$20^\circ$，不再把被声明为 warning-zone 的 $\geq25^\circ$ 角点画入结果；其原始矩阵已保存为 `expcache/fig1_phasemap.json`。
- Fig. 2 的 $300^\circ$ Hessian 现有带 FLORIS 版本和工况的缓存 `expcache/fig2_hessian_wd300.json`；图中明确省略对角线，以显示混合偏导。
- Fig. 3--6 不再使用陈旧硬编码数。Fig. 6 直接从固定 seed 的 12 布局证书缓存绘制观测 gap 和 “gap / bound”，最大归一化比 0.930。
- Fig. C1/C3/C4 现由 cache-backed 链生成。`exp_inverse.py` 写入有限网格 evidence 的 `expcache/ray_monotonicity.json`，并把同一九个内部 target 的 exact/proxy 记录写入 `expcache/table2_tracking.json` 与 `expcache/proxy_tracking_benchmark.json`；`make_figures2.py` 在绘制 C4 前断言目标数组完全一致。Fig. C4 不再含旧的 $4.18\times10^{-4}$ kW 标签或不可比的 8 目标 proxy 数字。

### 本地回归（不等同官方编译）

使用 `tools/latex_wasm/compile.mjs` 的 article+shim 回退链，双遍编译结果为：

| 稿件 | LaTex error | 未定义引用/文献 | Overfull hbox |
|---|---:|---:|---:|
| `paper1_interaction_structure.tex` | 0 | 0 / 0 | 54 |
| `paper2_djs_clustering.tex` | 0 | 0 / 0 | 6 |
| `paper3_power_tracking_inverse.tex` | 0 | 0 / 0 | 6 |

P1 的 overfull 数量提示真实模板排版仍需人工检查；局部回退 PDF 不能用来宣称 WES v7.15 通过。

## 可复现环境

从一个干净 checkout 重建已验证环境：

```bash
cd research
python3 -m venv .venv
.venv/bin/python -m pip install -r ws_submodularity/requirements.txt
cd ws_submodularity
../.venv/bin/python exp_inverse.py       # finite-grid ray screens + Table 2 + matched-target proxy cache
../.venv/bin/python make_figures.py      # P1 Fig. 1--6
../.venv/bin/python make_figures2.py     # P1 Fig. 7--10、P2/P3 图；另保留 fig12 历史生成物
```

`requirements.txt` 固定了 Python 3.11 下本轮验证的 `floris==4.6.6`、NumPy、SciPy、Matplotlib 和 Pillow 版本。全量其他实验脚本仍应在作者审阅其工况、随机种子和缓存后再运行。

## 新颖性与科学边界

- `NOVELTY_DOSSIER.md` 记录检索式和相邻工作。P3 的第四轮审计已经发现 Starke 2023、Oudich 2023、Sterle 2024 和 Tamaro 2025/2026 等直接 APC/yaw-tracking 先例，因此 P3 的“first/field avoided/certificate”旧叙事已明确作废。
- `SELF_AUDIT.md` 记录过去已发现并纠正的数值、口径与证据等级问题。当前公平比较是同一九个内部目标上的 51.8937 kW proxy residual 与 $7.8209\times10^{-4}$ kW Brent residual；它不是 matched online budget 比较。
- 任何“唯一分解”“定理”“保证”“首次”等措辞，都必须由作者在逐行推导、原始运行日志、引用准确性和新颖性检索后独立承担责任。当前文稿不应把仿真输出表述为实验事实或有限采样表述为数学证明。

## WES 投稿阻塞项（必须逐项关闭）

0. **P3 的科学投稿闸门。** P3 当前是静态、单工况 FLORIS benchmark，不是独立 WES 研究稿。只有在给出可审计的连续单调性/唯一性证明或 validated-numerics 结果、完成跨工况/模型/不确定性测试，并同动态 APC 基线进行同口径比较后，才可重新评估其投稿资格。
1. **生成式 AI 政策阻塞。** Copernicus 的现行 AI policy（<https://publications.copernicus.org/for_authors/ai_policy.html>，本轮核查于 2026-08-31）允许未声明的 grammar/spelling/punctuation/readability 协助，但明确规定生成式 AI 不得用于论文文本或科学解释。本项目稿件在本次工作流中获得了实质性生成式 AI 协助，因此**不得原样向 WES 投稿，也不能用虚假“仅语法检查”声明规避政策**。在考虑 WES 前，作者必须独立重写所有文本、逐项重新推导/核验解释与数据，并自行确认其最终稿的合规性；否则应选择允许透明、声明式生成辅助的期刊。
2. **真实官方包编译。** 官方 manuscript preparation 页面（<https://publications.copernicus.org/for_authors/manuscript_preparation.html>）所列 LaTeX package v7.15（2026-08-25）仍须在有真实 `copernicus.cls` 和完整 TeX Live 的环境中编译。当前环境只做了静态接口比对及 shim 回归，不能替代该步骤。
3. **永久存档和 DOI。** GitHub 工作分支不是可引用的长期研究存档。投稿前应整理可公开的代码、必要输入/缓存、运行说明和许可证，创建 release，并通过 Zenodo 或等效仓库生成不可变 DOI；availability statement 应改为实际的 archive URL/DOI，而不是预测性的仓库地址。
4. **作者与科学责任。** 作者应亲自确认署名、机构、邮箱、利益冲突、贡献声明、所有引文和每个数值；并决定三篇是否存在过度重叠、是否应合并或明确交叉引用。未经实际风洞/LES/现场验证，不应把预测性内容宣传为可投“顶刊”的经验定律。

## 主要文件

| 路径 | 用途 |
|---|---|
| `papers/paper1_interaction_structure.tex` | 主稿：交互分解、相图、解耦、贪心证书与实验预注册草案。 |
| `papers/paper2_djs_clustering.tex` | 算法稿：DJS、符号矩阵聚类和证书基准。 |
| `papers/paper3_power_tracking_inverse.tex` | 已降级的静态射线数值 benchmark：有限网格 screen、Brent 反演和 matched-target proxy 比较；不可独立投稿。 |
| `papers/refs.bib` | 三篇共享文献库。 |
| `ws_submodularity/requirements.txt` | 本轮验证的固定 Python 依赖。 |
| `ws_submodularity/expcache/` | 已绘图/已报告结果的版本化 JSON 缓存。 |
| `NOVELTY_DOSSIER.md`、`SELF_AUDIT.md` | 新颖性范围、相邻工作和问题纠正记录。 |
