@echo off
title CourtLens Test Suite
set "PATH=C:\Users\Dell\AppData\Local\Programs\Python\Python311;C:\Users\Dell\AppData\Local\Programs\Python\Python311\Scripts;%PATH%"
cd /d "C:\Users\Dell\Documents\Courtlens"

echo ===================================================
echo Running CourtLens Automated Verification Test Suite
echo ===================================================

python backend\tests\run_tests.py
pause
