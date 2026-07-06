#!/usr/bin/env python3
"""将看板导出为 PDF，可作为邮件附件（无需联网即可查看静态版）"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
HTML_PATH = ROOT / "knowledge-ops-dashboard.html"
PDF_PATH = ROOT / "weekly-report.pdf"


def export_pdf():
    if not HTML_PATH.exists():
        print(f"❌ 找不到看板文件: {HTML_PATH}")
        sys.exit(1)

    html_url = HTML_PATH.resolve().as_uri()
    script = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const browser = await chromium.launch();
  const page = await browser.newPage({{ viewport: {{ width: 1400, height: 900 }} }});
  await page.goto('{html_url}', {{ waitUntil: 'networkidle', timeout: 60000 }});
  await page.waitForTimeout(3000);
  await page.pdf({{
    path: '{PDF_PATH.resolve()}',
    format: 'A3',
    landscape: true,
    printBackground: true,
    margin: {{ top: '10mm', bottom: '10mm', left: '10mm', right: '10mm' }}
  }});
  await browser.close();
  console.log('PDF exported');
}})();
"""
  tmp = ROOT / ".export-pdf.mjs"
  tmp.write_text(script, encoding="utf-8")
  try:
    subprocess.run(["npx", "--yes", "playwright", "install", "chromium"], check=True, cwd=ROOT)
    subprocess.run(["node", str(tmp)], check=True, cwd=ROOT)
    print(f"✅ PDF 已导出: {PDF_PATH}")
  finally:
    tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    export_pdf()
