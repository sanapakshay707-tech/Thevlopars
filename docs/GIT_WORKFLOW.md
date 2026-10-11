# Git Workflow (simple rules for 5 people)

Golden rules:
1. **Nobody pushes directly to `main`** (except the lead for the first scaffold).
2. **One person = one branch = their own files.** This avoids merge conflicts.
3. Pull before you start work. Push small and often.
4. If the app does not run, do not merge.

## Branch names
| Member | Branch |
| --- | --- |
| Yash Thakur | `yash-thakur/integration` |
| Sharvaree | `sharvaree/dataset` |
| Vaibhav | `vaibhav/pdf-evidence` |
| Yash | `yash/extraction` |
| Akshya | `akshya/similarity` |

## Daily routine
```
git checkout main
git pull origin main
git checkout <your-branch>
git merge main            # bring latest changes into your branch
# ... work with Antigravity, test it ...
git add .
git commit -m "FR-03: extract text page by page"
git push origin <your-branch>
```
Then open a **Pull Request** on GitHub (branch -> main) using the template.
One other member reviews (10 minutes max), then the lead merges.

## First time creating your branch
```
git checkout main
git pull origin main
git checkout -b vaibhav/pdf-evidence
git push -u origin vaibhav/pdf-evidence
```

## Commit message style
`<requirement>: <what you did>` -> `FR-08: detect Acts and sections with regex`

## If you get a merge conflict
1. Do not panic and do not delete other people's code.
2. Open the file, find `<<<<<<<` and `>>>>>>>`, keep both needed parts.
3. Ask the lead or ask the agent: "Explain this merge conflict simply and help me resolve it safely."

## Never push
- `venv/` folder, `cache/`, model files, API keys, `.env`
- Judgment PDFs you are not allowed to redistribute (see docs/DATASET_GUIDE.md)
