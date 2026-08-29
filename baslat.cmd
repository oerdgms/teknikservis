@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "NODE_EXE=node"
if exist "%~dp0runtime\node.exe" set "NODE_EXE=%~dp0runtime\node.exe"
if "%NODE_EXE%"=="node" (
  where node >nul 2>nul
  if errorlevel 1 (
    echo Node.js bulunamadi. GitHub kurulum paketini kullanin veya Node.js 18+ kurun.
    pause
    exit /b 1
  )
)
if not exist "node_modules\express\package.json" (
  if exist "%~dp0runtime\node.exe" (
    echo Kurulum paketi eksik: node_modules bulunamadi.
    pause
    exit /b 1
  )
  echo Ilk calistirma: gerekli paketler kuruluyor...
  call npm install
  if errorlevel 1 (
    echo Gerekli paketler kurulamadi.
    pause
    exit /b 1
  )
)
start "TeknikServisPro" /min cmd /c ""%NODE_EXE%" server.js"
timeout /t 2 /nobreak >nul
start "" "http://localhost:3000"
exit /b 0
