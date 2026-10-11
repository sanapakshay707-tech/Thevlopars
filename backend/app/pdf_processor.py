import logging
import re
from typing import Dict, List, Tuple
import pymupdf

logger = logging.getLogger("courtlens.pdf_processor")


class InvalidPDFError(Exception):
    """Raised when PDF file is invalid or corrupt."""
    pass


class PDFDocument:
    def __init__(self, raw_bytes: bytes, filename: str = "document.pdf"):
        self.filename = filename
        self.raw_bytes = raw_bytes
        self.pages_text: List[str] = []
        self.page_count: int = 0
        self.is_scanned: bool = False
        self._parse()

    def _parse(self):
        try:
            doc = pymupdf.open(stream=self.raw_bytes, filetype="pdf")
        except Exception as e:
            logger.error(f"Failed to open PDF {self.filename}: {e}")
            raise InvalidPDFError(f"Invalid or corrupted PDF file: {str(e)}")

        self.page_count = len(doc)
        if self.page_count == 0:
            doc.close()
            raise InvalidPDFError("PDF document has 0 pages.")

        total_chars = 0
        for i, page in enumerate(doc):
            try:
                text = page.get_text("text")
            except Exception as e:
                logger.warning(f"Error getting text on page {i + 1}: {e}")
                text = ""
            self.pages_text.append(text)
            total_chars += len(text.strip())

        # If very little text across pages, attempt OCR or mark as scanned
        avg_chars_per_page = total_chars / max(1, self.page_count)
        if avg_chars_per_page < 30:
            logger.info("Detected low text layer; attempting OCR on available pages...")
            self.is_scanned = True
            ocr_pages = []
            for i, page in enumerate(doc):
                try:
                    # Attempt PyMuPDF OCR if available
                    tp = page.get_textpage_ocr(language="eng", dpi=150, full=True)
                    ocr_text = page.get_text(textpage=tp)
                    ocr_pages.append(ocr_text if ocr_text.strip() else self.pages_text[i])
                except Exception as ocr_err:
                    logger.debug(f"OCR not available or failed for page {i + 1}: {ocr_err}")
                    ocr_pages.append(self.pages_text[i])
            self.pages_text = ocr_pages
            total_chars = sum(len(t.strip()) for t in self.pages_text)

        doc.close()

        if total_chars == 0:
            logger.warning("No text extracted from PDF even after OCR checks.")

    def get_full_text(self, max_chars: int = 24000) -> str:
        """Returns concatenated text across all pages up to max_chars, sampling head and tail for large judgments."""
        if not self.pages_text:
            return ""

        total_pages = len(self.pages_text)
        if total_pages <= 8:
            accumulated = []
            current_len = 0
            for page_idx, text in enumerate(self.pages_text):
                header = f"\n--- [PAGE {page_idx + 1}] ---\n"
                cleaned = self._clean_text(text)
                if not cleaned:
                    continue
                addition = header + cleaned
                if current_len + len(addition) > max_chars:
                    remaining = max_chars - current_len
                    if remaining > 100:
                        accumulated.append(addition[:remaining] + "\n...[Document truncated]...")
                    break
                accumulated.append(addition)
                current_len += len(addition)
            return "".join(accumulated)

        # For long judgments (e.g. 10 to 100+ pages): allocate 60% budget to start, 40% to end
        head_budget = int(max_chars * 0.6)
        tail_budget = max_chars - head_budget

        head_parts = []
        head_len = 0
        last_head_idx = 0
        for page_idx in range(total_pages):
            text = self.pages_text[page_idx]
            cleaned = self._clean_text(text)
            if not cleaned:
                continue
            addition = f"\n--- [PAGE {page_idx + 1}] ---\n" + cleaned
            if head_len + len(addition) > head_budget:
                remaining = head_budget - head_len
                if remaining > 100:
                    head_parts.append(addition[:remaining])
                last_head_idx = page_idx
                break
            head_parts.append(addition)
            head_len += len(addition)
            last_head_idx = page_idx

        tail_parts = []
        tail_len = 0
        first_tail_idx = total_pages
        for page_idx in range(total_pages - 1, last_head_idx, -1):
            text = self.pages_text[page_idx]
            cleaned = self._clean_text(text)
            if not cleaned:
                continue
            addition = f"\n--- [PAGE {page_idx + 1}] ---\n" + cleaned
            if tail_len + len(addition) > tail_budget:
                first_tail_idx = page_idx
                break
            tail_parts.insert(0, addition)
            tail_len += len(addition)
            first_tail_idx = page_idx

        separator = f"\n\n--- [... Pages {last_head_idx + 2} to {first_tail_idx} omitted for prompt context ...] ---\n\n"
        return "".join(head_parts) + separator + "".join(tail_parts)

    @staticmethod
    def _clean_text(text: str) -> str:
        # Collapse excessive whitespace while preserving paragraph lines
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
        return text.strip()

    def find_evidence_snippet(self, phrase: str, preferred_field: str = "") -> Tuple[int, str]:
        """
        Locates the best matching page and contextual snippet for a given phrase.
        Returns (page_number (1-indexed), snippet_text).
        """
        if not phrase or len(phrase.strip()) < 3:
            return 1, "Document text referenced."

        clean_phrase = phrase.strip()
        # Clean phrase of punctuation for looser matching
        search_words = [w for w in re.split(r"\W+", clean_phrase.lower()) if len(w) > 2]

        best_page = 1
        best_snippet = ""
        best_score = 0

        # Pass 1: Exact substring match
        for page_idx, page_text in enumerate(self.pages_text):
            lower_page = page_text.lower()
            idx = lower_page.find(clean_phrase.lower())
            if idx != -1:
                start = max(0, idx - 60)
                end = min(len(page_text), idx + len(clean_phrase) + 80)
                snippet = page_text[start:end].replace("\n", " ").strip()
                return page_idx + 1, f"...{snippet}..."

        # Pass 2: Keyword overlap match
        if search_words:
            for page_idx, page_text in enumerate(self.pages_text):
                lower_page = page_text.lower()
                matches = sum(1 for w in search_words if w in lower_page)
                score = matches / len(search_words)
                if score > best_score and score >= 0.4:
                    best_score = score
                    best_page = page_idx + 1
                    # Extract surrounding sentence
                    sentences = re.split(r"(?<=[.!?])\s+", page_text)
                    for s in sentences:
                        s_lower = s.lower()
                        s_matches = sum(1 for w in search_words if w in s_lower)
                        if s_matches >= 2 or (len(search_words) == 1 and s_matches == 1):
                            best_snippet = s.replace("\n", " ").strip()
                            break
                    if not best_snippet and sentences:
                        best_snippet = sentences[0].replace("\n", " ").strip()

        if best_snippet:
            clean_snip = best_snippet[:200]
            return best_page, f"...{clean_snip}..."

        # Default fallback to first non-empty page
        for page_idx, page_text in enumerate(self.pages_text):
            if page_text.strip():
                snippet = page_text.strip()[:140].replace("\n", " ")
                return page_idx + 1, f"...{snippet}..."

        return 1, f"Extracted from document."

    def extract_heuristic_legal_provisions(self) -> List[str]:
        """Regex extractor to discover common Indian legal provisions."""
        full = "\n".join(self.pages_text)
        patterns = [
            r"Section\s+\d+[A-Z]?(?:\s*\([0-9a-zA-Z]+\))?(?:\s+of\s+the\s+[A-Za-z\s]+Act)?",
            r"Article\s+\d+[A-Z]?(?:\s*\([0-9a-zA-Z]+\))?",
            r"Order\s+[IVXLCDM]+\s+Rule\s+\d+",
            r"Section\s+\d+\s+IPC",
            r"Section\s+\d+\s+CrPC",
            r"Section\s+\d+\s+CPC",
        ]
        found = set()
        for p in patterns:
            for match in re.finditer(p, full, re.IGNORECASE):
                prov = match.group(0).strip()
                if len(prov) < 50:
                    found.add(prov)
        return sorted(list(found))
