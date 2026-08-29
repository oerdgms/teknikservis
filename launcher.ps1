$ErrorActionPreference = 'Stop'
$base = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $base
$port = 8972
$url = "http://localhost:$port"
$logDir = Join-Path $base 'logs'
$startupLog = Join-Path $logDir 'startup.log'
$serverOut = Join-Path $logDir 'server-output.log'
$serverErr = Join-Path $logDir 'server-error.log'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

function Write-StartupLog([string]$message) {
    Add-Content -Path $startupLog -Value "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $message" -Encoding UTF8
}

function Show-AppError([string]$message) {
    Add-Type -AssemblyName PresentationFramework
    [System.Windows.MessageBox]::Show($message, 'Teknik Servis Pro') | Out-Null
}

function Test-AppHealth {
    try {
        $r = Invoke-RestMethod -Uri "$url/api/health" -TimeoutSec 1
        return ($r.ok -eq $true)
    } catch {
        return $false
    }
}

Write-StartupLog 'Teknik Servis Pro v2.2.2 başlatılıyor.'

$nodeExe = Join-Path $base 'runtime\node.exe'
if (-not (Test-Path $nodeExe)) {
    $nodeCommand = Get-Command node -ErrorAction SilentlyContinue
    if ($nodeCommand) { $nodeExe = $nodeCommand.Source }
}

if (-not (Test-Path $nodeExe)) {
    Write-StartupLog 'HATA: Node.js çalışma zamanı bulunamadı.'
    Show-AppError "Teknik Servis Pro başlatılamadı.`nNode.js çalışma zamanı bulunamadı.`nKurulumu yeniden yapın."
    exit 1
}

if (-not (Test-Path (Join-Path $base 'server.js'))) {
    Write-StartupLog 'HATA: server.js bulunamadı.'
    Show-AppError "Teknik Servis Pro program dosyaları eksik.`nKurulumu yeniden yapın."
    exit 1
}

if (-not (Test-Path (Join-Path $base 'node_modules\express\package.json'))) {
    Write-StartupLog 'HATA: node_modules/express eksik.'
    Show-AppError "Teknik Servis Pro bağımlılık dosyaları eksik.`nKurulumu yeniden yapın."
    exit 1
}

if (-not (Test-AppHealth)) {
    $env:PORT = "$port"
    Write-StartupLog "Sunucu başlatılıyor: $nodeExe"
    try {
        Start-Process -FilePath $nodeExe `
            -ArgumentList 'server.js' `
            -WorkingDirectory $base `
            -WindowStyle Hidden `
            -RedirectStandardOutput $serverOut `
            -RedirectStandardError $serverErr
    } catch {
        Write-StartupLog ("HATA: Node süreci başlatılamadı: " + $_.Exception.Message)
        Show-AppError "Teknik Servis Pro sunucusu başlatılamadı.`nLog dosyası açılacak."
        if (Test-Path $startupLog) { Start-Process notepad.exe -ArgumentList ('"' + $startupLog + '"') }
        exit 1
    }
}

$ready = $false
for ($i = 0; $i -lt 40; $i++) {
    Start-Sleep -Milliseconds 500
    if (Test-AppHealth) {
        $ready = $true
        break
    }
}

if ($ready) {
    Write-StartupLog "Sunucu hazır: $url"
    Start-Process $url
    exit 0
}

Write-StartupLog 'HATA: Sunucu 20 saniye içinde hazır olmadı.'
Show-AppError "Teknik Servis Pro sunucusu başlatılamadı.`nTanılama kaydı açılacak."
if (Test-Path $serverErr) {
    Start-Process notepad.exe -ArgumentList ('"' + $serverErr + '"')
} else {
    Start-Process notepad.exe -ArgumentList ('"' + $startupLog + '"')
}
exit 1
