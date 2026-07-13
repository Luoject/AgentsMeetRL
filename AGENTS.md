# AgentsMeetRL

本仓库是静态 awesome list：`README.md`（精选列表）、`index.html`（交互仪表盘）、`logo.png`，以及本 fork 保留的 `knowledge-ops-dashboard.html`（知识底座运维周报看板）。

## 运行

```bash
python3 -m http.server 8000
# http://localhost:8000/index.html
# http://localhost:8000/knowledge-ops-dashboard.html
```

不要用 `file://` 打开；`index.html` 依赖运行时 `fetch()`。

## Lint / test / build

无。没有包管理器、构建步骤或测试套件；改完刷新页面即可。

## Cursor 快捷命令（Slash Commands）

项目级命令在 `.cursor/commands/`。在 Cursor 聊天框输入 `/` 即可选用：

| 命令 | 文件 | 用途 |
| --- | --- | --- |
| `/add-repo` | `add-repo.md` | 向 README 对应分类追加新的 Agent+RL 仓库 |
| `/update-ops-dashboard` | `update-ops-dashboard.md` | 按新一周数据刷新运维周报看板 |
| `/preview-site` | `preview-site.md` | 本地启动静态服务并给出预览地址 |
| `/sync-badges` | `sync-badges.md` | 核对并修正顶部分类徽章数量 |
| `/review-diff` | `review-diff.md` | 审查当前工作区或分支改动 |

新增命令：在 `.cursor/commands/` 下添加描述性 `.md` 文件即可，文件名即斜杠命令名。
