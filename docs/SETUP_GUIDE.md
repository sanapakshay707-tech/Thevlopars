# Setup Guide (every member does this on their own laptop)

## 1. Install tools (one time)
1. **Python 3.11** from python.org. Tick **"Add python.exe to PATH"**.
2. **Git** from git-scm.com.
3. **Antigravity IDE** from the official Google Antigravity site. Install on the **C: drive**
   and sign in with your Google account.
4. Check in a terminal:
   ```
   python --version
   git --version
   ```

## 2. Tell Git who you are (one time)
```
git config --global user.name "Your Name"
git config --global user.email "your-github-email@example.com"
```

## 3. Clone the repository
```
git clone <REPO_URL>
cd <repo-folder>
```
Open this folder in Antigravity (File > Open Folder).

## 4. Create the virtual environment
```
py -3.11 -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
You must see `(venv)` at the start of the terminal line. Activate it every time you open a new terminal.
If `activate` is blocked in PowerShell, run once:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## 5. Download the embedding model (needs internet, do it once)
```
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2'); print('model ready')"
```

## 6. Run the app
```
streamlit run app.py
```
A browser tab opens. If you see the "Proof Keeper" title and an upload box, your setup is fine.

## 7. Antigravity settings we use
- Review policy: **Request Review** (agent asks before big actions).
- Mode: **Planning** for big tasks, **Fast** for small edits.
- Each task starts with: "Read PROJECT_RULES.md and docs/SRS.md first."
- One task = one module = one Git branch.

## Common problems
| Problem | Fix |
| --- | --- |
| `python` not found | Reinstall Python and tick "Add to PATH" |
| `pip install` fails for torch or sentence-transformers | Copy the full error to the agent: "Explain the cause in simple words and fix it" |
| Streamlit does not open | Check venv is active; run `pip install streamlit` |
| Model download fails | Check Wi-Fi; try again; ask a teammate to share the model folder |
