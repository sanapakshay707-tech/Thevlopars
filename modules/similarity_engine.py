"""Owner: Akshya. SRS: section 8, FR-14 to FR-21.
Combined = 0.60*semantic + 0.25*provision + 0.15*keyword  (weights come from config.py)
If a signal is missing: renormalize the other weights. Never treat missing as a perfect match.
"""

def build_representation(case_info: dict) -> str:
    raise NotImplementedError


def rank_similar_cases(query_case: dict, stored_cases: list[dict], top_k: int = 5) -> list[dict]:
    """Return top_k results: case_id, score, matched issue, shared provisions,
    explanation, outcome (from stored record), source path/URL."""
    raise NotImplementedError
