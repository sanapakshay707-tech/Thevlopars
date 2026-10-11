"""Owner: Yash (2nd). SRS: FR-06 to FR-12. Rules + regex first, LLM only if time remains.
Every field must look like:
  {"value": ..., "evidence": "exact text from PDF", "page": 4}  or  {"value": "Not found", ...}
Never invent facts.
"""

def extract_case_info(pages: list[dict]) -> dict:
    """Return dict with: category, parties, acts_and_sections, legal_issues,
    key_facts, outcome, summary. Each with evidence + page."""
    raise NotImplementedError
