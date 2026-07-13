# 周报邮件推送准备

根据最新看板周期，准备或更新周报邮件相关资产。

## 输入

用户可附上：收件人、周期、看板 URL、是否需要 PDF/附件说明。

## 要求

1. 对齐 `knowledge-ops-dashboard.html` 的当前报告周期与标题。
2. 若仓库中存在 `email-weekly-report.html`、`dashboard-config.json`、`send-weekly-report.py`、`export-dashboard-pdf.py`，按现有结构更新；不存在则仅给出最小可行方案，不擅自引入复杂依赖。
3. 邮件正文保持简洁：周期、核心 KPI、看板链接；避免堆砌大段表格。
4. `dashboard-config.json` 中的 SMTP/密码仅保留占位符，绝不写入真实密钥。
5. 说明发送前还需用户本地配置的项（SMTP、收件人等）。
6. 用简体中文回复变更与使用步骤。
