# Cursor 网络修复脚本 (Windows)
# 请以管理员身份运行 PowerShell，然后执行:
#   Set-ExecutionPolicy -Scope Process Bypass; .\scripts\fix-cursor-network.ps1

$ErrorActionPreference = "Stop"

Write-Host "=== Cursor 网络诊断与修复 ===" -ForegroundColor Cyan

function Test-CursorEndpoint {
    param([string]$Name, [string]$Url)
    try {
        $r = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 15
        Write-Host "[OK] $Name : $($r.StatusCode)" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "[FAIL] $Name : $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

Write-Host "`n--- 1. 当前 DNS 解析 api2.cursor.sh ---" -ForegroundColor Yellow
try {
    $dns = Resolve-DnsName api2.cursor.sh -Type A -ErrorAction Stop
    $ips = ($dns | Where-Object { $_.Type -eq "A" }).IPAddress
    Write-Host "解析结果: $($ips -join ', ')"
    if ($ips.Count -lt 2) {
        Write-Host "警告: 仅解析到单个 IP，可能存在 DNS 污染" -ForegroundColor Red
    }
} catch {
    Write-Host "DNS 解析失败: $_" -ForegroundColor Red
}

Write-Host "`n--- 2. 修复 DNS（改为 Google DNS）---" -ForegroundColor Yellow
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "需要管理员权限才能修改 DNS。请右键 PowerShell -> 以管理员身份运行" -ForegroundColor Red
} else {
    $adapters = Get-NetAdapter | Where-Object { $_.Status -eq "Up" }
    foreach ($adapter in $adapters) {
        $alias = $adapter.Name
        try {
            Set-DnsClientServerAddress -InterfaceAlias $alias -ServerAddresses ("8.8.8.8", "8.8.4.4") -ErrorAction Stop
            Write-Host "[OK] 已将 $alias 的 DNS 设为 8.8.8.8 / 8.8.4.4" -ForegroundColor Green
        } catch {
            Write-Host "[SKIP] $alias : $_" -ForegroundColor DarkYellow
        }
    }
    ipconfig /flushdns | Out-Null
    Write-Host "[OK] DNS 缓存已刷新" -ForegroundColor Green
}

Write-Host "`n--- 3. 连通性测试 ---" -ForegroundColor Yellow
Test-CursorEndpoint "api2.cursor.sh" "https://api2.cursor.sh" | Out-Null
Test-CursorEndpoint "authentication" "https://prod.authentication.cursor.sh" | Out-Null

Write-Host "`n--- 4. 写入 Cursor 用户设置 ---" -ForegroundColor Yellow
$settingsPaths = @(
    "$env:APPDATA\Cursor\User\settings.json",
    "$env:LOCALAPPDATA\Cursor\User\settings.json"
)
$networkSettings = @{
    "cursor.general.disableHttp2" = $true
}
$patched = $false
foreach ($path in $settingsPaths) {
    if (-not (Test-Path (Split-Path $path))) { continue }
    if (-not (Test-Path $path)) {
        $dir = Split-Path $path
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
        $json = $networkSettings | ConvertTo-Json -Depth 5
        Set-Content -Path $path -Value $json -Encoding UTF8
        Write-Host "[OK] 已创建 $path" -ForegroundColor Green
        $patched = $true
        break
    }
    try {
        $raw = Get-Content -Path $path -Raw -Encoding UTF8
        $settings = $raw | ConvertFrom-Json
        if ($settings -is [System.Array]) {
            Write-Host "[SKIP] $path 格式异常，请手动添加设置" -ForegroundColor DarkYellow
            continue
        }
        $settings | Add-Member -NotePropertyName "cursor.general.disableHttp2" -NotePropertyValue $true -Force
        $settings | ConvertTo-Json -Depth 10 | Set-Content -Path $path -Encoding UTF8
        Write-Host "[OK] 已更新 $path" -ForegroundColor Green
        $patched = $true
        break
    } catch {
        Write-Host "[SKIP] $path : $_" -ForegroundColor DarkYellow
    }
}
if (-not $patched) {
    Write-Host "未能自动写入设置，请手动在 Cursor 设置 JSON 中添加:" -ForegroundColor Yellow
    Write-Host '  "cursor.general.disableHttp2": true' -ForegroundColor White
}

Write-Host "`n--- 5. 后续步骤 ---" -ForegroundColor Yellow
Write-Host "1. 完全退出 Cursor（托盘图标也要退出）"
Write-Host "2. 若使用 VPN/代理，暂时关闭后重试"
Write-Host "3. 重新打开 Cursor -> Settings -> Network -> Run Diagnostics"
Write-Host "4. 若仍失败，用手机热点测试以排除 ISP 限制"
Write-Host "`n完成。" -ForegroundColor Cyan
