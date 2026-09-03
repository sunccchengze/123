# 真实叶片级 AI-MDO 的重开门槛

**本文件不是当前研究计划。** 它定义了：若未来研究负责人明确允许添加新公开数据、生成新 CFD/CHT/FEA 样本或使用计算资源，一个候选必须满足什么才能从 `Archive only` 升为 `Question candidate`，再可能成为 `Research candidate`。

## A. 不可替代的最小数据合同

任何重新立项的真实叶片 MDO 必须先写出一份机器可读 manifest，使每条样本具有：

```yaml
case_id: globally unique and immutable
x:
  airfoil_or_endwall_geometry: shared parameterization + units
  cooling_layout_or_internal_geometry: shared parameterization + units
  thickness/material/manufacturing_deviation: if structurally claimed
operating_condition:
  inlet_total_conditions: units
  coolant_supply: mass-flow/pressure/temperature and units
  hot-gas_thermal_boundary: units
truth:
  aerodynamic: loss/efficiency/massflow/pressure field
  thermal: fluid + solid temperature / heat flux / cooling pressure loss
  structural: constraints, material law, stress, displacement
  life: creep/TMF/HCF law and parameters if claimed
provenance:
  mesh/solver/version/convergence status
  data license
  checksum
  train_calibration_validation_test assignment
```

### Hard prohibitions

- `x` 不能仅对气动学科有定义而对冷却/结构学科通过想象补齐；
- OT、生成式配对或 shared-latent alignment 不能替代共同 `case_id`、共同 \(x\) 或可验证的物理耦合；没有这些锚点时，cross-dataset coupling 只能作为待验证假设，不能是 MDO 真值；
- CFD 的流体温度不能自动替代金属温度；
- 没有材料、约束和热—力载荷传递时不能计算可信 stress/life；
- 同一低保真求解器产生训练、选优和验证的闭环不能支持“独立验证”“真实寿命提升”；
- 未收敛、不可网格化、物理约束违例必须分源记录，不能笼统删掉。

## B. 重新寻找新颖性的顺序

先固定中心命题，再搜索；不得先做一个网络后把它描述成创新。

1. **问题：** 哪个具体设计决策在当前工程流程中因什么信息缺失而失败？
2. **机制：** 新对象究竟是多学科耦合、数据不一致、优化失败、制造容差还是生命周期风险？“AI”不是机制。
3. **反事实：** 若方法无效，哪个量会表现为无提升或恶化？
4. **最近三篇直接前例：** 对每篇写问题、输入、真值、假设、模型、优化、验证、结果和未覆盖内容。
5. **理论边界：** 哪个命题可以在明确假设下证明，哪个只能作为模型内观察？
6. **验证：** 预先确定独立 holdout、跨保真/跨几何/跨工况测试、负对照和停止规则。

GT2025-151212 是必读排除基准。任何未来声称“制造偏差/边界条件/寿命 + 3-D AI 代理”的方案必须提供逐项差异表；若差异只是数据规模、编码或网络名称，立即关闭。

## C. G0–G6 晋级检查表

| Gate | 从 Archive 到 Question 所需 | 从 Question 到 Research candidate 所需 |
|---|---|---|
| G0 主张完整性 | 明确共享 \(x\)、输出、决策、范围和不声称的内容。 | 逐条 claim ledger 绑定原始输出、证明或来源。 |
| G1 工程后果 | 指出具体失效/成本/约束，例如热点、压损、应力或寿命 trade-off。 | 在可比较单位下定量展示方法改变的决策及其意义。 |
| G2 敌对新颖性 | 查询和收集最接近来源；不说“首次”。 | 精读/比较最近三篇以上，代码/专利/中英文术语/引文追踪完成。 |
| G3 有效性 | 变量、单位、求解链和假设清晰。 | 对连续性、收敛、误差、耦合迭代、约束语义作验证；有限网格不冒充证明。 |
| G4 验证阶梯 | 可获得的真值层和验证计划可信。 | 未参与训练的 coupled cases + 至少 solver verification/独立高保真；物理主张另需实验或严格限定。 |
| G5 公平与复现 | 指定基线、split、主要指标、预算、seeds。 | 发布环境、manifest、配置、失败样本、基线实现、原始/许可允许的衍生数据。 |
| G6 投稿合规 | 识别目标期刊的作者/AI/数据政策。 | 作者独立推导、实现、写作和政策复核完成。 |

## D. 一个未来 MDO 的验证阶梯（示例，不是承诺）

| 阶段 | 能验证的内容 | 不能跳过的反例 |
|---|---|---|
| 0 — 求解器/数据合同 | mesh/convergence、单位、耦合接口、solver verification。 | 将 failed cases 静默删除、或将不同 CAD 参数化强行配对。 |
| 1 — 单学科 | 气动、热、结构每个代理的 held-out 误差与不确定性。 | 一个总体 RMSE 掩盖热点/最大应力/尾部风险。 |
| 2 — 耦合 | 同一 \(x\) 的端到端 CHT→FEA/性能传递、协同与 trade-off。 | 用独立数据集的标量当作共同目标。 |
| 3 — 优化 | 候选在未参与训练的真实求解器中回算，报故障率与 Pareto fidelity。 | surrogate-only Pareto 或只回算一个被挑选的漂亮点。 |
| 4 — 外部验证 | 适用时的实验/高保真/跨求解器验证。 | 将 RANS self-consistency 称作物理/寿命验证。 |

## E. 必须预注册的强基线

按实际问题选择，而不是挑弱方法：

- 单学科高保真 surrogate、直接优化、普通/多保真 surrogate；
- 现有团队 MSFO、SDNO 或其公开可复现近似（若问题可比）；
- 对可靠性问题：不拒答、几何距离、ensemble、分层 conformal、failure classifier/safe BO 等；
- 对 thermo-mechanical/lifing：物理链/传统 FEA-lifing、GT2025 类型点云/NO 代理（若可获得或公平重建）；
- 同一数据预算、wall-clock/compute budget、超参数预算和独立 seeds。

## F. 停止条件

下列任一条件意味着缩窄或停止，而不是继续美化结果：

1. 数据无法形成共同设计向量或关键耦合输出仍不可验证；
2. 最接近前例已完成相同问题—机制—验证组合；
3. 新方法未胜过强基线，或收益仅存在于训练分布；
4. OOD/safety/life 的保证依赖未被检验的 IID/连续/已知 Lipschitz 假设；
5. 真实求解器回算推翻 surrogate Pareto；
6. 失败样本比例、计算预算或许可使可复现验证不可行；
7. 作者无法独立解释、复算和按目标期刊规则撰写。

## G. 当前最诚实的下一步

在当前“仅公开 GE-E3/Pak-B、无外部资源”的约束下，**不要运行一个假 MDO。** Q-IO 的敌对前例审计已于 2026-09-01 触发关闭（见候选台账 §4）；不得继续以它为名开发模型。此时只剩下面两类低风险取证工作：

1. 版本化数据 manifest：若能以合法、可审计方式获取原始文件，记录 SHA-256、MAT schema、真实分割与许可，并把版本冲突写清；
2. 对未来**全新**问题做前置立项：先获得/界定满足本文件 A 节的数据合同，再从问题、机制、反事实和最近直接前例开始 G0/G2 审查；不能将新措辞回填为 Q-IO。

只有先通过这些检查，才值得请求更多资源或启动计算。
