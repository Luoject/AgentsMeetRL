#!/usr/bin/env bash
# Cursor 网络修复脚本 (macOS / Linux) v2
# 用法: bash scripts/fix-cursor-network.sh

set -uo pipefail

echo "=== Cursor 网络诊断与修复 v2 ==="
echo "症状: ENOTFOUND = DNS 完全失效"
echo ""

test_dns() {
  local server="$1"
  local host="${2:-api2.cursor.sh}"
  if [ "$server" = "system" ]; then
    dig +short "$host" A 2>/dev/null | grep -E '^[0-9.]+$' | head -1
  else
    dig @"$server" +short "$host" A 2>/dev/null | grep -E '^[0-9.]+$' | head -1
  fi
}

echo "--- 1. 测试各 DNS 服务器 ---"
declare -a DNS_NAMES=("自动(system)" "阿里(223.5.5.5)" "腾讯(119.29.29.29)" "Cloudflare(1.1.1.1)" "Google(8.8.8.8)")
declare -a DNS_SERVERS=("system" "223.5.5.5" "119.29.29.29" "1.1.1.1" "8.8.8.8")
WORKING_DNS=""
for i in "${!DNS_SERVERS[@]}"; do
  ip=$(test_dns "${DNS_SERVERS[$i]}")
  if [ -n "$ip" ]; then
    echo "[OK] ${DNS_NAMES[$i]} -> $ip"
    [ -z "$WORKING_DNS" ] && WORKING_DNS="${DNS_SERVERS[$i]}"
  else
    echo "[FAIL] ${DNS_NAMES[$i]}"
  fi
done

echo ""
echo "--- 2. DNS 修复建议 ---"
if [ -n "$WORKING_DNS" ] && [ "$WORKING_DNS" != "system" ]; then
  echo "建议使用 DNS: $WORKING_DNS"
  if [[ "$(uname)" == "Darwin" ]]; then
    echo "macOS: 系统设置 -> 网络 -> DNS -> 删除 8.8.8.8，添加 $WORKING_DNS"
    echo "刷新缓存: sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder"
  else
    echo "Linux: sudo resolvectl dns \$(resolvectl status | awk '/Current DNS Server/{getline; print \$2; exit}') $WORKING_DNS"
    echo "或: nmcli con mod <连接名> ipv4.dns '$WORKING_DNS'"
  fi
elif [ "$WORKING_DNS" = "system" ]; then
  echo "[OK] 系统 DNS 可用，若 Cursor 仍失败请恢复为自动 DNS（删除手动 8.8.8.8）"
else
  echo "[FAIL] 所有 DNS 失败，尝试 hosts 备用方案"
  HOSTS_FILE="/etc/hosts"
  if [ -w "$HOSTS_FILE" ] || [ "$(id -u)" -eq 0 ]; then
    if ! grep -q "Cursor Network Fix" "$HOSTS_FILE" 2>/dev/null; then
      echo ""
      echo "以 sudo 运行以下命令写入 hosts:"
      echo "  sudo bash -c 'cat scripts/cursor-hosts-snippet.txt >> /etc/hosts'"
    else
      echo "[SKIP] hosts 中已有 Cursor 条目"
    fi
  else
    echo "请运行: sudo bash -c 'cat scripts/cursor-hosts-snippet.txt >> /etc/hosts'"
  fi
fi

echo ""
echo "--- 3. 写入 Cursor 设置 ---"
SETTINGS_PATHS=(
  "$HOME/Library/Application Support/Cursor/User/settings.json"
  "$HOME/.config/Cursor/User/settings.json"
)
for SETTINGS in "${SETTINGS_PATHS[@]}"; do
  [ -d "$(dirname "$SETTINGS")" ] || continue
  mkdir -p "$(dirname "$SETTINGS")"
  if [ ! -f "$SETTINGS" ]; then
    printf '{\n  "cursor.general.disableHttp2": true\n}\n' >"$SETTINGS"
  else
    python3 - "$SETTINGS" <<'PY'
import json, sys
path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    data = json.load(f)
data["cursor.general.disableHttp2"] = True
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")
PY
  fi
  echo "[OK] $SETTINGS"
  break
done

echo ""
echo "--- 4. 验证 ---"
if ip=$(test_dns system); then
  echo "[OK] api2.cursor.sh -> $ip"
else
  echo "[FAIL] 仍无法解析。请关闭 VPN/代理，或用手机热点测试。"
fi

echo ""
echo "完成后完全退出 Cursor 并重新运行 Network Diagnostics。"
