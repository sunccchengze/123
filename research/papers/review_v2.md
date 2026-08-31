# Pre-Submission Review — C1 论文包 v2（2026-08-31）

审核依据：HKUSTDial/Supervisor-Skills `pre-submission-reviewer`（五维度 + 禁词扫描 + 完整性门禁）。
审核对象：P1（旗舰，主审）、P2/P3/P4（联动核查）。Paradigm：STEM/工程+动力系统。

## Summary
- CRITICAL: 0
- MAJOR: 2（1 项已在本轮修复，1 项需作者决策）
- MINOR: 5
- Top three fixes first:
  1. **[MAJOR→已修]** 图案选择的归因缺少消融（无阈值对照）。已补：线性耦合消融实验（Exp.7a）——去掉全或无阈值后所有风机恒转、功率平滑单调 0.865→1.124 MW、无台阶，归因孤立。已写入 P1 §3/§4.2/§5.2 + fig8。
  2. **[MAJOR→待决策]** 目标期刊匹配：纯模型/延迟系统论文（无 CFD/LES/田间）投 JFM 首轮风险高。建议 v1 投 *Wind Energy Science*（开放获取，刊登解析尾流模型研究，见审计日志 WES 2025 命中例）或 *Chaos*/*Phys. Rev. E*（动力系统框架）；JFM 留待 F1–F4 获 LES/田间验证后升级。
  3. **[MINOR]** 摘要 190 词偏长（JFM 习惯 ~150 词内）；投稿前按目标刊压缩。

## Dimension 1: Macro logic
| # | Finding | Severity | Suggested fix |
|---|---|---|---|
| 1 | "discrete on/off pattern selection" 的主结果归因此前仅有机理叙述（threshold relay），无消融隔离核心机制 | MAJOR | **已修**：线性耦合对照（Exp.7a, fig8）证明台阶与离散图案均由全或无阈值产生 |
| 2 | 摘要 "excitable medium ... a refractory recovery"：文中展示的是 refractory *tail*（慢 CT 恢复 + 间隔下界），非经典"再激发被阻断"的不应期 | MINOR | 保留（讨论 §5.1 已区分），投稿时在 abstract 改为 "refractory recovery (slow wake re-establishment)" |
| 3 | "to the best of our knowledge" 新颖性措辞合规；32 项审计日志随文 | — | 维持 |
| 4 | 贡献清单 6 条 ↔ Exp.1–7 一一对应，F1/F2/F4 文内自验证 | — | 维持（结构合格） |

## Dimension 2: Writing details
| # | Finding | Severity | Suggested fix |
|---|---|---|---|
| 1 | 各节段落均有主题句；"verification path" 专节（§5.4）承载 知行合一 叙事（三条撤回声明的捕获路径） | — | 维持 |
| 2 | 摘要问题/方法/结果三要素齐全 | — | 维持 |
| 3 | P2 表格"comparison / T / gain / status"清晰呈现幻象来源的逐步演示 | — | 维持 |

## Dimension 3: English grammar
| # | Finding | Severity | Suggested fix |
|---|---|---|---|
| 1 | P1 intro: "wake-mixing controls impose periodic actuation" — controls 作名词不自然 | MINOR | **已修**：改为 "wake-mixing control strategies impose" |
| 2 | 冠词/主谓一致/时态：全文抽查通过（方法现在时、结果过去/现在时一致） | — | 维持 |

## Dimension 4: LaTeX format
| # | Finding | Severity | Suggested fix |
|---|---|---|---|
| 1 | 引用用普通空格 + \cite（约 20 处），规范要求 `~\cite` 非断空格 | MINOR | **已修**：批量替换 |
| 2 | 方程编号连续（1,2）且均被引用；图 8 张全部有 caption（首句即发现）；标签全下划线；图全部矢量 PDF（P3 加热链图已转矢量） | — | 维持 |
| 3 | `\date{Draft...}` 行投稿前删除 | MINOR | 投稿前处理 |

## Dimension 5: Figure quality
| # | Finding | Severity | Suggested fix |
|---|---|---|---|
| 1 | 全部 8 图矢量 PDF；字体缩放后达标；配色色盲安全（蓝/灰/红点+双编码）；caption 自含 | — | 维持 |
| 2 | fig7（τ_r×k 热图）版式偏空 | MINOR | 可改紧凑表格；当前可用，投稿前再优化 |
| 3 | fig1 右联图（幅值无关性）含点+柱双编码 | — | 维持 |

## Banned-vocabulary and em-dash scan
[attestation] 对 4 篇 .tex 全文扫描（非抽样）：em-dash（— 与 ---）= 0；禁词表 25 项（innovative, unprecedented, reveal, underscore, yet, yielding, notably, surpass, exceed, stems from, pave the way, …）= 0 命中。

## Retrieval-grounded checks
- 新颖性核验：32 项审计（web/arXiv/中文）零命中，最近邻 4 篇已区分（Howland 2019, Anvari 2016, Korb 2020/van Vondelen 2024, arXiv:2605.25192）。
- 引用完备性：9 篇全部 DOI 核验真实。1 项缺口：**Lissaman (1979) 首个数值尾流农场模型**仅有二手旁证（WES 2025 转引），未核验完整书目 → 列入投稿前待办（核验后补入 §2）。

## Final score: 8 / 10
（0 CRITICAL + 1 未决 MAJOR[期刊匹配，属作者决策] + 4 MINOR 未清[摘要长度/fig7 版式/date 行/Lissaman]）

## Submission recommendation
**Needs 1-2 days more work**：作者定目标刊（建议 WES 或 Chaos 先行）→ 按刊压缩摘要 → 补 Lissaman 引用核验 →（可选）JFM 路线需 LES/田间验证 F1–F4。
