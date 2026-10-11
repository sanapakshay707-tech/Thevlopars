@echo off
set "PATH=C:\Users\Dell\AppData\Local\Microsoft\WinGet\Packages\Git.MinGit_Microsoft.Winget.Source_8wekyb3d8bbwe\cmd;%PATH%"
cd /d "C:\Users\Dell\Documents\Courtlens"

echo 1. Initializing Git repository...
git init

echo 2. Setting local commit author...
git config user.name "sanapakshay707-tech"
git config user.email "sanapakshay707@users.noreply.github.com"

echo 3. Configuring remote...
git remote remove origin 2>nul
git remote add origin https://github.com/sanapakshay707-tech/Thevlopars.git

echo 4. Staging files...
git add .

echo 5. Committing changes...
git commit -m "Initial commit: CourtLens Legal AI Analysis System (FastAPI + React + Ollama)"

echo 6. Setting branch to main...
git branch -M main

echo 7. Pushing to GitHub...
git push -u origin main
