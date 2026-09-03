# ⚡ 快进推送速查卡 — 绕过 PR 更新 main

> 一句话：`git push origin <你的分支>:main`

## 何时用
- 你在 Arena 会话里，`arena/xxxx` 分支上有新提交
- 想让 `main` 也拿到内容，但**不想关闭远程通道**（合并 PR 会导致通道关闭，之后 push 全部失败）

## 何时不能用
- `main` 开了 Branch Protection → Require PR → 推送会被拒，只能走 PR 且把 merge 留到最后一步
- `main` 超前于你（你分支不是基于最新 main）→ 先 rebase

## 标准 4 步

```bash
git status --short
git fetch origin main
git merge-base --is-ancestor origin/main HEAD && echo "✅可快进" || echo "❌需rebase"

git push origin $(git branch --show-current)

git push origin $(git branch --show-current):main

git ls-remote --heads origin | cat
```

## 如果提示 non-fast-forward

```bash
git fetch origin main
git rebase origin/main
# 解决冲突后
git push origin $(git branch --show-current) -f
git push origin $(git branch --show-current):main
```

## 对比

|  | PR Merge | FF Push |
|---|---|---|
| main 更新 | ✅ | ✅ |
| Arena 通道 | 🩸关闭 | ✅保留 |
| PR 记录 | 有 | 无 |
| 线性历史 | 否 | 是 |

## 保命 3 件套（推失败时）

```bash
git format-patch origin/main..HEAD -o /tmp/patches/
git bundle create /tmp/backup.bundle HEAD
git log --oneline origin/main..HEAD
```

## 本仓库实测

- 当前 `origin/main` = `2bb4636`
- 本分支 `arena/01a06530-can-ai-write-papers-scz` 与 main 同步
- 满足 FF 条件，可直接 `./scripts/ff-push.sh`

> 来源：SCZ_Archived/BRANCH-SAFETY.md
