# Dataset Guide (owner: Sharvaree)

Goal: 20-30 real Indian judgment PDFs (up to 50), with correct metadata.

## Where to get judgments (manual download only)
- Supreme Court of India official website (judgments section)
- High Court official websites
- eCourts and other official public portals
- Other sources only if their terms allow your use
Check each website's terms. Public does not always mean free to redistribute.
Do not auto-scrape websites (the SRS says no automatic downloading).

## Pick cases with variety (so similarity can be shown)
- 10-15 criminal and 10-15 civil cases
- Groups of 3-4 cases on the SAME topic (example: bail under Section 438 CrPC, cheque bounce under Section 138 NI Act, property/injunction disputes, tenancy)
- A few unrelated cases as "distractors"
- Prefer text-based PDFs (you can select/copy text). Scanned PDFs need OCR.
- English language only for now

## Naming
Save PDFs as `dataset/judgments/case_001.pdf`, `case_002.pdf`, ...

## Metadata sheet (keep in Google Sheet or CSV, then convert to cases.json)
| case_id | case_name | court | judgment_date | source_url | date_downloaded | local_pdf_path | category | topic_group | usage_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Use the template: `dataset/cases_template.json`.

## Rules
- Only write real metadata. If unknown, leave blank/null. Do not guess.
- `metadata_verified` stays `false` until a person checks the PDF.
- Keep `outcome` as "unknown" when you did not read it.
- Check file size. Keep each PDF under the limit in `config.py` (25 MB).
- If a PDF is large or restricted, keep it only locally and list it in `.gitignore`;
  push only the metadata JSON.

## Ground truth for testing (important for Precision@5)
For every case, add a `topic_group` label. Later you will use it to judge whether a top-5 result is relevant.
