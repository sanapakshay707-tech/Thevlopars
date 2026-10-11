@echo off
title CourtLens Frontend Server
set "PATH=C:\Users\Dell\AppData\Local\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.20.0-win-x64;%PATH%"
cd /d "C:\Users\Dell\Documents\Courtlens\frontend"

echo ===================================================
echo Starting CourtLens React Frontend on http://localhost:5173
echo ===================================================

npm run dev
pause
