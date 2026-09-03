# 适合 `sunccchengze` 的优质 GitHub 仓库推荐

> 这份清单排除了刚才 Trending 前十，按用户近期的风电科研、CFD、数字孪生、学习系统、PPT/文档处理、Agent Skills 和质量门禁来筛选。推荐不等于授权复制；取用前必须核对当前 LICENSE/NOTICE 和依赖。

## 1. 风电、CFD 和科研计算

### [NatLabRockies/floris](https://github.com/NatLabRockies/floris) — ★★★★★

controls-oriented 风电场尾流建模和风场控制软件。用户的 `wind_farm_viz` 已经使用 FLORIS，推荐把它作为固定版本的物理上游，而不是复制源码。适合生成风向/风速/偏航/尾流/功率回归数据，并为 `0824-2026` 的演示数据提供依据。当前主仓库声明 BSD-3-Clause；用户项目中应继续固定版本，例如 4.6.6。

### [OpenFAST/openfast](https://github.com/OpenFAST/openfast) — ★★★★★

整机风机与 FAST.Farm 风场的气动、结构、控制、电气和水动力耦合仿真。适合给代理模型和数字孪生增加高保真验证层，生成少量可信样本；不适合直接塞进网页。Apache-2.0。

### [su2code/SU2](https://github.com/su2code/SU2) — ★★★★☆

开源 CFD 和气动外形优化套件。适合对 `turbine-blade-ai-platform` 产生的 Pareto 候选做 RANS/高保真抽查，形成“代理模型快速筛选 → CFD 复核”的闭环。主仓库 `LICENSE/COPYING` 为 LGPL-2.1 体系，组件级再分发仍需核对。

### [anyoptimization/pymoo](https://github.com/anyoptimization/pymoo) — ★★★★★

NSGA-II、NSGA-III、MOEA/D、遗传算法、粒子群和多目标结果可视化。用户项目已在使用，它不是新发现，但值得作为正式上游固定版本、随机种子、约束配置和引用。Apache-2.0。

### [astral-sh/uv](https://github.com/astral-sh/uv) — ★★★★★

统一管理 Python 版本、虚拟环境、依赖、workspace 和 lockfile。适合逐步整理 `turbine-blade-ai-platform`、`wind_farm_viz`、`0824-2026` 和资料处理脚本，减少环境不可复现。Apache-2.0。

## 2. PDF、教材、PPT 和科研表达

### [docling-project/docling](https://github.com/docling-project/docling) — ★★★★★

支持 PDF、DOCX、PPTX、XLSX、HTML、图片和音频等格式，能保留版面、阅读顺序、表格、公式和图片信息，支持本地运行、MCP 和 API 服务。适合 `tushupdf`、`sucheng` 和 `zixue2026` 的资料入库。MIT。

建议管线：

```text
原始 PDF/PPT → Docling 结构化解析 → Markdown + JSON + 页码/截图 → 人工核验 → 知识库
```

### [opendatalab/MinerU](https://github.com/opendatalab/MinerU) — ★★★★★

对中文教材、论文、扫描 PDF 和复杂版式材料很值得测试，适合教材 OCR、PPT/PDF 逐页审计和资料索引。当前 `LICENSE.md` 声明 Apache-2.0 加附加条款；基于它提供在线服务时要注意署名和商业阈值条款。建议和 Docling 做小样本对比，不要一开始同时部署两个生产管线。

### [quarto-dev/quarto-cli](https://github.com/quarto-dev/quarto-cli) — ★★★★★

基于 Markdown 和 Pandoc 的科研/技术出版系统，可嵌入 Python、R、Julia、Jupyter 和 JavaScript，生成报告、网页、书籍、图表和可复现输出。适合 `zixue2026` 学习报告、风电实验报告和技术文档。README 声明 MIT。

### [slidevjs/slidev](https://github.com/slidevjs/slidev) — ★★★★☆

Markdown 驱动的交互式演示文稿，支持代码、公式、Mermaid、动画、录屏和导出 PDF/PNG/PPTX。适合 `sucheng` 的结构迭代和科研汇报初稿；最终商业/竞赛交付仍建议保留 PowerPoint 精修环节。MIT。

### [marimo-team/marimo](https://github.com/marimo-team/marimo) — ★★★★☆

反应式 Python Notebook，文件是纯 Python，可运行成脚本、交互式 App 或 Web 页面，强调无隐藏状态和 Git 友好。适合把风场数据实验和 `wind_farm_viz` 的 Streamlit 留档工具改造成更可复现的实验应用。Apache-2.0。

## 3. Agent Skills、记忆和质量门禁

### [anthropics/skills](https://github.com/anthropics/skills) — ★★★★★

官方 Skills 示例、规范、模板，以及文档、PDF、PPTX、XLSX 等复杂技能的参考实现。适合完善 `-SKILL-` 的元数据、渐进式加载、技能包和插件组织方式。

注意：仓库内许可证并不统一；README 特别说明部分文档技能是 source-available 而非传统意义上的开源。适合参考，不能不加审查地整体复制或再分发。

### [sickn33/agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills) — ★★★★★

旧的搜索结果可能称其为 `antigravity-awesome-skills`，当前 canonical 仓库是这个地址。它提供本地技能目录、Agent 自主选择、技能栈组合、manifest、选择证据、可复现计划和 MCP 查询，和你的 `-SKILL-` 架构高度相似。建议拿来比较路由、证据和 stack 设计，不要把两千多个技能全部再复制一次。MIT。

### [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) — ★★★★☆

MCP 官方参考服务器，包括 Fetch、Filesystem、Git、Memory、Time 和 Sequential Thinking。适合研究如何让技能库连接真实工具和资料，但官方明确提醒它们主要是参考实现，不是生产即用组件。部署前必须自行加路径、权限、网络和凭据边界。

### [getzep/graphiti](https://github.com/getzep/graphiti) — ★★★★★

面向 Agent 的时间知识图谱，记录事实何时成立、何时被替换、实体关系和原始 episode 来源。适合把你的 `MEMORY_SYSTEM`、`HANDOFF`、学习进度和 PPT 事实账本升级成可查询的时间上下文。Apache-2.0。

### [mem0ai/mem0](https://github.com/mem0ai/mem0) — ★★★★☆

通用 AI Agent 记忆层，接口比 Graphiti 更直接，适合先做用户/会话/Agent 记忆原型。如果重点是“关系和事实的时间变化及来源”，Graphiti 更匹配；如果重点是快速接入个性化记忆，可以先比较 Mem0。Apache-2.0。

### [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) — ★★★★★

测试 Prompt、Agent、RAG 和多模型输出，支持红队测试、漏洞扫描、结果对比和 CI/CD。建议给 `-SKILL-` 的技能路由、`zixue2026` 的学习 Agent、PPT 审计和 LoveMaster 的安全边界各建立 10～30 个固定回归案例。MIT。

## 4. 3D、工作流和演示动效

### [CesiumGS/cesium](https://github.com/CesiumGS/cesium) — ★★★★☆

WebGL 地理空间 3D 引擎，适合把风场、地形、卫星/气象图层和时序数据放到可复用的地球场景中。它比单纯的 Three.js 场景更偏地理空间基础设施，可作为 `0824-2026` 的重型可选路线。仓库通常以 Apache-2.0 发布；接入前仍核对当前 LICENSE、第三方资产和构建体积。

### [xyflow/xyflow](https://github.com/xyflow/xyflow) — ★★★★★

React Flow/Svelte Flow 节点式 UI。适合做 Agent 技能路由图、多 Agent 工作流、风电数据流、数据契约和研究技术路线图。可以把 `-SKILL-` 的文字路由变成可交互编排器，也可以把 `0824-2026` 的控制闭环画出来。MIT。

### [theatre-js/theatre](https://github.com/theatre-js/theatre) — ★★★★☆

Three.js/R3F 的 Web 动效和时间轴编辑器，适合 `0824-2026` 的日夜切换、风况雷达、尾流、镜头导览和答辩演示。当前仓库最近推送时间相对较旧，使用前应验证与现有 Three.js/R3F 版本的兼容性，不建议一开始变成核心依赖。Apache-2.0。

## 5. Agent 运行时和可观测性候选

### [VoltAgent/voltagent](https://github.com/VoltAgent/voltagent) — ★★★★☆

TypeScript 优先的 Agent/多 Agent 应用框架，适合对比 `-SKILL-` 的路由、工具调用、工作流、记忆和可观测性实现。它更像应用运行时而不是技能规范，建议先阅读架构和安全边界，用一个小型科研助手做隔离 PoC；许可证以仓库当前 LICENSE 为准，不从 star 或 API 元数据推定。

### [langfuse/langfuse](https://github.com/langfuse/langfuse) — ★★★☆☆

LLM/Agent 的 tracing、prompt 管理、评测和成本/延迟观测平台。可给 `-SKILL-`、学习 Agent 和 PPT 审计建立运行证据，但会引入服务端、数据库和潜在敏感输入留存，不能直接发送教材、个人关系或未脱敏科研数据。GitHub API 当时返回 `NOASSERTION`，许可证必须阅读仓库当前文件后再决定。

## 6. 推荐的实际取用顺序

### 如果只选五个新仓库

1. [OpenFAST](https://github.com/OpenFAST/openfast)：给风电数字孪生补高保真物理验证。
2. [Docling](https://github.com/docling-project/docling)：统一 PDF/PPT/教材资料入库。
3. [promptfoo](https://github.com/promptfoo/promptfoo)：给 Agent 技能建立自动回归和安全评测。
4. [Graphiti](https://github.com/getzep/graphiti)：补强长期、带时间和来源的记忆。
5. [xyflow](https://github.com/xyflow/xyflow)：把技能路由和科研数据流可视化。

`uv` 可以立即作为所有 Python 项目的基础工具；`FLORIS`、`pymoo`、`SU2` 是你已有技术栈的上游，不必重复搬家。

### 对应到你的仓库

- `0824-2026`：FLORIS + OpenFAST + xyflow；需要镜头编排时再试 Theatre。
- `turbine-blade-ai-platform`：SU2 + OpenFAST + pymoo + uv。
- `zixue2026` / `tushupdf`：Docling 或 MinerU + Quarto + marimo。
- `sucheng`：Docling/MinerU + Slidev + promptfoo 的术语/事实回归。
- `-SKILL-`：Anthropic Skills + agentic-awesome-skills + MCP reference + promptfoo。
- 长期记忆：先用小数据集比较 Mem0 和 Graphiti，不要立即替换已有 Markdown 账本。

## 7. 通用取用规范

每个上游至少登记：

```text
来源仓库
固定 tag/commit
许可证和 NOTICE
实际取用的目录/包
目标项目
依赖和网络需求
凭据需求
写入路径和副作用
验证命令
本地改动
```

大型技能库采用 sparse checkout、submodule 或只复制选中的技能目录；科学计算库采用固定版本和回归样本；带模型/文档数据的仓库保留来源和版权边界。
