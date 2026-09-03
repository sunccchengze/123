#!/usr/bin/env bash
set -euo pipefail

# Fast-forward push to main without PR
# Usage: ./scripts/ff-push.sh [branch]
# Default branch = current branch

BRANCH="${1:-$(git branch --show-current)}"
echo ">>> 当前分支: $BRANCH"
echo ">>> 目标: origin/main"

echo "--- 0. 工作区检查"
git status --short

echo "--- 1. 拉取最新 main"
git fetch origin main

echo "--- 2. 检查是否可 fast-forward"
if git merge-base --is-ancestor origin/main "$BRANCH"; then
  echo "✅ FF 安全: origin/main 是 $BRANCH 的祖先"
else
  echo "❌ origin/main 不是祖先，需要先 rebase"
  echo "请执行:"
  echo "  git rebase origin/main"
  echo "  git push origin $BRANCH -f"
  echo "  然后再跑此脚本"
  exit 1
fi

echo "--- 3. 先推自己的分支（保命）"
git push origin "$BRANCH"

echo "--- 4. 快进推送到 main"
git push origin "$BRANCH":main

echo "--- 5. 核对远端 ref"
git ls-remote --heads origin | grep -E "main|$BRANCH" || true

echo "✅ 完成：main 已快进到 $BRANCH"
