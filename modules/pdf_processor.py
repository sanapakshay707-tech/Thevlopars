"""Owner: Vaibhav. SRS: FR-01 to FR-05, NFR-17.
Validate a PDF and extract text page by page with PyMuPDF.
"""

def validate_pdf(file_bytes: bytes, max_mb: int) -> tuple[bool, str]:
    """Return (is_valid, message). Reject empty, too-big, unreadable files."""
    raise NotImplementedError


def extract_pages(file_bytes: bytes) -> list[dict]:
    """Return [{'page': 1, 'text': '...', 'is_scanned': False}, ...]. Keep page numbers."""
    raise NotImplementedError
