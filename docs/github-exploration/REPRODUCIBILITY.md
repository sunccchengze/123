# Reproducibility

## 前置条件

- 可访问 GitHub 公开 API 和 `https://github.com/trending`。
- 已安装 `gh`，但不需要用户密码或 token 写入命令。
- 目标账号为 `sunccchengze`。

## 复现步骤

### 1. 账号与公开仓库

```bash
gh api users/sunccchengze
gh api 'users/sunccchengze/repos?per_page=100&sort=pushed&direction=desc'
```

### 2. 分支感知的最新提交

对每个公开仓库执行：

```bash
gh api 'repos/sunccchengze/<repo>/branches?per_page=100'
gh api 'repos/sunccchengze/<repo>/commits/<branch-head-sha>'
```

把所有 branch head 的 `commit.committer.date` 排序，选择最大值；同时读取 `main` head 用于对比。分支名称含 `/` 时，优先使用 branch head SHA 读取 commit，避免 URL 编码问题。

### 3. Trending

```bash
curl -L -A 'Mozilla/5.0' -sS https://github.com/trending -o /tmp/trending.html
```

解析所有 `<article class="Box-row">`，取前十个 `<h2>` 仓库链接和每个 article 的描述、语言、总 star、今日 star。抓取后立即记录 UTC 时间。

### 4. 用户技能库

当前报告读取了固定分支：

```text
https://github.com/sunccchengze/-SKILL-/tree/arena/01a048e7-skill
head: 8d749b9a0270e3ea6d330bb54e172cc26d7f1d65
```

本任务实际使用/核验的入口：

```text
SKILL.md
TASK_ROUTING.md
AGENTS.md
skills/core/research-expert-system/SKILL.md
skills/core/official-source-router/SKILL.md
```

### 5. 下一次更新

- 将时间窗口向前滚动到新的抓取日期；
- 重新枚举所有分支，不复用旧的 latest branch；
- 对同一仓库记录新旧 head 的差异；
- 对 Trending 重新排序并标记变化；
- 对推荐仓库重新核对 README、license、release 和依赖；
- 新报告使用新日期文件，旧报告保持不变。
