$ErrorActionPreference = 'Stop'
$base = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $base
$port = 8972
$url = "http://localhost:$port"
$logDir = Join-Path $base 'logs'
$logFile = Join-Path $logDir 'startup.log'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
Add-Content -Path $logFile -Value "`r`n=================================================="
Add-Content -Path $logFile -Value "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Teknik Servis Pro baslatiliyor"

$nodeExe = Join-Path $base 'runtime\node.exe'
if (-not (Test-Path $nodeExe)) {
    $cmd = Get-Command node -ErrorAction SilentlyContinue
    if ($cmd) { $nodeExe = $cmd.Source }
}
if (-not (Test-Path $nodeExe)) {
    Add-Content $logFile "HATA: Node.js bulunamadi."
    Add-Type -AssemblyName PresentationFramework
    [System.Windows.MessageBox]::Show('Teknik Servis Pro baslatilamadi: Node.js bulunamadi. Kurulumu yeniden yapin.','Teknik Servis Pro') | Out-Null
    exit 1
}
if (-not (Test-Path (Join-Path $base 'node_modules\express\package.json'))) {
    Add-Content $logFile "HATA: node_modules eksik."
    Add-Type -AssemblyName PresentationFramework
    [System.Windows.MessageBox]::Show('Teknik Servis Pro program dosyalari eksik. Kurulumu yeniden yapin.','Teknik Servis Pro') | Out-Null
    exit 1
}

function Test-AppHealth {
    try {
        $r = Invoke-RestMethod -Uri "$url/api/health" -TimeoutSec 1
        return ($r.ok -eq $true)
    } catch { return $false }
}

if (-not (Test-AppHealth)) {
    $env:PORT = "$port"
    Add-Content $logFile "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Node sunucusu baslatiliyor: $nodeExe"
    Start-Process -FilePath $nodeExe -ArgumentList 'server.js' -WorkingDirectory $base -WindowStyle Hidden -RedirectStandardOutput $logFile -RedirectStandardError (Join-Path $logDir 'server-error.log')
}

$ready = $false
for ($i=0; $i -lt 25; $i++) {
    Start-Sleep -Milliseconds 600
    if (Test-AppHealth) { $ready = $true; break }
}

if ($ready) {
    Add-Content $logFile "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Sunucu hazir: $url"
    Start-Process $url
    exit 0
}

Add-Content $logFile "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] HATA: Sunucu baslatilamadi."
Add-Type -AssemblyName PresentationFramework
[System.Windows.MessageBox]::Show("Teknik Servis Pro sunucusu baslatilamadi.`nLog dosyasi acilacak.",'Teknik Servis Pro') | Out-Null
Start-Process notepad.exe -ArgumentList ('"' + $logFile + '"')
exit 1
