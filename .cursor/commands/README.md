# Cursor Cmd 快捷命令

在 Cursor Agent 输入框输入 `/`，即可选用本目录下的快捷命令。文件名即命令名。

| 命令 | 用途 |
| --- | --- |
| `/update-dashboard` | 按本周数据刷新知识底座运维周报看板 |
| `/add-repo` | 向 AgentsMeetRL awesome list 添加仓库 |
| `/review` | 审查当前改动或指定文件 |
| `/fix-bug` | 定位并修复问题 |
| `/make-pr` | 整理提交并创建/更新 PR |
| `/weekly-email` | 准备周报邮件推送相关文件 |

## 用法

1. 打开 Cursor Chat / Agent。
2. 输入 `/`，选择命令（或继续键入命令名过滤）。
3. 在命令后追加具体上下文，例如：

```text
/update-dashboard 周期 2026-07-06 ~ 2026-07-12，语料总量 420 万……
```

```text
/add-repo https://github.com/org/repo 分类 Search & RAG
```

```text
/fix-bug 看板 MaaS 明细表 Token 合计不对
```

命令正文是给 Agent 的固定指令；你追加的文字会作为本次任务的补充上下文。
