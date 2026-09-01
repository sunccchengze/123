# FAN-02 公开发布内容审计（2026-09-01）

**对象：** *Fan Acoustic Noise 2（FAN-02）* 的当前公开 Zenodo release：record `17909944`、DOI [`10.5281/zenodo.17909944`](https://doi.org/10.5281/zenodo.17909944)。

**当前处置：** `future-release / contact-dependent reference benchmark`，**不是**当前可启动的 AI-FSAI-MDO 数据合同，也不是投稿候选。

**审计问题：** 论文所描述的封闭离心风机流—固—声（FSAI）测量，是否已经以可重放、可分组留出的数据形式包含在当前公开 record 内？

**简短答案：** 当前 record 的公开文件 API 只列出 CAD 几何与传感器位置文件。它没有在该清单中列出能够复现论文级 PIV、压力、振动或声学分析的原始/派生测量文件。因此，该实验体系有很高的**论文级科学价值**，但当前发布内容没有通过本项目所需的数据合同门槛。

> 这里的“没有列出”仅指下述 record/revision 的当前 `/files` 响应。它不声称实验未进行、数据永远不存在、作者没有另行保管数据，或没有未来/独立 companion release。

---

## 1. 主张—证据台账

| 本记录中的表述 | 证据类别 | 紧邻来源 | 不能扩展成什么 |
|---|---|---|---|
| 当前 release 的文件 API 返回一个含 11 项的 `entries` 数组。 | 一手的 record 文件清单事实。 | [Zenodo `/files` API](https://zenodo.org/api/records/17909944/files)，2026-09-01 读取；响应末尾为 `default_preview` 与空 `order`，无额外条目。 | 不把 API 列表误写成本地下载、逐字节校验或永恒的 repository 状态。 |
| 这 11 项是 3 个 STEP 文件与 8 个传感器位置 TXT 文件。 | 一手的 file-name/type/size 事实。 | 同一 [Zenodo `/files` API](https://zenodo.org/api/records/17909944/files)。完整转录见 §2。 | 不把文件名中的 `Pressure`、`Sensor` 或 CAD 几何推断成压力时序、传感器读数、CFD 网格或结构声学模型。 |
| 当前清单未列出 PIV/HWA、叶片压力时序、LSV、声强、麦克风时序、CFD fluid domain、结构声学 mesh 或 common-run table。 | 受限的 manifest 范围判断。 | §2 的逐项 inventory，与论文概述的测量类别作比对。 | 不声称这些数据在所有位置、所有 revision 或作者私有存档中不存在。 |
| 论文说明该 400-mm、12-blade enclosed centrifugal fan 进行了多类气动、结构和声学测量。 | 论文级实验描述。 | [FAN-02 overview, *Journal of Imaging*, 2026](https://www.mdpi.com/2504-186X/11/1/10)。 | 不把论文实验描述当作当前 public release 的逐文件 schema，也不把“whole or in part”数据可用措辞当作原始全量文件已经下载的证明。 |
| 当前 release 无法支撑同一 run 的跨模态训练、独立 grouped holdout 或设计优化回算。 | 数据合同判断。 | 原始文件/键/分组/设计变量没有出现在 §2 的当前 inventory；本项目真实 MDO 定义见 [候选台账 §1.2](CANDIDATE_LEDGER_2026-09-01.md#12-最小真实-mdo-证据图)。 | 不否定未来完整发布后开展 FSAI 学习的价值；也不把这个 archive 缺口归因于任何实验质量问题。 |

---

## 2. 当前 `/files` inventory 的逐项转录

本节转录的是 2026-09-01 读取到的 [Zenodo file endpoint](https://zenodo.org/api/records/17909944/files) 的 `key`、`size` 与 advertised MD5。MD5 是远端元数据，**不是**本地重新计算的 checksum。

| 类别 | `key` | bytes | advertised MD5 |
|---|---|---:|---|
| STEP geometry | `Housing_Structure.stp` | 8,885,120 | `ac9b4be7173c988bf742c559c9c7ec5d` |
| sensor positions | `Sensor_Positions_Spiral_Housing_m.txt` | 1,136 | `9e97271c5411e6a9b3cb39e34232c94d` |
| sensor positions | `Sensor_Positions_Spiral_Housing_mm.txt` | 578 | `38cdf0d95df732548ce6df22be12507d` |
| STEP geometry | `housing_structure_advanced.stp` | 10,110,179 | `b65a48070879fdc6dfadf28e60c4c28a` |
| sensor positions | `Sensor_Positions_Backplate_m.txt` | 941 | `c9eaf05da8e9773a6451f9fff0eb281d` |
| sensor positions | `Sensor_Postions_Fan_m.txt` | 903 | `3da142ecda79051bb41c3afbbede3518b` |
| STEP geometry | `Housing_WallPressure_Window.stp` | 11,563,976 | `598237ed6509713eff5302069508b96b` |
| sensor positions | `Sensor_Position_Circle_mm.txt` | 440 | `7f03fe5004e2d9cd13397941e81f1726` |
| sensor positions | `Sensor_Positions_Backplate_mm.txt` | 531 | `4383190ceb428fe2348aa77703a5c883` |
| sensor positions | `Sensor_Position_Circle_m.txt` | 794 | `415b235a74806ac9d7c01ea7d3b81569` |
| sensor positions | `Sensor_Postions_Fan_mm.txt` | 421 | `06e18d460e131431d71a49e9b3a859bd` |

**Count and size check.** 3 STEP + 8 TXT = 11 files; total advertised size = 30,565,019 bytes. The current endpoint identifies `Housing_Structure.stp` as its default preview. No item in this inventory has a raw-signal, image/velocity-field, tabular run-data, CFD-domain, finite-element, acoustic-mesh, or experiment-log filename/type.

A filename inventory is not enough to prove a scientific semantic negative. The limited conclusion is narrower: **the current record manifest does not deliver the files needed to establish those semantics.**

---

## 3. Why the paper–release distinction matters

The [FAN-02 overview paper](https://www.mdpi.com/2504-186X/11/1/10) describes a rare experimental chain on one real enclosed centrifugal fan: flow-field measurements, blade/casing pressure and vibration-related measurements, and acoustic measurements including sound intensity and free-field microphones. This is exactly the kind of common physical object that could eventually make a FSAI transfer question meaningful.

However, an AI-MDO experiment requires more than a paper-level description of instruments. At minimum, it needs the following auditable links.

| Required item for a current FSAI learning/MDO claim | Evidence in current 11-file inventory | Consequence now |
|---|---|---|
| Sample/run ID linking flow, pressure, structural and acoustic observations | Not listed. | Cannot define paired multimodal examples or prevent cross-run leakage. |
| Raw or explicitly derived PIV/HWA, pressure, LSV, sound-intensity and microphone data | Not listed. | Cannot train, reproduce figures, or quantify cross-domain prediction error. |
| Operating-point, acquisition, calibration and synchronization metadata | Not listed. | Cannot define experimental groups, uncertainty, or a defensible holdout. |
| Geometry/design intervention table with manufacturing/operating constraints | Not listed beyond CAD and locations. | Cannot formulate or validate a design-level MDO decision. |
| Structural/acoustic model inputs, mesh/units/material/boundary data, or independently replayable solver results | Not listed. | Cannot turn casing-response/radiation language into a coupled truth model. |
| Frozen independent validation protocol | Not listed. | Cannot make a generalization, optimization or safety claim. |

The correct state is therefore not “FAN-02 failed scientifically.” It is “**the current public archive payload has not demonstrated the data contract needed for the proposed use.**”

---

## 4. Novelty boundary if a complete release later appears

A fuller release would solve a data-access gate; it would not automatically solve novelty. Two direct centrifugal-fan vibroacoustic optimization predecessors already prevent a generic proposal such as “use an AI surrogate/NSGA-II to change volute thickness and trade mass against noise.”

| Direct predecessor | Explicit scope used here | Consequence for a future FAN-02 route |
|---|---|---|
| [2012 centrifugal-fan volute vibroacoustic optimization](https://www.sciencedirect.com/science/article/abs/pii/S0022460X1200003X) | Unsteady pressure excitation, structural/acoustic modeling, local thickness design and noise optimization. | Do not claim the generic flow-induced-vibration/noise thickness mechanism is unstudied. |
| [2019 centrifugal-fan vibroacoustic optimization](https://www.mdpi.com/2076-3417/9/5/859) | CFD excitation, FEM, panel-thickness variables, RBF surrogate, NSGA-II, radiated sound power and mass objectives. | A neural surrogate or a different optimizer alone is not a distinct contribution. |

If public paired data later arrive, a new route still needs to predefine all of the following before implementation:

1. a specific intervention and a physically testable transfer mechanism, rather than a generic efficiency/noise Pareto wrapper;
2. the exact common run/design key across modalities;
3. a frozen grouped holdout that separates operating sessions and/or design interventions;
4. direct predecessor comparisons, including any FAN-01 PCWE-source ML work after full-text review; and
5. an independent replay, additional experiment, or high-fidelity calculation that tests the optimized decision.

Until then, neither the existence of an impressive experiment nor a keyword search for “FAN-02 optimization” establishes a paper contribution.

---

## 5. Re-entry protocol

FAN-02 may be reconsidered only after a newly accessible release passes all of these checks:

1. **Freeze the artifact.** Record the Zenodo revision, DOI, file API response, license, retrieval time, advertised checksums, and locally computed SHA-256 values.
2. **Audit schema before modeling.** Identify raw versus processed files, units, sensor coordinate frames, sample rate, clocks, calibration, operating point, run/session identifiers, and exclusion criteria.
3. **Prove the pairing.** Build an explicit table showing which flow, pressure, vibration and acoustic records belong to each physical run; do not infer pairing from filenames or proximity in time.
4. **Predeclare validation.** Group by the actual dependence structure (at least session/run; design and operating point where available), create a final untouched test partition, and retain negative controls.
5. **Re-open novelty separately.** Read the closest FSAI, fan-vibroacoustic and PCWE/ML predecessors in full, state a narrower mechanism and a kill criterion, then re-run G0–G6.

Before step 1 succeeds, the only legitimate use of the current release is geometry/sensor-layout reference or future benchmark discovery—not training, optimization, or claims about coupled FSAI prediction.

---

## 6. Adversarial read and residual uncertainty

| Reviewer role | Objection | Current answer |
|---|---|---|
| Experimentalist | “The paper documents real measurements; why call the dataset incomplete?” | The audit does not challenge the experiments. It distinguishes them from the exact public release inventory, which currently exposes only 11 geometry/coordinate files. |
| Data steward | “Could a future file/revision change the conclusion?” | Yes. The conclusion is revision- and endpoint-specific and must be rechecked at re-entry. |
| FSAI specialist | “Could the CAD and sensor locations be enough to reconstruct the experiment?” | Not without time series/fields, calibration, conditions, material/model data and run links. Reconstruction would introduce unvalidated assumptions. |
| MDO reviewer | “Why not optimize geometry using the CAD alone?” | CAD alone supplies neither objective/constraint truth nor an independent replay protocol. A generic fan noise/weight surrogate route also faces the direct predecessors in §4. |
| Novelty reviewer | “Does no exact FAN-02 paper prove novelty?” | No. An absent exact-hit search is not evidence of novelty. The next applicable proposal must survive full-text predecessor and mechanism comparison. |

**Residual uncertainty.** This audit has not established whether other records, supplementary repositories, author-mediated releases, or future revisions will carry the missing data. It records a reproducibility gate for the current public artifact, not a universal verdict on the FAN-02 programme.
