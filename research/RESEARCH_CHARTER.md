# RESEARCH_CHARTER — 孙承泽科研突破任务

依据 `research-workflow-orchestrator` / `research-question-protocol` / `academic-integrity-ai-disclosure` 技能建立。

## 任务定义

- **总目标**：找到一个"全网零提及、文献零覆盖"的创新研究点，并将其挖深挖透，产出可投顶刊的数篇研究论文。
- **绝对第一标准（用户红线）**：创新点必须是全网搜不到的。凡检索到任何相关结果 → 该点作废，或在该点上继续深挖到无先例的子层面。
- **负责人**：孙承泽（研究负责人，最终判断权）。本仓库分支 `arena/01a053b1-123`。
- **工作目录**：`/home/user/123/research/`。

## 硬约束

1. **新颖性审计纪律**：每个候选点必须通过多通道检索审计并留档（`NOVELTY_DOSSIER.md`）：
   - 网页多语种检索（web_search 工具，中英文多组同义表达）；
   - arXiv API（标题/摘要/全文字段精确短语）；
   - OpenAlex / Crossref（含 fulltext.search）；
   - OEIS（若涉及整数序列/常数）；
   - GitHub 代码检索（gh api search）；
   - 专利/其他（视情况）。
2. **审计失败即作废**：只要一个通道命中实质相关结果，就记录在案并作废或降级该点；"没搜到"必须附检索边界和日期，表述为"在检索范围内未发现先例"，不夸大为"宇宙中不存在"。
3. **反 AI 味写作**：论文写作调用 `humanizer-zh`（中文）+ `claude-scholar/nature-*`（英文顶刊规范）与 `doc-coauthoring`；禁用夸大修辞、禁用编造引用。
4. **证据先于叙事**：任何数值/定理/实验必须有可复现脚本，存 `research/` 下；负结果保留。
5. **时刻反省**：每完成一个里程碑，更新 `SELF_AUDIT.md`：重新搜索、重新怀疑"真的没人做过吗"。

## 能力盘点（今晚可用）

- **计算**：Python 3.11 + numpy/scipy/sympy/mpmath/pandas/matplotlib（venv 已建）。
- **学术检索通道**：arXiv API、OpenAlex、Crossref（经 fetch_page）；OEIS JSON（经 fetch_page）。
- **Web 检索**：web_search（中/英）、fetch_page（任意网页）。
- **代码生态**：GitHub API（gh，全权限）。
- **不可用**：LLM API（无 key）；bash 直连外部 HTTP（除 PyPI/GitHub 白名单）。

## 研究问题构造（FINER 检查表）

每个候选点必须写明：可检验命题、可证伪条件、学科归属、潜在期刊、审计计划。
