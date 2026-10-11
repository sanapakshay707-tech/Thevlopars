# Team Plan - Proof Keeper

Team: Yash Thakur, Sharvaree, Vaibhav, Yash, Akshya
(Two members are named Yash. In this plan, "Yash T." = Yash Thakur and "Yash" = the second Yash.)
You can swap roles. Just make sure every module has ONE owner.

## Roles
| Member | Role | Owns these files | SRS parts |
| --- | --- | --- | --- |
| Yash T. | Team lead, integration, UI | `app.py`, `config.py`, `modules/storage.py`, README | FR-23 to FR-25, section 6, 7, 9 |
| Sharvaree | Dataset + testing + docs | `dataset/`, `docs/TEST_EVALUATION_SHEET.md`, `docs/DEMO_SCRIPT.md` | FR-14, section 9, 13, 18 |
| Vaibhav | PDF processing + evidence | `modules/pdf_processor.py`, `text_extractor.py`, `evidence_manager.py` | FR-01 to FR-05, FR-13 |
| Yash | Information extraction | `modules/information_extractor.py` | FR-06 to FR-12 |
| Akshya | Similarity engine | `modules/similarity_engine.py`, `scripts/prepare_dataset.py` | FR-15 to FR-22, section 8 |

Everyone also writes tests for their own module in `tests/`.

## Timeline (SRS gives 8 hours; hackathon is team work so we run in parallel)

### Step 0 - Setup (first 30 min, all)
- Yash T.: pushes the starter files to `main` (see "First push" below).
- Everyone: clone, run `docs/SETUP_GUIDE.md`, confirm `streamlit run app.py` works.
- Everyone: create own branch (see `docs/GIT_WORKFLOW.md`).

### Block 1 - Build in parallel (hours 1-3)
| Member | Task | Done when |
| --- | --- | --- |
| Sharvaree | Collect 20-30 judgment PDFs, fill `cases.json` metadata (source URL, court, date) | PDFs in `dataset/judgments/`, a metadata sheet ready |
| Vaibhav | Validation + page-wise extraction + scanned-page detection | `extract_pages()` works on 5 PDFs |
| Yash | Regex extraction of parties, Acts/sections, category, outcome | Works on 3 PDFs with evidence + page |
| Akshya | Embeddings + TF-IDF + provision overlap + scoring on dummy data | `rank_similar_cases()` returns top 5 on test data |
| Yash T. | Streamlit layout, storage, config, error messages | Upload box + empty result sections + status area |

### Block 2 - Connect (hours 4-5)
- Vaibhav's output feeds Yash's extractor -> feeds Akshya's ranking.
- Akshya + Sharvaree run `scripts/prepare_dataset.py` to build real `cases.json` with embeddings.
- Yash T. connects everything in `app.py`.

### Block 3 - Evidence and polish (hours 6-7)
- Match explanations, source pages, outcome shown separately, uncertainty warnings.
- Fix bugs found in testing.

### Block 4 - Test and demo (hour 8)
- Sharvaree leads testing with 5 query judgments and records Precision@5.
- Everyone rehearses the demo (`docs/DEMO_SCRIPT.md`).

## Handshake between modules (agree on this early!)
- `pdf_processor.extract_pages(bytes)` -> `[{"page": 1, "text": "...", "is_scanned": False}]`
- `information_extractor.extract_case_info(pages)` -> dict with `category, parties, acts_and_sections, legal_issues, key_facts, outcome, summary`. Each field has `value`, `evidence`, `page`.
- `similarity_engine.rank_similar_cases(query_case, stored_cases, top_k)` -> list of result dicts.
If you change the format, tell the whole team in the group chat first.

## First push (Yash T. only, one time)
1. Copy ALL files from the starter folder into the cloned repo folder.
2. Run:
```
git add .
git commit -m "Initial project structure"
git push origin main
```
3. Tell the others: "Pull main and create your branches."

## Daily sync (10 minutes, every 2 hours)
Each person answers: What did I finish? What am I stuck on? What do I need from someone?

## Priority rule (from SRS)
P0 first: upload, extraction, structured info, dataset, ranking, explanation, outcome, error handling.
P1 only after P0 works: OCR, local LLM, filters, charts. A working end-to-end app beats a fancy half-done one.
