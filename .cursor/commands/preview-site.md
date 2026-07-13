# 本地预览站点

在本仓库根目录启动静态服务，预览交互看板与运维周报。

## 步骤

1. 确认工作目录为仓库根目录（含 `index.html`、`knowledge-ops-dashboard.html`、`README.md`）。
2. 若 8000 端口空闲，执行：`python3 -m http.server 8000`。
3. 打开：
   - AgentsMeetRL 仪表盘：`http://localhost:8000/index.html`
   - 知识底座运维周报：`http://localhost:8000/knowledge-ops-dashboard.html`
4. 不要用 `file://` 打开；`index.html` 依赖运行时 `fetch()`。
5. 若用户只想看某一个页面，优先打开对应 URL。

## 说明

- 本仓库无 package manager / build / lint / test。
- `index.html` 会请求外网（Chart.js CDN、shields.io 星标、README）；内网受限时图表或星标可能加载失败，属预期。

## 输出

告知已启动的端口与两个页面的访问地址；若端口冲突，换端口并说明。
