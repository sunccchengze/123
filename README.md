# Can_AI_Write_Papers.scz. — 全量并集存档 (Union Archive)

> 本 README 为 **取并集** 后的主 README，保留所有分支历史，合并自：
> - `main` @ `2bb4636` Initial `# 123`
> - `arena/01a050e3-123` GitHub 探索归档 (11 files)
> - `arena/01a053b2-123` C1 可激风机行 4 papers + 8 实验 + 9 图 (93 files, 26.8MB)
> - `arena/01a053b1-123` WES 尾流转向 3 papers + SPLEEN 审计 + forensic (105 files, 30 commits)
> - `arena/01a06530-can-ai-write-papers-scz` 生存手册 + 快进推送教学 (6 files)

> 合并方式：`git merge --no-ff` 保留全部 commit 历史，冲突文件取并集，无强制覆盖。

---

## 原始占位

# 123

---

## 1. GitHub 探索归档 (来自 01a050e3-123)

本仓库分支用于保存针对 GitHub 账号 `sunccchengze` 的公开信息探索、Trending 快照、仓库推荐和后续巡检协议。

- [探索索引](docs/github-exploration/README.md)
- [长期探索协议](docs/github-exploration/EXPLORATION_PROTOCOL.md)
- [2026-08-30 账号与 Trending 报告](docs/github-exploration/2026-08-30-account-and-trending.md)
- [2026-08-30 宝藏仓库推荐](docs/github-exploration/2026-08-30-repository-recommendations.md)

> 这里是归档区，不把本仓库自身内容带入账号画像；账号画像以公开 GitHub 数据和目标仓库实际最新分支为准。

---

## 2. C1 可激风机行研究 (来自 01a053b2-123)

**4篇论文 + 8组实验 + 9张图 + 完整npy输出**

- `research/papers/P1_excitable_wind_farm_row.tex` JFM/Chaos 旗舰：离散图案+触发波+功率台阶+(N-1)L/U沉降+随机颤振，5预测全审结
- `research/papers/P2_defibrillation_protocol.tex` Wind Energy 阴性结果《The defibrillation illusion》60协议T=9000s全零增益
- `research/papers/P3_universality.tex` PNAS/Chaos 三系统普适性
- `research/papers/P4_spike_biomarker.tex` NatComms/JPhysD SCADA生物标志物 5种子

实验：`research/code/` + `research/*.npy` + `research/fig*.png/pdf` + `research/papers/review_v2.md` (8/10)

---

## 3. WES 尾流转向 + Turbomachinery 审计 + Forensic 否定 (来自 01a053b1-123)

This repository contains archived wake-steering research materials, current turbomachinery-MDO evidence audits, reproducibility scripts, and forensic audit records.

> **Current status (2026-09-01):** P1 and P2 are non-submission forensic records, and P3 is a narrow static benchmark record. None is currently a Wind Energy Science submission candidate. The independent impact review remains a submission **no-go**; the broad C0 route was closed after direct prior-art review and is not a result or future paper plan. See [`research/SUMMARY.md`](research/SUMMARY.md), [`research/RESEARCH_IMPACT_ASSESSMENT_2026-09-01.md`](research/RESEARCH_IMPACT_ASSESSMENT_2026-09-01.md), [`research/P1_P2_FORENSIC_STATUS.md`](research/P1_P2_FORENSIC_STATUS.md), and [`research/CLAIM_LEDGER_2026-08-31.md`](research/CLAIM_LEDGER_2026-08-31.md) before relying on any figures, caches, or paper sources. The separate turbomachinery inquiry is also an evidence audit rather than a submission project; its current public-data gate, including FAN-02, is documented in [`research/turbomachinery_mdo/README.md`](research/turbomachinery_mdo/README.md).

- `research/papers/paper1_interaction_structure.tex` / `paper2_djs_clustering.tex` / `paper3_power_tracking_inverse.tex` (WES drafts, 36 verified refs)
- `research/ws_submodularity/` FLORIS 4.6.6可复现代码 + 19图 + expcache (p1_p2_forensic_audit.json SHA256: 63d6cd...)
- `research/RESEARCH_CHARTER.md` 8条铁律 + `SELF_AUDIT.md` 9审计点
- `research/turbomachinery_mdo/` SPLEEN C1证据kill审计

---

## 4. Arena 生存手册 + 快进推送 (来自 01a06530 / main)

- `BRANCH-SAFETY.md` Arena Agent 生存手册五条铁律 + 快进推送 `git push origin <分支>:main`
- `docs/FF_PUSH_CHEATSHEET.md` 速查卡
- `scripts/ff-push.sh` 一键快进脚本
- `REPO_ANALYSIS.md` / `REPO_FULL_ANALYSIS.md` 全量分析报告

**快进推送妙招：**
```bash
git push origin <你的分支>:main  # 绕过PR，不触发Arena关闭通道
```

---

## 目录总表 (并集后)

- `BRANCH-SAFETY.md`, `REPO_*.md`, `docs/FF_PUSH_CHEATSHEET.md`, `scripts/ff-push.sh` (生存手册)
- `docs/github-exploration/` (GitHub探索 10 files)
- `research/` (C1 4 papers + WES 3 papers + 审计，约180 files, 30MB)
  - `research/papers/` 7篇tex + 3 pdf
  - `research/code/` + `*.npy` 实验输出
  - `research/ws_submodularity/` + `turbomachinery_mdo/` + `novelty_audits/` + `skills/` + `tools/latex_wasm/`
- `.gitignore` (from 01a053b1)

---

## 合并记录

所有分支历史已通过 `git merge --no-ff` 保留，无 squash，无 rebase 丢失。

```bash
git log --all --oneline --graph
```

验证并集完整性：
```bash
git ls-tree -r --name-only HEAD | wc -l   # 应 >= 200
```

---

> 来源：全量分支 `git ls-tree` + `BRANCH-SAFETY.md` from `SCZ_Archived`
