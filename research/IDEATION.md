# IDEATION — 候选创新点库（v0.1）

> 每个候选点的"新颖性"都是**待证伪假设**。证伪通道：arXiv/OpenAlex/Crossref/OEIS/Web(中英)/GitHub。
> 规则：任何通道命中实质先例 → 作废或深挖到无先例子层。

## 背景锚点（承泽的项目）

- 风电场偏航优化：FLORIS 仿真，两机串列 +25° 增益 8.13%；3×3 阵列统一 +14.87%、逐排贪心 +24.04%、`[30,20,0]°` 与最优差 <1%。
- POD：Mode0 76.38% + Mode1 21.58% = 97.97%（前两阶）。
- PPO seed42：MAE 0.523%。
- 悬而未决的深层问题：**为什么贪心这么好？为什么响应流形如此低秩？逆问题（功率跟踪）为什么好解？** —— 全是"结果在手、理论缺位"的富矿。

## 候选 P1 — 尾流偏航优化的次模性结构与贪心保证（主候选）

- **命题**：在 FLORIS 类尾流模型（高斯尾流+线性/二次叠加）下，把偏航决策离散化，全场功率函数是否（近似）次模？若证得次模性，贪心即可给 (1−1/e) 近似保证，从理论上解释"贪心≈全局最优"。
- **可证伪**：找到反例（枚举小阵列/粗离散）即推翻；或检索到先例即作废。
- **为什么可能没人做过**：风电场优化文献用遗传算法/序列二次规划/MPC 的极多，但"次模性/近似保证"的视角需要离散优化背景，跨域冷门。
- **审计查询**："submodular wind farm"、"submodularity wake steering"、"greedy approximation guarantee wind farm optimization"、"matroid wind turbine yaw"。
- **潜在期刊**：Renewable Energy / Wind Energy / IEEE Trans. Control Systems Technology / IEEE Trans. Sustainable Energy；数学版可投 Operations Research Letters / SIAM J. Optimization 信。
- **可行性**：本地实现高斯尾流模型（闭式），数值搜索反例 + sympy 符号验证 + 定理证明。完全可行。

## 候选 P2 — 偏航响应流形的低秩结构定理（主候选）

- **命题**：在"自损项（单变量，每机同形）+ 成对增益项（双变量）"的分解下，P(γ)=Σᵢf(γᵢ)+Σᵢ<ⱼg(γᵢ,γⱼ;dᵢⱼ) 的变差（ANOVA 型分解）具有低秩结构 → 解释 POD 两阶 97.97% 的机制性根源。推广：给出一类"稀疏交互流形"的低秩定理。
- **可证伪**：数值分解残差大即假；或该分解已见于降阶模型文献。
- **审计查询**："ANOVA decomposition wind farm"、"low-rank yaw response"、"POD wake steering manifold"、"HDMR wind farm power"。
- **潜在期刊**：Wind Energy / Renewable Energy / SIAM J. Sci. Comput.（若有普适定理）/ J. Fluid Mech.（若含流动结构论证）。
- **可行性**：完全本地可算（他们有 POD 数据口径，我可复现高斯模型版）。

## 候选 P3 — 功率跟踪逆问题的良定性与显式结构

- **命题**：给定目标功率 P*，求 γ* 使 P(γ)=P*。证明（在自然条件下）逆映射存在、连续、（分段）可逆；给出单调性/闭式结构（如 Lambert-W 型）。他们的双线性代理+反向搜索将有定理支撑。
- **审计查询**："inverse problem yaw power tracking"、"invertibility yaw power curve wind farm"、"closed form optimal yaw angle"。
- **期刊**：Wind Energy / IEEE TSTE / Automatica（若控制论化）。

## 候选 P4 — 尾流链的连分数/闭式结构（数学侧）

- **命题**：串列 N 机、二次叠加高斯尾流的稳态功率递推能否化为新的一类连分数/非线性递推，并证得新闭式（可能引出新常数/新序列，进 OEIS 审计）。
- **风险**：可能形式化后发现平凡；或与既有"尾流叠加闭式解"重合。
- **审计查询**："continued fraction wake model"、"closed form serial turbines quadratic superposition"。

## 候选 P5 — 元科学：一条新的经验定律（数据侧）

- **方向**：用 arXiv/OpenAlex/GitHub 全量数据找一条前人未报告的定量规律（候选：预印本→期刊的存活函数新协变量效应；AI 时代摘要词频相变的新不变量；代码可用性与引用加速的非线性门限……）。
- **规则**：任何候选定律先检索，凡有同类文献即作废；必须"具体到数字"。

## 候选 P6 — 组合学：小网络同步模式的计数（OEIS 审计）

- **命题**：全同频率 Kuramoto 相振子网络上相位锁定解的计数/分类，若产生新序列且 OEIS 无记录，可做一个小而硬的组合结果。
- **审计**：OEIS + "number of phase-locked states Kuramoto"。

## 后备

- P7：两机最优偏航角的闭式解（Lambert-W 族）——查先例后决定。
- P8：偏航率限制（rate limit）下的农场功率损失律——查"yaw rate limit power loss"。
- P9：贪心最优性的充要条件（对 P1 的深化，独立成文）。
- P10：偏航+储能/功率跟踪的联合可解性。

## 今日执行顺序

1. 审计 P1（4 组查询 × 多通道）→ 存活则深挖。
2. 审计 P2、P3、P7。
3. 本地实现高斯尾流模型，开始数值探查（支撑所有存活候选）。
4. 每步写入 NOVELTY_DOSSIER.md 与 SELF_AUDIT.md。
