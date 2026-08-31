# 03 · Novelty Audit Protocol（六通道）

## 通道
1. web_search 中/英（多组同义表述，含负面表述）
2. arXiv API：`all:"phrase1" AND all:"phrase2"`（全文匹配）
3. OpenAlex：`filter=fulltext.search:"..."`（全文）+ search=
4. Crossref（DOI 核实）
5. OEIS（整数序列/常数查重）
6. GitHub code search（gh api）

## 规则
- 所有检索记录：查询式、通道、日期、命中数、命中物的"相邻先例"判定。
- 实质命中 → 作废或深挖；相邻先例 → 必须引用 + 写清区别。
- 表述纪律："在检索范围内（日期+查询集）未见先例"，禁止"宇宙中不存在"。
- 数值声明双检查：差分步长收敛 + 模拟器边界（负速度/极端工况）排除。

## 2026-08-30 实录（节选，全文见 NOVELTY_DOSSIER.md）
- submodular+wind farm（arXiv 0 命中；OpenAlex 仅 2 篇排布文献）→ H1 方向本身空白，但被符号证伪。
- supermodular+wind（arXiv 0）→ H2 方向空白。
- 交互矩阵/Hessian/解耦/贪心保证 + yaw（Web/OpenAlex）→ 全部零结构分析先例。
- 相邻：Zhang 2011（排布次模）、Starke 2024（二元连接矩阵）、WGWD 2020（几何权重图解耦）、APC 2025（查表跟踪）、Bestehorn 2025（NP-hard 黑盒）。
