@echo off
title CourtLens Master Launcher
set "PATH=C:\Users\Dell\AppData\Local\Programs\Python\Python311;C:\Users\Dell\AppData\Local\Programs\Python\Python311\Scripts;C:\Users\Dell\AppData\Local\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.20.0-win-x64;%PATH%"
cd /d "C:\Users\Dell\Documents\Courtlens"

echo ===================================================
echo             CourtLens Legal AI System
echo ===================================================
echo 1. Checking Ollama status...
powershell -Command "try { $r = Invoke-RestMethod -Uri 'http://localhost:11434/api/tags' -TimeoutSec 3; Write-Host '   Ollama is running with models:' ($r.models.name -join ', ') -ForegroundColor Green } catch { Write-Host '   Warning: Ollama not reachable on http://localhost:11434. Please start Ollama.' -ForegroundColor Yellow }"

echo 2. Launching FastAPI Backend on port 8000...
start "CourtLens Backend" cmd /k run_backend.bat

echo 3. Launching Vite React Frontend on port 5173...
start "CourtLens Frontend" cmd /k run_frontend.bat

echo 4. Waiting for servers to initialize...
timeout /t 3 /nobreak > nul

echo 5. Opening CourtLens in browser...
start http://localhost:5173

echo ===================================================
echo CourtLens is running at http://localhost:5173
echo ===================================================
pause
