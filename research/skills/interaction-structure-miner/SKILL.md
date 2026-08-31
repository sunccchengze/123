---
name: interaction-structure-miner
description: |
  从工程/科学系统的目标函数中挖掘"交互结构"：把混合偏导分解为互补通道与替代通道（C−S 分解），
  生成符号矩阵、相图与"最优点解耦"检验，并给出贪心/解耦算法的交互能界；附带多通道新颖性审计协议。
  适用于风电场偏航优化（FLORIS/GCH 类）、以及任何"可加式作用核 + 凸功率映射"的多智能体目标函数。
  触发词：「交互结构」「互补替代」「符号矩阵」「最优点解耦」「C−S 分解」「交互能界」「新颖性审计」。
  English triggers: "interaction structure", "complements substitutes", "sign matrix", "decoupling at the optimum",
  "mixed partial decomposition", "novelty audit".
---

# Interaction Structure Miner · 交互结构挖掘术

> 「别急着优化。先问：这个目标函数里，谁的决策帮谁、谁的决策挤谁？」
> —— 本技能把这句话变成可执行的二阶分析流水线，并强制每项"新发现"通过多通道新颖性审计。

## 核心理念

许多多智能体工程目标（风电场偏航功率、排布、联合控制）的表层是"非凸、多模态、NP-hard"，
但其**混合偏导结构**往往只有两种通道：

- **互补通道 B_ij ≥ 0**：i 与 j 的决策通过共同的受益对象互相增强（`∂²P/∂γi∂γj > 0`）；
- **替代通道 A_ij ≥ 0**：j 在 i 的下游时，j 自身功率权重（如 cos^p(γj)）随 yaw 下降，削弱 i 的边际价值（`∂²P/∂γi∂γj < 0`）。

`M_ij = B_ij − A_ij` —— 符号由**作用图（DAG）拓扑**与**工作点**共同决定。这个分解是
理解"为什么贪心几乎最优"、"为什么最优点处问题变得可分离"、"为什么最优剖面单调递减"的钥匙。

## 执行流程（五步）

### Step 1: 建模与核性质声明
写清系统属于哪个模型类（本技能默认：可加式作用核 + 凸功率映射 + 随自身决策递减的功率因子）：
- 决策变量与作用 DAG（谁影响谁）；
- 核的"恢复单调性"：上游决策从不加深下游亏损（`r_ij = −∂w_ij/∂γ_i ≥ 0`）；
- 叠加规则（线性 / 平方和）。

### Step 2: C−S 分解（纸笔 + sympy 验证）
对每个 (i, j) 推导 `M_ij = Σ_{k≻i,j} 互补项 − 替代项·1{j≻i}`。
- 纯串列对 → 替代（两机问题在盒上严格次模）；
- 共享下游的横向对 → 互补；
- 链相邻对 → 符号随工作点翻转（相边界 B=A，见 `scripts/analytic_3chain.py`）。
**相边界必须给出显式条件**（间距/湍流/偏航态的依赖方向），不可只给数值。

### Step 3: 数值验证（FLORIS 或等价模拟器）
- 中心差分混合偏导（h 选择：先 5° 粗扫，关键点 2.5°/1.25° 收敛性检查）；
- **符号矩阵**（原工作点/最优点/不同风向）——必须复现 DAG 拓扑；
- **相图**：扫描 (γi, γj) 平面记录 sign(M_ij)；
- **最优点解耦检验（Law 1）**：比较 `‖M_off‖/‖diag(M)‖` 在一般点 vs 最优点，期望下降一个量级；
- 边界纪律：模拟器警告区域（如 FLORIS 负速度、≥25° 极端偏航）**排除出声明**，写进限制。

### Step 4: 算法推论（至少给一条，且给界）
- 贪心/串行方法的**交互能界**：gap ≤ ½Σ_{i≠j} M̄_ij γ̄² + 网格项（用采样 M̄_ij 评估，与实测 gap 同量级才算合格）；
- 或"最优点解耦 ⇒ 解耦 Jacobi 扫描（DJS）2-3 轮收敛"的验证；
- 或符号矩阵聚类 → 去中心化控制（阈值 τ 的含义：低于 τ 的耦合最多损失 τ·γ̄²/对）。

### Step 5: 新颖性审计（硬性，见 `references/research/03-novelty-audit.md`）
**任何"首次发现"的表述必须通过六通道检索并留档**，否则降级为"在检索范围内未见先例"：
arXiv（all: 短语组合）、OpenAlex fulltext.search、Crossref、Web 中英多语、OEIS（若涉序列）、GitHub 代码。
命中实质先例 → 作废或深挖到无先例子层；相邻先例必须精确区分并引用（见 03 中 2026-08-30 实例）。

## 诚实边界

- 本技能证明的是**模型类上的结构**，不是流体物理定律；LES/实测外推是假设，必须标注。
- 最优点解耦（Law 1）对**内点最优**成立；角点最优平凡对角，不构成证据。
- 数值发现≠定理：能证则证，不能证就写"经验定律 + 部分机制（stationarity identity）"。
- 审计是时间与查询受限的："搜不到"永远不等于"不存在"。

## 快速上手

```bash
python scripts/analytic_3chain.py                 # 三机链 C−S 分解与相边界
python - <<'EOF'                                    # FLORIS 符号矩阵（示例）
import numpy as np, pathlib, floris
from floris import FlorisModel
# ... 见 references/research/01-discovery-log.md 的完整流水线
EOF
```

## 参考文件

- `references/research/01-discovery-log.md` — 2026-08-30 完整发现日志（假设→证伪→转向→验证），本技能的方法论源头；
- `references/research/02-theory.md` — 定理与命题清单（Theorem 1 C−S 分解 / Law 1 解耦 / Theorem 2 交互能界 / 比较静态）；
- `references/research/03-novelty-audit.md` — 六通道审计协议 + 当次审计实录（含作废记录）。

> 本 Skill 由 [女娲 · Skill造人术](https://github.com/alchaincyf/nuwa-skill) 主题模式生成，创建者：孙承泽的科研智能体（Arena session 01a053b1-123）。
