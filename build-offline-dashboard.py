#!/usr/bin/env python3
"""生成优化版离线看板：纯 SVG/CSS 图表，无外部依赖，体积小、打开即渲染"""

import math
from pathlib import Path

OUTPUT = Path("知识底座运维周报看板.html")
COLORS = ["#3b82f6", "#22c55e", "#f59e0b", "#ef4444", "#a855f7", "#06b6d4",
          "#ec4899", "#84cc16", "#f97316", "#6366f1", "#14b8a6", "#e879f9"]

DATA_SOURCES = [
    ("support", "文档", "在线", 580290, "天级刷新", "2026-07-01"),
    ("support", "案例", "在线", 119868, "天级刷新", "2026-07-02"),
    ("support", "案例(iCase)", "在线", 772103, "天级刷新", "2026-07-02"),
    ("support", "公告", "在线", 57688, "天级刷新", "2026-07-02"),
    ("supportE", "文档", "在线", 153995, "天级刷新", "2026-07-01"),
    ("supportE", "案例", "在线", 117953, "天级刷新", "2026-07-03"),
    ("supportE", "公告", "在线", 31334, "天级刷新", "2026-07-02"),
    ("iTSC", "方案库", "在线", 40384, "天级刷新", "2026-07-01"),
    ("3MS", "社区/文档", "在线", 736544, "天级刷新", "2026-07-02"),
    ("isup", "咨询文档", "在线", 2463, "天级刷新", "2026-07-02"),
    ("getit", "文档", "在线", 587546, "天级刷新", "2026-07-01"),
    ("linstar", "洞察报告", "在线", 10234, "天级刷新", "2026-06-27"),
    ("O3社区", "论坛等", "在线", 50745, "天级刷新", "2026-07-02"),
    ("MCD", "政企营销资料", "在线", 32906, "天级刷新", "2026-07-02"),
    ("稼先社区", "社区帖子", "离线", 261919, "一次性采集", "2026-05-27"),
    ("PDMC+", "流程", "离线", 22267, "一次性采集", "2026-06-24"),
    ("华为案例", "案例", "离线", 62438, "一次性采集", "2026-03-04"),
    ("2012Labs", "突击队等", "离线", 16862, "一次性采集", "2026-06-22"),
    ("Whatsell", "营销/文档", "离线", 6357, "一次性采集", "2026-06-15"),
    ("Wiki", "知识库", "在线", 60642, "天级刷新", "2026-07-02"),
]

KNOWLEDGE_GROUPS = [
    ("ICT网络技术", 5019836),
    ("ICT运维服务", 5568),
    ("服务业务架构设计", 128593),
]

FAILURES = [
    ("【解析】其他", 1648),
    ("【采集】数据异常，内容为空", 622),
    ("【解析】文件转化失败", 316),
    ("【解析】入库失败需补偿", 307),
    ("【解析】文件无法读取", 197),
    ("【解析】解析后内容为空", 72),
    ("【解析】任务超时", 24),
    ("【解析】文件解压缩失败", 11),
    ("【解析】内置文件为空", 11),
    ("【解析】解析超时", 9),
    ("【解析】jsonl不存在", 5),
    ("【解析】S3文件下载失败", 2),
]

SEARCH_APPS = [
    ("服务智能体体验中心", 424386),
    ("Webot智能问答", 82568),
    ("知识一张网应用侧", 1701),
]

SEARCH_HITS = [
    ("ICT网络技术", 5019836),
    ("服务架构设计", 128593),
    ("政企服务业务管理", 95842),
    ("咨询", 13283),
    ("平台与支撑业务", 5801),
    ("ICT运维服务", 5568),
    ("数据治理与分析", 1899),
    ("交付项目管理", 1458),
    ("能力发展服务", 1202),
]

MAAS = [
    ("S007555", "Qwen-S-pro", 117480718, 55128),
    ("S007555", "GTSLLM-Pro-Moe", 473694, 73),
    ("S007555", "GTSLLM-Lite-Moe", 84653, 209),
    ("S007555", "Pangu-S-pocket", 15381, 32),
    ("S02638", "Qwen-S-pro", 120319475, 55223),
    ("S02638", "DeepSeek-R1", 92124259, 34119),
    ("S02638", "GTSLLM-Pro-Moe", 8792699, 2797),
    ("S02638", "GTSLLM-VL-Standard", 6099178, 2429),
    ("S02638", "GTSLLM-Lite-Moe", 152470, 60),
]


def fmt(n):
    if n >= 1e8:
        return f"{n/1e8:.2f}亿"
    if n >= 1e4:
        return f"{n/1e4:.1f}万"
    return f"{n:,}"


def donut_svg(items, size=220, cx=None, cy=None, r=80, ir=50):
    cx = cx or size // 2
    cy = cy or size // 2
    total = sum(v for _, v in items) or 1
    paths, legends = [], []
    angle = -90
    for i, (label, val) in enumerate(items):
        pct = val / total
        sweep = pct * 360
        if sweep <= 0:
            continue
        a1, a2 = math.radians(angle), math.radians(angle + sweep)
        x1o, y1o = cx + r * math.cos(a1), cy + r * math.sin(a1)
        x2o, y2o = cx + r * math.cos(a2), cy + r * math.sin(a2)
        x1i, y1i = cx + ir * math.cos(a2), cy + ir * math.sin(a2)
        x2i, y2i = cx + ir * math.cos(a1), cy + ir * math.sin(a1)
        large = 1 if sweep > 180 else 0
        color = COLORS[i % len(COLORS)]
        paths.append(
            f'<path d="M{x1o:.1f},{y1o:.1f} A{r},{r} 0 {large},1 {x2o:.1f},{y2o:.1f} '
            f'L{x1i:.1f},{y1i:.1f} A{ir},{ir} 0 {large},0 {x2i:.1f},{y2i:.1f}Z" '
            f'fill="{color}" stroke="#1e293b" stroke-width="2"><title>{label}: {fmt(val)} ({pct*100:.1f}%)</title></path>'
        )
        legends.append(
            f'<div class="legend-item"><span class="legend-dot" style="background:{color}"></span>'
            f'<span class="legend-label">{label}</span><span class="legend-val">{pct*100:.1f}%</span></div>'
        )
        angle += sweep
    svg = (
        f'<div class="donut-wrap"><svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
        + "".join(paths) + "</svg>"
        f'<div class="donut-legend">{"".join(legends)}</div></div>'
    )
    return svg


def hbar_chart(items, max_label_len=14):
    mx = max(v for _, v in items) or 1
    rows = []
    for i, (label, val) in enumerate(items):
        w = val / mx * 100
        color = COLORS[i % len(COLORS)]
        short = label if len(label) <= max_label_len else label[:max_label_len - 1] + "…"
        rows.append(
            f'<div class="hbar-row"><div class="hbar-label" title="{label}">{short}</div>'
            f'<div class="hbar-track"><div class="hbar-fill" style="width:{w:.1f}%;background:{color}"></div></div>'
            f'<div class="hbar-val">{fmt(val)}</div></div>'
        )
    return '<div class="hbar-chart">' + "".join(rows) + "</div>"


def vbar_chart(items):
    mx = max(v for _, v in items) or 1
    bars = []
    for i, (label, val) in enumerate(items):
        h = val / mx * 100
        color = COLORS[i % len(COLORS)]
        short = label if len(label) <= 8 else label[:7] + "…"
        bars.append(
            f'<div class="vbar-item"><div class="vbar-bar-wrap">'
            f'<div class="vbar-bar" style="height:{h:.1f}%;background:{color}" title="{label}: {fmt(val)}"></div></div>'
            f'<div class="vbar-label">{short}</div><div class="vbar-val">{fmt(val)}</div></div>'
        )
    return '<div class="vbar-chart">' + "".join(bars) + "</div>"


def progress_bars(items):
    mx = items[0][1] if items else 1
    rows = []
    for i, (label, val) in enumerate(items):
        w = val / mx * 100
        color = COLORS[i % len(COLORS)]
        rows.append(
            f'<div class="progress-row"><div class="progress-label" title="{label}">{label}</div>'
            f'<div class="progress-track"><div class="progress-fill" style="width:{w:.1f}%;background:{color}"></div></div>'
            f'<div class="progress-val">{val:,}</div></div>'
        )
    return "".join(rows)


def table_rows(rows, cols):
    out = []
    for row in rows:
        tds = []
        for j, cell in enumerate(row):
            cls = ' class="num highlight"' if cols[j] == "num" else (' class="num"' if cols[j] == "num_plain" else "")
            val = f"{cell:,}" if isinstance(cell, int) else cell
            tds.append(f"<td{cls}>{val}</td>")
        out.append("<tr>" + "".join(tds) + "</tr>")
    return "\n".join(out)


# aggregate data sources
src_agg = {}
for s, *_ , cnt, __, ___ in DATA_SOURCES:
    src_agg[s] = src_agg.get(s, 0) + cnt
src_items = sorted(src_agg.items(), key=lambda x: -x[1])

model_agg = {}
for _, m, t, _ in MAAS:
    model_agg[m] = model_agg.get(m, 0) + t
model_items = sorted(model_agg.items(), key=lambda x: -x[1])

app_agg = {}
for a, _, t, _ in MAAS:
    app_agg[a] = app_agg.get(a, 0) + t
app_items = sorted(app_agg.items(), key=lambda x: -x[1])

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>知识底座运维运营周报看板 | 2026-06-29 ~ 2026-07-05</title>
<style>
:root {{
  --bg:#0f172a;--surface:#1e293b;--surface-2:#334155;--border:#475569;
  --text:#f1f5f9;--muted:#94a3b8;--primary:#3b82f6;--success:#22c55e;
  --warning:#f59e0b;--danger:#ef4444;--purple:#a855f7;--cyan:#06b6d4;
}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;background:var(--bg);color:var(--text);line-height:1.6}}
.dashboard{{max-width:1600px;margin:0 auto;padding:24px}}
.header{{background:linear-gradient(135deg,#1e3a5f,#1e293b 50%,#312e81);border-radius:16px;padding:32px 40px;margin-bottom:24px;border:1px solid var(--border);position:relative;overflow:hidden}}
.header::before{{content:'';position:absolute;top:-50%;right:-10%;width:400px;height:400px;background:radial-gradient(circle,rgba(59,130,246,.15),transparent 70%)}}
.header-top{{display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px;position:relative}}
.header h1{{font-size:1.75rem;font-weight:600}}
.header-sub{{margin-top:8px;color:var(--muted);font-size:.95rem}}
.badge{{background:rgba(59,130,246,.2);border:1px solid rgba(59,130,246,.4);color:#93c5fd;padding:6px 14px;border-radius:20px;font-size:.85rem}}
.nav-tabs{{display:flex;gap:8px;margin-bottom:24px;flex-wrap:wrap;position:sticky;top:0;z-index:100;background:var(--bg);padding:12px 0;border-bottom:1px solid var(--border)}}
.nav-tab{{padding:8px 18px;border-radius:8px;background:var(--surface);border:1px solid var(--border);color:var(--muted);font-size:.875rem;text-decoration:none;transition:.2s}}
.nav-tab:hover,.nav-tab.active{{background:var(--primary);border-color:var(--primary);color:#fff}}
.kpi-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px}}
.kpi-card{{background:var(--surface);border-radius:12px;padding:20px 24px;border:1px solid var(--border);position:relative;overflow:hidden}}
.kpi-card::after{{content:'';position:absolute;top:0;left:0;right:0;height:3px}}
.kpi-card.blue::after{{background:var(--primary)}}.kpi-card.green::after{{background:var(--success)}}
.kpi-card.orange::after{{background:var(--warning)}}.kpi-card.purple::after{{background:var(--purple)}}
.kpi-label{{font-size:.8rem;color:var(--muted);letter-spacing:.05em;margin-bottom:8px}}
.kpi-value{{font-size:1.75rem;font-weight:700}}
.kpi-card.blue .kpi-value{{color:#60a5fa}}.kpi-card.green .kpi-value{{color:#4ade80}}
.kpi-card.orange .kpi-value{{color:#fbbf24}}.kpi-card.purple .kpi-value{{color:#c084fc}}
.kpi-sub{{font-size:.8rem;color:var(--muted);margin-top:6px}}
.up{{color:var(--success)}}.down{{color:var(--danger)}}
.section{{margin-bottom:32px}}
.section-title{{font-size:1.15rem;font-weight:600;margin-bottom:16px;padding-left:12px;border-left:4px solid var(--primary);display:flex;align-items:center;gap:8px}}
.section-num{{background:var(--primary);color:#fff;width:24px;height:24px;border-radius:6px;display:inline-flex;align-items:center;justify-content:center;font-size:.75rem;font-weight:700}}
.grid-2{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.card{{background:var(--surface);border-radius:12px;padding:20px;border:1px solid var(--border)}}
.card-title{{font-size:.9rem;font-weight:600;color:var(--muted);margin-bottom:16px;text-align:center}}
.table-wrap{{overflow-x:auto;border-radius:8px}}
table{{width:100%;border-collapse:collapse;font-size:.85rem}}
th{{background:var(--surface-2);color:var(--muted);font-weight:600;text-align:left;padding:10px 14px;white-space:nowrap}}
td{{padding:9px 14px;border-bottom:1px solid rgba(71,85,105,.5)}}
tr:hover td{{background:rgba(59,130,246,.05)}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}
.highlight{{color:#60a5fa;font-weight:600}}
.sla-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:16px}}
.sla-item{{text-align:center;padding:16px;background:var(--surface-2);border-radius:10px}}
.sla-num{{font-size:2rem;font-weight:700}}
.sla-num.success{{color:var(--success)}}.sla-num.info{{color:var(--cyan)}}.sla-num.warn{{color:var(--warning)}}
.sla-desc{{font-size:.8rem;color:var(--muted);margin-top:4px}}
.meter-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}}
.meter{{background:var(--surface-2);border-radius:10px;padding:14px}}
.meter-title{{font-size:.8rem;color:var(--muted);margin-bottom:8px}}
.meter-bar{{height:12px;background:rgba(0,0,0,.3);border-radius:6px;overflow:hidden;margin-bottom:6px}}
.meter-fill{{height:100%;border-radius:6px}}
.meter-stats{{display:flex;justify-content:space-between;font-size:.75rem;color:var(--muted)}}
.progress-row{{display:flex;align-items:center;gap:12px;margin-bottom:10px}}
.progress-label{{width:180px;font-size:.8rem;color:var(--muted);flex-shrink:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.progress-track{{flex:1;height:8px;background:var(--surface-2);border-radius:4px;overflow:hidden}}
.progress-fill{{height:100%;border-radius:4px}}
.progress-val{{width:60px;text-align:right;font-size:.8rem;flex-shrink:0}}
.donut-wrap{{display:flex;align-items:center;justify-content:center;gap:20px;flex-wrap:wrap;padding:8px}}
.donut-legend{{display:flex;flex-direction:column;gap:6px;font-size:.78rem}}
.legend-item{{display:flex;align-items:center;gap:8px}}
.legend-dot{{width:10px;height:10px;border-radius:2px;flex-shrink:0}}
.legend-label{{color:var(--muted);flex:1}}
.legend-val{{color:var(--text);font-weight:600}}
.hbar-chart{{padding:8px 0}}
.hbar-row{{display:flex;align-items:center;gap:10px;margin-bottom:10px}}
.hbar-label{{width:130px;font-size:.8rem;color:var(--muted);flex-shrink:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.hbar-track{{flex:1;height:22px;background:var(--surface-2);border-radius:4px;overflow:hidden}}
.hbar-fill{{height:100%;border-radius:4px;transition:width .6s ease}}
.hbar-val{{width:70px;text-align:right;font-size:.78rem;font-weight:600;flex-shrink:0}}
.vbar-chart{{display:flex;align-items:flex-end;justify-content:space-around;height:220px;padding:0 8px;gap:8px}}
.vbar-item{{display:flex;flex-direction:column;align-items:center;flex:1;max-width:120px;height:100%}}
.vbar-bar-wrap{{flex:1;width:100%;display:flex;align-items:flex-end;justify-content:center}}
.vbar-bar{{width:70%;max-width:60px;border-radius:6px 6px 0 0;min-height:4px;transition:height .6s ease}}
.vbar-label{{font-size:.7rem;color:var(--muted);margin-top:8px;text-align:center;line-height:1.2}}
.vbar-val{{font-size:.72rem;font-weight:600;margin-top:4px;color:var(--text)}}
.rank-list{{padding:8px}}
.rank-item{{display:flex;align-items:center;gap:14px;padding:14px 12px;margin-bottom:10px;background:var(--surface-2);border-radius:10px}}
.rank-badge{{width:36px;height:36px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:1rem;flex-shrink:0}}
.rank-badge.gold{{background:linear-gradient(135deg,#fbbf24,#f59e0b);color:#1e293b}}
.rank-badge.silver{{background:linear-gradient(135deg,#94a3b8,#64748b);color:#1e293b}}
.rank-badge.bronze{{background:linear-gradient(135deg,#cd7f32,#a0522d);color:#fff}}
.rank-name{{font-size:1rem;font-weight:600;flex:1}}
.rank-bar-wrap{{flex:1;max-width:200px}}
.rank-bar{{height:8px;background:var(--surface);border-radius:4px;overflow:hidden;margin-top:4px}}
.rank-bar-fill{{height:100%;border-radius:4px;background:var(--primary)}}
.action-list{{display:flex;flex-direction:column;gap:12px}}
.action-item{{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:16px 20px;display:flex;gap:16px;align-items:flex-start}}
.action-icon{{width:36px;height:36px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1.1rem;flex-shrink:0}}
.action-icon.warn{{background:rgba(245,158,11,.2)}}.action-icon.info{{background:rgba(59,130,246,.2)}}.action-icon.danger{{background:rgba(239,68,68,.2)}}
.action-content h4{{font-size:.9rem;margin-bottom:4px}}.action-content p{{font-size:.82rem;color:var(--muted)}}
.action-meta{{margin-left:auto;text-align:right;flex-shrink:0}}
.action-owner{{font-size:.8rem;color:#93c5fd}}.action-deadline{{font-size:.75rem;color:var(--warning);margin-top:2px}}
.contacts-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}
.contact-card{{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:14px;text-align:center}}
.contact-role{{font-size:.75rem;color:var(--muted);margin-bottom:4px}}
.contact-name{{font-size:.9rem;font-weight:600;color:#93c5fd}}
.contact-id{{font-size:.75rem;color:var(--muted);margin-top:2px}}
.footer{{text-align:center;padding:24px;color:var(--muted);font-size:.8rem;border-top:1px solid var(--border);margin-top:16px}}
.tip-banner{{background:rgba(59,130,246,.15);border:1px solid rgba(59,130,246,.3);border-radius:10px;padding:12px 20px;margin-bottom:20px;font-size:.85rem;color:#93c5fd;display:flex;align-items:center;gap:10px}}
.tip-banner button{{margin-left:auto;background:var(--primary);color:#fff;border:none;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:.8rem}}
@media(max-width:1200px){{.kpi-grid,.grid-2,.contacts-grid{{grid-template-columns:1fr 1fr}}}}
@media(max-width:640px){{.kpi-grid,.grid-2,.sla-grid,.contacts-grid{{grid-template-columns:1fr}}.dashboard{{padding:12px}}}}
</style>
</head>
<body>
<div class="dashboard">
<div class="tip-banner" id="tip">📎 离线版看板 · 无需联网 · 双击本文件即可查看完整图表 <button onclick="this.parentElement.style.display='none'">知道了</button></div>

<div class="header">
  <div class="header-top">
    <div><h1>知识底座运维运营周报看板</h1><p class="header-sub">编制：知识底座运维组</p></div>
    <div style="display:flex;gap:12px;flex-wrap:wrap">
      <span class="badge">📅 2026-06-29 ~ 2026-07-05</span>
      <span class="badge">📊 第27周</span>
    </div>
  </div>
</div>

<nav class="nav-tabs">
  <a class="nav-tab active" href="#summary">本周摘要</a>
  <a class="nav-tab" href="#knowledge-base">底座知识库</a>
  <a class="nav-tab" href="#pipeline">知识产线</a>
  <a class="nav-tab" href="#search">知识搜索服务</a>
  <a class="nav-tab" href="#maas">GTS MaaS</a>
  <a class="nav-tab" href="#actions">问题与改进</a>
</nav>

<section id="summary" class="section">
<div class="kpi-grid">
  <div class="kpi-card blue"><div class="kpi-label">知识库语料总量</div><div class="kpi-value">412.5万</div><div class="kpi-sub">本周新增 <span class="up">+169,285</span> · 日落 <span class="down">-32,575</span></div></div>
  <div class="kpi-card green"><div class="kpi-label">语料入网成功率</div><div class="kpi-value">99.63%</div><div class="kpi-sub">平均 SLA <span style="color:#fbbf24">31 min/篇</span> · 入网 106,261 篇</div></div>
  <div class="kpi-card orange"><div class="kpi-label">搜索服务调用次数</div><div class="kpi-value">51.8万</div><div class="kpi-sub">较上周 <span class="down">-144,020</span> · 峰值 QPS <span class="up">43</span></div></div>
  <div class="kpi-card purple"><div class="kpi-label">模型 Token 消耗总量</div><div class="kpi-value">2.96亿</div><div class="kpi-sub">主力模型 Qwen-S-pro · 调用 48,470 次</div></div>
</div>
</section>

<section id="knowledge-base" class="section">
<div class="section-title"><span class="section-num">二</span>底座知识库</div>
<div class="grid-2">
  <div class="card">
    <div class="card-title">本周语料 Top3 知识组</div>
    <div class="rank-list">
      <div class="rank-item"><div class="rank-badge gold">1</div><div><div class="rank-name">ICT网络技术</div><div class="rank-bar"><div class="rank-bar-fill" style="width:100%"></div></div></div></div>
      <div class="rank-item"><div class="rank-badge silver">2</div><div><div class="rank-name">ICT运维服务</div><div class="rank-bar"><div class="rank-bar-fill" style="width:45%"></div></div></div></div>
      <div class="rank-item"><div class="rank-badge bronze">3</div><div><div class="rank-name">服务业务架构设计</div><div class="rank-bar"><div class="rank-bar-fill" style="width:35%"></div></div></div></div>
    </div>
  </div>
  <div class="card">
    <div class="card-title">语料入库概览（按数据源）</div>
    {donut_svg(src_items, size=200, r=70, ir=42)}
  </div>
</div>
<div class="card" style="margin-top:16px">
  <div class="card-title" style="text-align:left">入库语料明细表</div>
  <div class="table-wrap"><table>
    <thead><tr><th>数据源</th><th>板块</th><th>在线/离线</th><th class="num">数据量（篇）</th><th>更新周期</th><th>库内最新数据日期</th></tr></thead>
    <tbody>{table_rows([(a,b,c,d,e,f) for a,b,c,d,e,f in DATA_SOURCES], ["text","text","text","num","text","text"])}</tbody>
  </table></div>
</div>
</section>

<section id="pipeline" class="section">
<div class="section-title"><span class="section-num">三</span>知识产线</div>
<div class="sla-grid">
  <div class="sla-item"><div class="sla-num info">106,261</div><div class="sla-desc">本周语料入网总量（篇）</div></div>
  <div class="sla-item"><div class="sla-num success">99.63%</div><div class="sla-desc">语料解析成功率</div></div>
  <div class="sla-item"><div class="sla-num warn">31 min</div><div class="sla-desc">语料入网平均 SLA / 篇</div></div>
</div>
<div class="grid-2">
  <div class="card">
    <div class="card-title">语料入网失败原因分布（387 篇 · 3,224 文件）</div>
    {donut_svg(FAILURES[:6], size=200, r=70, ir=42)}
  </div>
  <div class="card">
    <div class="card-title">失败原因明细</div>
    {progress_bars(FAILURES)}
  </div>
</div>
<div class="card" style="margin-top:16px">
  <div class="card-title" style="text-align:left">MongoDB 资源利用率</div>
  <div class="meter-grid">
    <div class="meter"><div class="meter-title">CPU 使用率</div><div class="meter-bar"><div class="meter-fill" style="width:23.26%;background:#3b82f6"></div></div><div class="meter-stats"><span>23.26%</span></div></div>
    <div class="meter"><div class="meter-title">内存使用率</div><div class="meter-bar"><div class="meter-fill" style="width:85.5%;background:#f59e0b"></div></div><div class="meter-stats"><span>85.5%</span></div></div>
    <div class="meter" style="grid-column:span 2"><div class="meter-title">存储使用率</div><div class="meter-bar"><div class="meter-fill" style="width:83.28%;background:#ef4444"></div></div><div class="meter-stats"><span>83.28%</span><span style="color:#fbbf24">分片存储不均衡</span></div></div>
  </div>
</div>
</section>

<section id="search" class="section">
<div class="section-title"><span class="section-num">四</span>知识搜索服务</div>
<div class="kpi-grid" style="grid-template-columns:repeat(3,1fr);margin-bottom:16px">
  <div class="kpi-card blue"><div class="kpi-label">搜索消费语料</div><div class="kpi-value" style="font-size:1.4rem">762,115 篇</div><div class="kpi-sub">占知识库总量 <span class="up">18.44%</span></div></div>
  <div class="kpi-card orange"><div class="kpi-label">零消费语料占比</div><div class="kpi-value" style="font-size:1.4rem;color:#fbbf24">33.9%</div><div class="kpi-sub">需专项分析语料价值</div></div>
  <div class="kpi-card green"><div class="kpi-label">MySQL 存储使用率</div><div class="kpi-value" style="font-size:1.4rem;color:#ef4444">84.05%</div><div class="kpi-sub">已超 80% 告警阈值 · CPU 2.27%</div></div>
</div>
<div class="grid-2">
  <div class="card"><div class="card-title">调用搜索服务 Top 应用</div>{vbar_chart(SEARCH_APPS)}</div>
  <div class="card"><div class="card-title">知识组搜索命中 Top 9</div>{hbar_chart(SEARCH_HITS)}</div>
</div>
<div class="grid-2" style="margin-top:16px">
  <div class="card">
    <div class="card-title">EC2 主机资源利用率</div>
    <div class="table-wrap"><table>
      <thead><tr><th>主机名称</th><th class="num">CPU 峰值</th><th class="num">CPU P95</th><th class="num">内存峰值</th><th class="num">内存 P95</th></tr></thead>
      <tbody>
        <tr><td>kwephis41482604</td><td class="num highlight">18.70%</td><td class="num">2.36%</td><td class="num">39.60%</td><td class="num">38.90%</td></tr>
        <tr><td>kwephis41482609</td><td class="num">17.20%</td><td class="num">1.63%</td><td class="num">34.40%</td><td class="num">33.80%</td></tr>
        <tr><td>kwephis41482613</td><td class="num">13.30%</td><td class="num">1.27%</td><td class="num">29.90%</td><td class="num">28.80%</td></tr>
        <tr><td>kwephis41482598</td><td class="num">11.10%</td><td class="num">1.30%</td><td class="num">33.60%</td><td class="num">31.50%</td></tr>
      </tbody>
    </table></div>
    <div class="meter-grid" style="margin-top:16px">
      <div class="meter"><div class="meter-title">EC2 CPU 平均 / 峰值</div><div class="meter-bar"><div class="meter-fill" style="width:1.64%;background:#3b82f6"></div></div><div class="meter-stats"><span>平均 1.64%</span><span>峰值 18.7%</span></div></div>
      <div class="meter"><div class="meter-title">EC2 内存平均 / 峰值</div><div class="meter-bar"><div class="meter-fill" style="width:33%;background:#22c55e"></div></div><div class="meter-stats"><span>平均 33%</span><span>峰值 39.60%</span></div></div>
    </div>
  </div>
  <div class="card">
    <div class="card-title">CSS / MySQL 资源概览</div>
    <div class="meter-grid">
      <div class="meter"><div class="meter-title">CSS CPU</div><div class="meter-bar"><div class="meter-fill" style="width:30%;background:#f59e0b"></div></div><div class="meter-stats"><span>30%</span></div></div>
      <div class="meter"><div class="meter-title">CSS 内存</div><div class="meter-bar"><div class="meter-fill" style="width:48%;background:#a855f7"></div></div><div class="meter-stats"><span>48%</span></div></div>
      <div class="meter"><div class="meter-title">CSS 存储（27TB）</div><div class="meter-bar"><div class="meter-fill" style="width:74%;background:#ef4444"></div></div><div class="meter-stats"><span>74%</span></div></div>
      <div class="meter"><div class="meter-title">MySQL 存储</div><div class="meter-bar"><div class="meter-fill" style="width:84.05%;background:#ef4444"></div></div><div class="meter-stats"><span>84.05%</span><span style="color:#fbbf24">已告警</span></div></div>
      <div class="meter" style="grid-column:span 2"><div class="meter-title">MySQL CPU / 内存</div><div class="meter-bar"><div class="meter-fill" style="width:70.5%;background:#06b6d4"></div></div><div class="meter-stats"><span>CPU 2.27%</span><span>内存 70.5%</span></div></div>
    </div>
  </div>
</div>
</section>

<section id="maas" class="section">
<div class="section-title"><span class="section-num">五</span>GTS MaaS 大模型服务</div>
<div class="grid-2">
  <div class="card"><div class="card-title">各模型 Token 消耗分布</div>{donut_svg(model_items, size=200, r=70, ir=42)}</div>
  <div class="card"><div class="card-title">各 APPID Token 消耗</div>{vbar_chart(app_items)}</div>
</div>
<div class="card" style="margin-top:16px">
  <div class="card-title" style="text-align:left">模型调用明细表</div>
  <div class="table-wrap"><table>
    <thead><tr><th>APPID</th><th>模型</th><th class="num">消耗 Token</th><th class="num">调用次数</th></tr></thead>
    <tbody>{table_rows(MAAS, ["text","text","num","num_plain"])}</tbody>
  </table></div>
</div>
</section>

<section id="actions" class="section">
<div class="section-title"><span class="section-num">六</span>问题与改进</div>
<div class="action-list">
  <div class="action-item"><div class="action-icon warn">⚠️</div><div class="action-content"><h4>【解析】其他失败原因占比过大</h4><p>失败原因不明，占比较大（1,648 次）。需解析组优化解析结果返回，给出修复计划。</p></div><div class="action-meta"><div class="action-owner">尹林枫</div><div class="action-deadline">截止：7月30日前</div></div></div>
  <div class="action-item"><div class="action-icon danger">🗄️</div><div class="action-content"><h4>MySQL 资源存储超过 80%，已告警</h4><p>存储使用率达 84.05%。需清理日志表历史数据，后续考虑将日志存储迁移到 ES。</p></div><div class="action-meta"><div class="action-owner">郭嘉伦</div><div class="action-deadline">截止：7月30日</div></div></div>
  <div class="action-item"><div class="action-icon info">📦</div><div class="action-content"><h4>MongoDB 资源存储不均衡</h4><p>存储使用率 83.28%，各节点分片存储不均衡。需处理分片均衡问题。</p></div><div class="action-meta"><div class="action-owner">王梁</div><div class="action-deadline">截止：7月15日</div></div></div>
  <div class="action-item"><div class="action-icon danger">📊</div><div class="action-content"><h4>零消费语料占比过高（33.9%）</h4><p>需捞出具体数据专项分析语料价值，优化知识库质量。</p></div><div class="action-meta"><div class="action-owner">吴亦章</div><div class="action-deadline">截止：7月30日前</div></div></div>
</div>
<div style="margin-top:24px">
  <div class="section-title" style="font-size:1rem;border-left-color:#a855f7">运维运营团队接口人</div>
  <div class="contacts-grid">
    <div class="contact-card"><div class="contact-role">知识产线 & 语料入网</div><div class="contact-name">唐熊</div><div class="contact-id">60049465</div></div>
    <div class="contact-card"><div class="contact-role">知识搜索 & 底座知识库</div><div class="contact-name">郭嘉伦</div><div class="contact-id">30060574</div></div>
    <div class="contact-card"><div class="contact-role">资源使用率</div><div class="contact-name">王梁</div><div class="contact-id">60086520</div></div>
    <div class="contact-card"><div class="contact-role">GTS LLM 模型</div><div class="contact-name">常宏</div><div class="contact-id">30056551</div></div>
  </div>
</div>
</section>

<div class="footer">知识底座运维运营周报看板 · 数据周期 2026-06-29 ~ 2026-07-05 · 编制：知识底座运维组 · 离线版</div>
</div>
<script>
document.querySelectorAll('.nav-tab').forEach(tab=>{{
  tab.addEventListener('click',e=>{{
    e.preventDefault();
    document.querySelector(tab.getAttribute('href'))?.scrollIntoView({{behavior:'smooth'}});
  }});
}});
window.addEventListener('scroll',()=>{{
  let cur='';
  document.querySelectorAll('.section').forEach(s=>{{if(window.scrollY>=s.offsetTop-120)cur=s.id}});
  document.querySelectorAll('.nav-tab').forEach(t=>t.classList.toggle('active',t.getAttribute('href')==='#'+cur));
}});
</script>
</body>
</html>"""

OUTPUT.write_text(html, encoding="utf-8")
print(f"Generated {OUTPUT} ({OUTPUT.stat().st_size:,} bytes)")
