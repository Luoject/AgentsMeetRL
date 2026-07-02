# Cursor 网络修复脚本 (Windows)
# 请以管理员身份运行 PowerShell:
#   Set-ExecutionPolicy -Scope Process Bypass; .\scripts\fix-cursor-network.ps1

$ErrorActionPreference = "Continue"

Write-Host "=== Cursor 网络诊断与修复 v2 ===" -ForegroundColor Cyan
Write-Host "症状: ENOTFOUND / ERR_NAME_NOT_RESOLVED = DNS 完全失效`n" -ForegroundColor Yellow

function Test-DnsResolver {
    param([string]$Server, [string]$HostName = "api2.cursor.sh")
    try {
        if ($Server -eq "system") {
            $result = Resolve-DnsName $HostName -Type A -DnsOnly -ErrorAction Stop
        } else {
            $result = Resolve-DnsName $HostName -Type A -Server $Server -DnsOnly -ErrorAction Stop
        }
        $ips = @($result | Where-Object { $_.Type -eq "A" } | Select-Object -ExpandProperty IPAddress)
        if ($ips.Count -gt 0) {
            return @{ Ok = $true; IPs = $ips }
        }
    } catch {}
    return @{ Ok = $false; IPs = @() }
}

function Test-BasicInternet {
    foreach ($host in @("www.baidu.com", "www.microsoft.com")) {
        try {
            $null = Resolve-DnsName $host -Type A -DnsOnly -ErrorAction Stop
            Write-Host "[OK] 基础 DNS 正常: $host 可解析" -ForegroundColor Green
            return $true
        } catch {}
    }
    Write-Host "[FAIL] 基础 DNS 也失败，可能是网络完全断开或 DNS 配置损坏" -ForegroundColor Red
    return $false
}

Write-Host "--- 1. 基础网络检测 ---" -ForegroundColor Yellow
$basicOk = Test-BasicInternet

Write-Host "`n--- 2. 测试各 DNS 服务器 ---" -ForegroundColor Yellow
$dnsCandidates = @(
    @{ Name = "自动(DHCP)"; Servers = $null },
    @{ Name = "阿里 DNS"; Servers = @("223.5.5.5", "223.6.6.6") },
    @{ Name = "腾讯 DNS"; Servers = @("119.29.29.29", "182.254.116.116") },
    @{ Name = "Cloudflare"; Servers = @("1.1.1.1", "1.0.0.1") },
    @{ Name = "Google DNS"; Servers = @("8.8.8.8", "8.8.4.4") }
)

$workingDns = $null
foreach ($candidate in $dnsCandidates) {
    if ($null -eq $candidate.Servers) {
        $test = Test-DnsResolver -Server "system"
        $label = "system (自动)"
    } else {
        $test = Test-DnsResolver -Server $candidate.Servers[0]
        $label = "$($candidate.Name) ($($candidate.Servers[0]))"
    }
    if ($test.Ok) {
        Write-Host "[OK] $label -> $($test.IPs -join ', ')" -ForegroundColor Green
        if (-not $workingDns) { $workingDns = $candidate }
    } else {
        Write-Host "[FAIL] $label" -ForegroundColor Red
    }
}

$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

Write-Host "`n--- 3. 修复 DNS ---" -ForegroundColor Yellow
if (-not $isAdmin) {
    Write-Host "需要管理员权限修改 DNS。请右键 PowerShell -> 以管理员身份运行" -ForegroundColor Red
} elseif ($workingDns) {
    $adapters = Get-NetAdapter | Where-Object { $_.Status -eq "Up" }
    foreach ($adapter in $adapters) {
        $alias = $adapter.Name
        try {
            if ($null -eq $workingDns.Servers) {
                Set-DnsClientServerAddress -InterfaceAlias $alias -ResetServerAddresses -ErrorAction Stop
                Write-Host "[OK] $alias -> 恢复为自动(DHCP) DNS" -ForegroundColor Green
            } else {
                Set-DnsClientServerAddress -InterfaceAlias $alias -ServerAddresses $workingDns.Servers -ErrorAction Stop
                Write-Host "[OK] $alias -> $($workingDns.Servers -join ', ')" -ForegroundColor Green
            }
        } catch {
            Write-Host "[SKIP] $alias : $_" -ForegroundColor DarkYellow
        }
    }
    ipconfig /flushdns | Out-Null
    Write-Host "[OK] DNS 缓存已刷新" -ForegroundColor Green
} else {
    Write-Host "所有 DNS 均失败，将尝试 hosts 文件备用方案" -ForegroundColor Red
}

Write-Host "`n--- 4. hosts 文件备用（DNS 全失败时）---" -ForegroundColor Yellow
$hostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"
$hostsBlock = @"

# === Cursor Network Fix (可删除此段) ===
34.234.109.125 api2.cursor.sh
104.18.18.125 api3.cursor.sh
50.18.248.73 agent.api5.cursor.sh
3.216.242.30 repo42.cursor.sh
172.64.152.23 authenticator.cursor.sh
172.66.144.201 marketplace.cursorapi.com
104.18.16.128 downloads.cursor.com
104.26.8.156 cursor-cdn.com
32.196.97.191 prod.authentication.cursor.sh
# === End Cursor Fix ===
"@

if ($isAdmin -and -not $workingDns) {
    $hostsContent = Get-Content $hostsPath -Raw -ErrorAction SilentlyContinue
    if ($hostsContent -notmatch "Cursor Network Fix") {
        Add-Content -Path $hostsPath -Value $hostsBlock -Encoding ASCII
        Write-Host "[OK] 已写入 hosts 备用条目到 $hostsPath" -ForegroundColor Green
        Write-Host "注意: hosts IP 可能随时间变化，DNS 恢复后请删除此段" -ForegroundColor Yellow
    } else {
        Write-Host "[SKIP] hosts 中已有 Cursor 条目" -ForegroundColor DarkYellow
    }
} elseif (-not $workingDns) {
    Write-Host "请手动以管理员编辑 $hostsPath ，添加 scripts/cursor-hosts-snippet.txt 中的内容" -ForegroundColor Yellow
} else {
    Write-Host "[SKIP] DNS 已恢复，无需 hosts 备用" -ForegroundColor Green
}

Write-Host "`n--- 5. 写入 Cursor 设置 ---" -ForegroundColor Yellow
$settingsPaths = @(
    "$env:APPDATA\Cursor\User\settings.json",
    "$env:LOCALAPPDATA\Cursor\User\settings.json"
)
$patched = $false
foreach ($path in $settingsPaths) {
    $dir = Split-Path $path
    if (-not (Test-Path $dir)) { continue }
    try {
        if (-not (Test-Path $path)) {
            @{ "cursor.general.disableHttp2" = $true } | ConvertTo-Json | Set-Content $path -Encoding UTF8
        } else {
            $settings = Get-Content $path -Raw -Encoding UTF8 | ConvertFrom-Json
            $settings | Add-Member -NotePropertyName "cursor.general.disableHttp2" -NotePropertyValue $true -Force
            $settings | ConvertTo-Json -Depth 10 | Set-Content $path -Encoding UTF8
        }
        Write-Host "[OK] 已设置 disableHttp2: $path" -ForegroundColor Green
        $patched = $true
        break
    } catch {
        Write-Host "[SKIP] $path" -ForegroundColor DarkYellow
    }
}
if (-not $patched) {
    Write-Host '请手动添加: "cursor.general.disableHttp2": true' -ForegroundColor Yellow
}

Write-Host "`n--- 6. 验证 ---" -ForegroundColor Yellow
Start-Sleep -Seconds 2
$final = Test-DnsResolver -Server "system"
if ($final.Ok) {
    Write-Host "[OK] api2.cursor.sh -> $($final.IPs -join ', ')" -ForegroundColor Green
} else {
    Write-Host "[FAIL] 仍无法解析，请检查:" -ForegroundColor Red
    Write-Host "  - 是否开启了 VPN/代理（尝试关闭或换节点）"
    Write-Host "  - 用手机热点测试"
    Write-Host "  - 联系网络管理员检查防火墙是否拦截 DNS(UDP 53)"
}

Write-Host "`n完成后请完全退出 Cursor 并重新运行 Network Diagnostics。" -ForegroundColor Cyan
