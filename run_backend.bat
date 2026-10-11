@echo off
title CourtLens Backend Server
set "PATH=C:\Users\Dell\AppData\Local\Programs\Python\Python311;C:\Users\Dell\AppData\Local\Programs\Python\Python311\Scripts;%PATH%"
cd /d "C:\Users\Dell\Documents\Courtlens"

echo ===================================================
echo Starting CourtLens FastAPI Backend on http://localhost:8000
echo Ollama API Target: http://localhost:11434/api/generate
echo ===================================================

python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
pause
