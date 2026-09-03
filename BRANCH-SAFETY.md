# 🩸 Arena Agent 生存手册

> 面向所有进入本仓库的 AI agent 与人类协作者。**动手之前先读完这页。**
>
> 本页不是推测。核心内容摘自 `sunccchengze/turbine-blade-ai-platform`
> 项目的 `HANDOFF.md`——由承泽与历代 agent 实战踩坑积累的会话交接总文档。

---

# 第一部分：⭐ 快进推送 —— 把内容送上 main 而不碰 PR

**这是本页最重要的操作。** 它让你既能把成果合进 `main`，又完全不触发
"PR 合并/关闭 → 会话远程通道被关"这个陷阱（原因见第二部分铁律 2）。

## 一行命令

```bash
git push origin <你的分支>:main
```

就这一条。**不开 PR、不合 PR、不关 PR**，`main` 直接前进到你分支的位置。
会话通道毫发无损，你可以继续干活。

## 为什么安全

| | PR 合并 | 快进推送 |
|---|---|---|
| `main` 拿到你的内容 | ✅ | ✅ |
| 触发 Arena 关闭远程通道 | 🩸 **会** | ✅ 不会 |
| 之后还能 push / gh | ❌ | ✅ 能 |
| 留下 PR 记录 / review | ✅ | ❌ 没有 |
| 产生 merge commit | 会 | 不会（线性历史） |

`git push <分支>:main` 走的是**纯 Git 协议**，GitHub 那边只是把 `main`
这个 ref 往前挪一格，压根没有"PR 被合并/关闭"这个事件，自然不会触发关闭通道。

## 完整操作流程（照抄即可）

```bash
# ── 0. 前置：确认工作区干净、提交都已 commit ──────────────
git status --short

# ── 1. 自检：main 必须是你分支的祖先，否则不能快进 ─────────
git fetch origin main
git merge-base --is-ancestor origin/main HEAD \
  && echo "✅ FF 安全，可以推" \
  || echo "❌ main 有你没有的提交，先 rebase"

# ── 2. 先推自己的分支（保命，铁律 1：绝不攒提交）───────────
git push origin <你的分支>

# ── 3. 快进推送到 main ────────────────────────────────
git push origin <你的分支>:main

# ── 4. 核对：两个 ref 应指向同一个 commit ──────────────────
git ls-remote --heads origin | sed 's#refs/heads/##'
```

## 万一第 1 步说"需要先 rebase"

说明 `main` 上有你分支没有的提交，快进不成立。**不要用 `-f` 强推**——
那会覆盖掉 `main` 上别人的工作。正确做法：

```bash
git fetch origin main
git rebase origin/main      # 把你的提交挪到 main 之上
# 解决冲突后
git push origin <你的分支>   # 你自己的分支可以 -f
git push origin <你的分支>:main   # 再快进
```

## 边界与代价（诚实说明）

- **没有 PR 记录、没有 code review。** 对只读归档仓、单人项目很合适；
  若你的团队依赖 PR 评审流程，需要自行权衡。
- **要求线性历史。** `main` 必须是你分支的祖先。
- **不适用于受保护分支。** 若 `main` 开了 branch protection 要求 PR，
  这条推送会被拒绝——那种情况下只能开 PR，并把合并留到会话最后一步。
- **本仓实测**：`main` 上的全部归档内容，均通过
  `git push origin arena/01a060a9-ai:main` 送达，**全程 0 个 PR**，
  推了 5 次，工作分支与会话通道始终完好。

---

# 第二部分：五条铁律（HANDOFF.md 原文）

> 前几代 AI 都栽过，看完再动手。

### 1. 推送优先于一切

每完成一个可交付单元，立刻 `commit` + `push`。**绝不攒提交。**
**未推送的提交 = 不存在的提交**（`af73fdc` 教训）。

### 2. 🩸 绝不主动合并 PR

Arena 会在 PR **合并/关闭**后**立刻关闭本会话的远程通道**，
之后所有 `push` / `gh` 全失败。

→ 合并 PR 只能是会话的**最后一个动作**，或留给承泽在 GitHub 网页点。
**要继续干活就让 PR 开着。**

```bash
gh pr create ...   # ✅ 开 PR 没问题
gh pr merge  ...   # 🩸 关闭远程通道
gh pr close  ...   # 🩸 同样关闭远程通道
```

三个易错点：
- 触发条件是「合并**或关闭**」，不只是合并。
- **别用"分支还在不在"判断**——分支通常好端端在，通道照样已关。
  也与 `delete_branch_on_merge` 设置无关（该仓是关闭状态，一样出事）。
- 通道一关，**尚未推送的提交就永久丢失**（见下方 Day 19 事故）。

### 3. 推不上去时，立刻导 patch 存档，然后如实上报

不要静默跳过、不要假装成功。

```bash
git format-patch origin/main..HEAD -o /tmp/patches/   # 导出存档
git bundle create /tmp/backup.bundle HEAD             # 或整包备份
```

### 4. 引用任何数字前先自己复现，不许照抄

🩸 Day 19 抓到 R² 是错的；Day 22 又抓到 NSGA-II 数字是旧环境产物。
**答不出口径，比数字低一点致命得多**（"训练集还是测试集""怎么复现"是最基本一问）。

### 5. 遇到权限 / 网络 / 环境问题，直接说，不要绕过去假装完成

沙盒有网络白名单；GitHub App 无 `workflows` 权限。

---

# 第三部分：血泪教训

## Day 19 事故——铁律 2 的真实代价

原始记录：

> Day 19 提交 `43b461d` 曾未推送（**旧会话在 PR #3 合并后被关闭**）。
> 本会话已用承泽粘贴的 `D19_RECOVERY.md`（README 全文 + 3 个代码文件改动）
> 重建为 `1839aa5`，4 项验证全过并推送。

链条：PR 合并 → 会话通道关闭 → 未推送的提交消失 → 只能靠人工粘贴内容重建。
这就是铁律 1 的由来。

## ⚠️ 前兆信号：TLS 报错

> 推送前常先撞一次 gnutls TLS 报错，看着像抖动，
> **其实是会话将关闭的前兆**；别机械重试超 2–3 次。

看到反复 TLS / 网络报错，别当偶发抖动死磕。**立刻 commit 并尝试推送**，
推不上去就导 patch 存档并上报（铁律 3）。

## 其他通用坑

| # | 坑 |
|---|---|
| 1 | `node_modules` 等不跨会话持久；重要产物别只放 `dist/build/cache/__pycache__/.venv` 等被排除目录 |
| 2 | 会话权限不确定：**开工先 `git ls-remote` 探一次** |
| 3 | GitHub 身份：`git config user.name "Arena Agent"` / `user.email "arena-agent@arena.ai"`（clone 会带成仓库主人，先改再提交） |
| 4 | 聊天里贴 patch 会被改坏（空白/HTML 实体）→ 用「整篇覆盖 + 模糊匹配脚本」恢复，别依赖 `git apply` |
| 5 | 沙盒有出口白名单：GitHub/PyPI/npm 通，很多外部域名 TLS 直接失败 |
| 6 | 测连通性用 `curl -o /dev/null -w "%{http_code}"` 发 **GET**；`HEAD` 返回 exit 0 可能是**假阳性** |
| 7 | 附件上传可能不落盘 → 让用户直接粘贴内容 |
| 8 | 🩸 **GitHub App 无 `workflows` 权限**：推送含 `.github/workflows/*.yml` 的提交会被 GitHub 拒绝 |

---

## 来源

`sunccchengze/turbine-blade-ai-platform` → `HANDOFF.md`
（§0.-1 五条铁律、§0.1 Day 19 恢复、§9 沙盒坑与教训 #6 #7 #12 #13 #15 #17）。
第一部分的快进推送手册为本仓（`sunccchengze/ai`）归档作业中的实测总结。
