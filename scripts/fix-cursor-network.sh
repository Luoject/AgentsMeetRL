#!/usr/bin/env bash
# Cursor 网络修复脚本 (macOS / Linux)
# 用法: bash scripts/fix-cursor-network.sh

set -euo pipefail

echo "=== Cursor 网络诊断与修复 ==="

echo ""
echo "--- 1. 当前 DNS 解析 api2.cursor.sh ---"
if command -v dig >/dev/null 2>&1; then
  IPS=$(dig +short api2.cursor.sh A | grep -E '^[0-9.]+$' | tr '\n' ' ')
  echo "解析结果: ${IPS:-无}"
  COUNT=$(echo "$IPS" | wc -w | tr -d ' ')
  if [ "${COUNT:-0}" -lt 2 ]; then
    echo "警告: 仅解析到单个 IP，可能存在 DNS 污染"
  fi
else
  nslookup api2.cursor.sh || true
fi

echo ""
echo "--- 2. 连通性测试 ---"
curl -sS --connect-timeout 10 -o /dev/null -w "api2.cursor.sh: HTTP %{http_code} (%{time_total}s)\n" https://api2.cursor.sh || echo "api2.cursor.sh: 连接失败"

echo ""
echo "--- 3. 流式连接测试 (Chat/Agent) ---"
if echo -ne '\x0\x0\x0\x0\x11{"payload":"foo"}' | curl --http1.1 -No - -XPOST \
  -H "Content-Type: application/connect+json" \
  --data-binary @- \
  --connect-timeout 10 -m 15 \
  https://api2.cursor.sh/aiserver.v1.HealthService/StreamSSE 2>/dev/null | grep -q payload; then
  echo "[OK] SSE 流式连接正常"
else
  echo "[FAIL] SSE 流式连接失败，请检查代理/VPN/防火墙"
fi

echo ""
echo "--- 4. 写入 Cursor 用户设置 ---"
SETTINGS_PATHS=(
  "$HOME/Library/Application Support/Cursor/User/settings.json"
  "$HOME/.config/Cursor/User/settings.json"
)
PATCHED=0
for SETTINGS in "${SETTINGS_PATHS[@]}"; do
  if [ ! -d "$(dirname "$SETTINGS")" ]; then
    continue
  fi
  mkdir -p "$(dirname "$SETTINGS")"
  if [ ! -f "$SETTINGS" ]; then
    printf '{\n  "cursor.general.disableHttp2": true\n}\n' >"$SETTINGS"
    echo "[OK] 已创建 $SETTINGS"
    PATCHED=1
    break
  fi
  if python3 - "$SETTINGS" <<'PY'
import json, sys
path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    data = json.load(f)
data["cursor.general.disableHttp2"] = True
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")
PY
  then
    echo "[OK] 已更新 $SETTINGS"
    PATCHED=1
    break
  fi
done
if [ "$PATCHED" -eq 0 ]; then
  echo "未能自动写入设置，请手动添加: \"cursor.general.disableHttp2\": true"
fi

echo ""
echo "--- 5. DNS 修复提示 ---"
if [[ "$(uname)" == "Darwin" ]]; then
  echo "macOS: 系统设置 -> 网络 -> 你的连接 -> 详细信息 -> DNS"
  echo "删除 7.192.144.x 等自定义 DNS，添加 8.8.8.8 和 8.8.4.4"
  echo "然后运行: sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder"
elif [ -f /etc/resolv.conf ]; then
  echo "Linux: 请将 /etc/resolv.conf 中的 nameserver 改为 8.8.8.8 和 8.8.4.4"
  echo "或使用 NetworkManager: nmcli con mod <连接名> ipv4.dns '8.8.8.8 8.8.4.4'"
fi

echo ""
echo "--- 6. 后续步骤 ---"
echo "1. 完全退出并重启 Cursor"
echo "2. 暂时关闭 VPN/代理后重试"
echo "3. Cursor Settings -> Network -> Run Diagnostics"
echo ""
echo "完成。"
