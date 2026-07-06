#!/usr/bin/env python3
"""发送知识底座运维周报邮件（摘要 + 看板链接 + 可选 PDF 附件）"""

import json
import smtplib
import sys
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

ROOT = Path(__file__).parent
CONFIG_PATH = ROOT / "dashboard-config.json"
EMAIL_TEMPLATE_PATH = ROOT / "email-weekly-report.html"
PDF_PATH = ROOT / "weekly-report.pdf"


def load_config() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def build_email_html(config: dict) -> str:
    with open(EMAIL_TEMPLATE_PATH, encoding="utf-8") as f:
        html = f.read()
    url = config.get("dashboardUrl") or config.get("dashboardUrlFallback", "")
    return html.replace("{{DASHBOARD_URL}}", url)


def send_email(config: dict, attach_pdf: bool = False) -> None:
    smtp_cfg = config["smtp"]
    email_cfg = config["email"]
    html_body = build_email_html(config)

    msg = MIMEMultipart("mixed")
    msg["Subject"] = email_cfg["subject"]
    msg["From"] = email_cfg["from"]
    msg["To"] = ", ".join(email_cfg["to"])
    if email_cfg.get("cc"):
        msg["Cc"] = ", ".join(email_cfg["cc"])

    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText("请使用支持 HTML 的邮件客户端查看，或点击链接访问看板：" + config["dashboardUrl"], "plain", "utf-8"))
    alt.attach(MIMEText(html_body, "html", "utf-8"))
    msg.attach(alt)

    if attach_pdf and PDF_PATH.exists():
        with open(PDF_PATH, "rb") as f:
            part = MIMEApplication(f.read(), _subtype="pdf")
            part.add_header("Content-Disposition", "attachment", filename=PDF_PATH.name)
            msg.attach(part)

    recipients = email_cfg["to"] + email_cfg.get("cc", [])

    if smtp_cfg.get("useSsl"):
        server = smtplib.SMTP_SSL(smtp_cfg["host"], smtp_cfg["port"])
    else:
        server = smtplib.SMTP(smtp_cfg["host"], smtp_cfg["port"])
        server.starttls()

    server.login(smtp_cfg["username"], smtp_cfg["password"])
    server.sendmail(email_cfg["from"], recipients, msg.as_string())
    server.quit()
    print(f"✅ 邮件已发送至: {', '.join(recipients)}")


def main():
    attach_pdf = "--pdf" in sys.argv
    config = load_config()
    send_email(config, attach_pdf=attach_pdf)


if __name__ == "__main__":
    main()
