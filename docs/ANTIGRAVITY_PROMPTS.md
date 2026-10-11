# Antigravity Prompts (copy and paste)

How to use:
1. Open the repo folder in Antigravity. Switch to your own Git branch first.
2. Open Agent Manager -> New Task. Use **Planning mode**.
3. Read the plan the agent makes BEFORE you approve it.
4. Run and test the result yourself. If it fails, paste the full error back.
5. Commit and push after every working step.

Useful follow-up prompts:
- "Explain the core logic of this module in simple English with a small example for each part."
- "I got this error: <paste>. Explain the cause in simple words, then fix it with minimal changes."
- "Write 3 tests for this function, including an empty file and a bad file."
- "Do not change any file except <file>."

---

## Yash Thakur - Integration, UI, storage
**Task 1: Streamlit layout (FR-23, FR-24, FR-25)**
```
Read PROJECT_RULES.md and docs/SRS.md (sections 4.4 and 6.1). Only edit app.py.
Build a single-page Streamlit dashboard with these sections: Upload, Status/Errors,
Case Analysis (category, parties, Acts/sections, legal issues, key facts, outcome, summary),
Similar Cases (top 5 cards with score, shared provisions, explanation, stored outcome, source),
and Evidence (source passage + page). Use placeholder data for now.
Add a spinner while processing, a warning banner that results are preliminary, and a
"Not found / uncertain" label style for missing fields. Explain how to run it.
```
**Task 2: storage.py (SRS section 9)**
```
Read PROJECT_RULES.md and docs/SRS.md (section 9). Only edit modules/storage.py and tests.
Implement load_cases() and save_cases() for dataset/cases.json using paths from config.py.
Validate each record (unique case_id, required keys). Skip broken records, report them,
never crash. Missing outcome must be "unknown". Add tests.
```
**Task 3: Integration (after others merge)**
```
Read PROJECT_RULES.md and docs/SRS.md (section 7 and 10). Only edit app.py.
Connect: pdf_processor.validate_pdf -> extract_pages -> information_extractor.extract_case_info
-> storage.load_cases -> similarity_engine.rank_similar_cases -> display with evidence.
Handle each error case from SRS section 11 with a clear message.
```

## Sharvaree - Dataset, testing, docs
**Task 1: cases.json builder from the metadata sheet**
```
Read PROJECT_RULES.md and docs/SRS.md (section 9). Create scripts/csv_to_cases_json.py that
reads a CSV (columns: case_id, case_name, court, judgment_date, source_url, local_pdf_path,
category, topic_group) and writes dataset/cases.json using the format in dataset/cases_template.json.
Missing values must stay null/empty. Do not invent any metadata.
```
**Task 2: Precision@5 script**
```
Read PROJECT_RULES.md and docs/SRS.md (sections 8 and 13.5). Create scripts/evaluate.py that,
for given query case IDs, runs the similarity engine and prints top-5 results and Precision@5
using the topic_group labels in cases.json as ground truth. Save results to a CSV.
```

## Vaibhav - PDF processing and evidence
**Task 1: pdf_processor (FR-01 to FR-04, NFR-17)**
```
Read PROJECT_RULES.md and docs/SRS.md (FR-01 to FR-05). Only edit modules/pdf_processor.py
and tests/test_pdf_processing.py. Implement validate_pdf(file_bytes, max_mb) and
extract_pages(file_bytes) with PyMuPDF. Reject empty/corrupt/too-big files with clear messages.
Return [{"page": n, "text": str, "is_scanned": bool}]. Mark a page as scanned if it has
almost no text but contains images. Never crash on bad input. Add tests.
```
**Task 2: text_extractor + evidence_manager (FR-13)**
```
Read PROJECT_RULES.md and docs/SRS.md (FR-13, section 7.2 F). Edit modules/text_extractor.py
and modules/evidence_manager.py. Clean text and split into chunks keeping page numbers.
find_evidence(pages, snippet) must return the exact passage and page, or None.
Never fabricate quotes or page numbers.
```

## Yash - Information extraction
**Task 1: rule-based extraction (FR-06 to FR-12)**
```
Read PROJECT_RULES.md and docs/SRS.md (FR-06 to FR-13, section 7.2 C). Only edit
modules/information_extractor.py and tests/test_extraction.py. Use regex/rules only (no LLM).
Input: pages list from pdf_processor. Extract: case category (civil/criminal/uncertain),
parties with roles (appellant, respondent, petitioner, accused), Acts and sections
(e.g. "Section 138 of the Negotiable Instruments Act"), legal issue, key facts, outcome
(allowed, dismissed, disposed, etc.), and a short summary. Each field returns
{"value":..., "evidence":..., "page":...}. If unsure return "Not found" or "Uncertain".
Do not force a civil/criminal label. Interim orders must not be shown as final outcome.
```
**Task 2 (only after P0 works): optional Ollama helper**
```
Add an optional function that uses a local Ollama model (qwen2.5:3b) to improve issue/summary text.
It must be switched by ENABLE_LLM in config.py and fall back to rule-based output if Ollama is missing.
```

## Akshya - Similarity engine
**Task 1: signals and ranking (section 8)**
```
Read PROJECT_RULES.md and docs/SRS.md (section 8, FR-14 to FR-22). Only edit
modules/similarity_engine.py and tests/test_similarity.py. Implement:
(A) semantic similarity using sentence-transformers all-MiniLM-L6-v2 + cosine,
(B) shared Acts/sections score with simple normalization (exact section match counts more than only the Act name),
(C) TF-IDF cosine similarity on facts/keywords using scikit-learn.
Combined = 0.60*semantic + 0.25*provision + 0.15*keyword using weights from config.py.
All scores are 0-1. If a signal is missing, renormalize the remaining weights (never treat missing as a perfect match).
Exclude the query case itself. Return top 5 with an explanation text built from the real matched provisions/terms.
Load the model once and cache embeddings. Add tests with small dummy data.
```
**Task 2: scripts/prepare_dataset.py**
```
Read PROJECT_RULES.md and docs/SRS.md (FR-14, FR-15, section 9). Implement scripts/prepare_dataset.py:
for each PDF in dataset/judgments/, run pdf_processor and information_extractor, build the
representation text, create the embedding, and save everything into dataset/cases.json.
Skip broken files and print a report at the end.
```
