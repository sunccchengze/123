# Evidence Ledger

> 对应报告快照：2026-08-30 04:21 UTC。

| ID | 来源 | 核验内容 | 证据强度 | 限制 |
|---|---|---|---|---|
| E1 | [公开 profile](https://api.github.com/users/sunccchengze) | 账号名、创建时间、公开仓库数量、公开 profile 字段 | 高（直接 API） | 只代表公开 profile；无法覆盖私有资料。 |
| E2 | [公开仓库列表](https://api.github.com/users/sunccchengze/repos?per_page=100&sort=pushed&direction=desc) | 33 个公开仓库、默认分支、仓库 `pushed_at`、描述和语言 | 高（直接 API） | `pushed_at` 不是分支级提交事实，因此不能单独作为活动判据。 |
| E3 | 目标仓库各自的 `/branches`、`/commits/{sha}` API | 所有可见分支的 head 时间、最新分支、commit 消息和 URL | 高（直接 API） | 只覆盖公开且 API 可见的分支；提交元数据不能证明实际逐行贡献。 |
| E4 | [GitHub Trending](https://github.com/trending) | 默认 Today / Any language 前十、项目描述、当日 star 展示 | 高（页面快照） | 排名和 star 是动态值；页面默认是当前抓取时刻。 |
| E5 | [sunccchengze/-SKILL-](https://github.com/sunccchengze/-SKILL-/tree/arena/01a048e7-skill) 分支 `8d749b9a` | `SKILL.md`、`TASK_ROUTING.md`、`AGENTS.md`、科研路由和来源路由规则 | 高（用户指定公开来源） | 这是用户技能库的一个固定分支快照，未来可能变化。 |
| E6 | 候选仓库当前 README、metadata、LICENSE/NOTICE | FLORIS/OpenFAST/SU2/pymoo、Docling/MinerU、Quarto/Slidev/marimo、Graphiti/Mem0、promptfoo、xyflow、Skills/MCP 等用途和许可 | 中高（上游自述+文件） | README 是项目方自述；商业/再分发仍需逐项法律核验。 |
| E7 | 用户之前的明确请求 | 不分析当前工作区仓库内容；关注账号近期分支提交；持续寻找相关仓库 | 高（直接用户指令） | “持续”受当前 Agent 不能后台自主联网的运行方式限制。 |
