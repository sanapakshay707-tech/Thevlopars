import logging
import time
from typing import Any, Dict, List
from .models import AnalysisResponse, EvidenceItem, Parties
from .pdf_processor import PDFDocument
from .ollama_client import OllamaClient
from .config import MAX_DOC_CHARS

logger = logging.getLogger("courtlens.analyzer")

SYSTEM_PROMPT = """You are an expert legal document analyzer specializing in court judgments and orders.
Analyze the provided court judgment text accurately. Extract ONLY information explicitly supported by the text.
Do NOT invent or hallucinate facts, parties, statutes, or outcomes.
If the judgment is an interim order or has no final outcome, set outcome to "N/A - Interim Order / No final outcome".

Return ONLY a valid JSON object with EXACTLY this structure:
{
  "caseType": "Civil" or "Criminal" or "Constitutional" or "Commercial" or "Other",
  "parties": {
    "petitioner": "Name of petitioner / appellant / plaintiff",
    "respondent": "Name of respondent / defendant"
  },
  "legalProvisions": ["Exact cited legal sections/articles/acts, e.g. Section 420 IPC"],
  "issues": ["Key legal issues or questions framed by the court"],
    "summary": "A 5-7 point plain-language summary for a general reader",
    "advocateSummary": "A 5-7 point legally focused summary for a junior advocate",
  "outcome": "Final order / ruling, or 'N/A - Interim Order / No final outcome'",
  "keyQuotes": [
    {"field": "parties", "quote": "exact phrase from text naming the parties"},
    {"field": "legalProvisions", "quote": "exact phrase from text mentioning the section or act"},
    {"field": "issues", "quote": "exact phrase framing the core dispute or issue"},
    {"field": "outcome", "quote": "exact phrase stating the court's final ruling or order"}
  ]
}"""


class JudgmentAnalyzer:
    def __init__(self, ollama_client: OllamaClient):
        self.client = ollama_client

    async def analyze(self, pdf_doc: PDFDocument) -> AnalysisResponse:
        start_time = time.time()

        # Check if text exists
        full_text = pdf_doc.get_full_text(max_chars=MAX_DOC_CHARS)
        if not full_text.strip():
            return AnalysisResponse(
                caseType="Unknown",
                summary="The document appears to be scanned or contains no extractable text layer.",
                outcome="N/A",
                error="Could not extract text from PDF (document may be empty or unreadable scanned image).",
                pageCount=pdf_doc.page_count,
                processingTimeMs=round((time.time() - start_time) * 1000, 2),
            )

        # Heuristic legal provisions extraction for backup/cross-verification
        heuristic_provisions = pdf_doc.extract_heuristic_legal_provisions()

        # Build prompt for LLM
        prompt = f"""Analyze the following court judgment and extract the required structured information in JSON format:

DOCUMENT TEXT:
{full_text}

Remember:
1. Identify if Civil, Criminal, Constitutional, etc.
2. List exact parties (Petitioner vs Respondent).
3. List cited legal sections/statutes.
4. In "summary", write 5-7 numbered points in plain language for a general reader, aiming for 120-170 words when supported by the document. Explain what happened, what each side wanted, the court's decision or current status, and what it means in everyday terms. Briefly explain legal terms that are necessary.
5. In "advocateSummary", write 5-7 numbered points for a junior advocate, aiming for 150-200 words when supported. Cover procedural posture, material facts, issues, each side's submissions, applicable provisions or precedents expressly cited, the court's reasoning and holding, relief granted or refused, and any next steps or unresolved issues apparent from the text.
6. Keep both summaries accurate and grounded in the document. Clearly distinguish allegations and party submissions from facts the court found or accepted. Do not infer legal rules, procedural steps, or practical consequences not stated in the judgment. Use fewer points for short documents; do not pad.
7. If there is NO final decision (e.g. interim order, notice issued, matter adjourned), set outcome to "N/A - Interim order / No final outcome" and make the pending status clear in both summaries.
8. In keyQuotes, include short exact phrases copied directly from the text as evidence."""

        try:
            llm_result = await self.client.generate_json(
                prompt=prompt,
                system=SYSTEM_PROMPT,
            )
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            # Graceful fallback: return heuristic extraction if LLM is unavailable or fails
            return self._build_fallback_response(pdf_doc, heuristic_provisions, start_time, error=str(e))

        if not isinstance(llm_result, dict):
            llm_result = {"summary": str(llm_result)}

        # Parse LLM response
        case_type = str(llm_result.get("caseType") or "Civil").strip()
        parties_data = llm_result.get("parties")
        petitioner = "N/A"
        respondent = "N/A"

        if isinstance(parties_data, dict):
            petitioner = str(parties_data.get("petitioner") or "N/A").strip()
            respondent = str(parties_data.get("respondent") or "N/A").strip()
        elif isinstance(parties_data, str) and parties_data.strip():
            raw_p = parties_data.strip()
            # Split on ' vs ', ' v. ', ' versus '
            import re
            parts = re.split(r"\s+(?:vs\.?|v\.?|versus)\s+", raw_p, flags=re.IGNORECASE)
            if len(parts) >= 2:
                petitioner = parts[0].strip()
                respondent = parts[1].strip()
            else:
                petitioner = raw_p
                respondent = "N/A"
        elif isinstance(parties_data, list):
            if len(parties_data) >= 1:
                petitioner = str(parties_data[0]).strip()
            if len(parties_data) >= 2:
                respondent = str(parties_data[1]).strip()

        provisions_raw = llm_result.get("legalProvisions") or []
        if isinstance(provisions_raw, str):
            import re
            provisions = [p.strip() for p in re.split(r"[,;\n]+", provisions_raw) if p.strip()]
        elif isinstance(provisions_raw, list):
            provisions = [str(p).strip() for p in provisions_raw if str(p).strip()]
        else:
            provisions = []

        # Merge with heuristic provisions if model missed obvious ones
        merged_provisions = list(dict.fromkeys(provisions + heuristic_provisions[:5]))

        issues_raw = llm_result.get("issues") or []
        if isinstance(issues_raw, str):
            import re
            issues = [i.strip() for i in re.split(r"[\n;]+", issues_raw) if i.strip()]
        elif isinstance(issues_raw, list):
            issues = [str(i).strip() for i in issues_raw if str(i).strip()]
        else:
            issues = []

        summary = str(llm_result.get("summary") or "").strip()
        advocate_summary = str(llm_result.get("advocateSummary") or "").strip()
        outcome = str(llm_result.get("outcome") or "N/A").strip()

        # Evidence gathering and verification
        evidence_items: List[EvidenceItem] = []
        key_quotes = llm_result.get("keyQuotes") or []
        if isinstance(key_quotes, list):
            for item in key_quotes:
                if isinstance(item, dict):
                    quote = str(item.get("quote", "")).strip()
                    field = str(item.get("field", "general")).strip()
                elif isinstance(item, str):
                    quote = item.strip()
                    field = "general"
                else:
                    continue

                if quote:
                    page_num, snippet = pdf_doc.find_evidence_snippet(quote, preferred_field=field)
                    evidence_items.append(EvidenceItem(
                        page=page_num,
                        text=snippet,
                        field=field,
                    ))

        # Ensure we have evidence for the primary fields (parties, provisions, outcome)
        existing_fields = {e.field for e in evidence_items}

        if "parties" not in existing_fields and (petitioner != "N/A" or respondent != "N/A"):
            phrase = petitioner if petitioner != "N/A" else respondent
            page_num, snippet = pdf_doc.find_evidence_snippet(phrase, preferred_field="parties")
            evidence_items.append(EvidenceItem(page=page_num, text=snippet, field="parties"))

        if "provisions" not in existing_fields and merged_provisions:
            page_num, snippet = pdf_doc.find_evidence_snippet(merged_provisions[0], preferred_field="provisions")
            evidence_items.append(EvidenceItem(page=page_num, text=snippet, field="provisions"))

        if "outcome" not in existing_fields and outcome and outcome != "N/A":
            page_num, snippet = pdf_doc.find_evidence_snippet(outcome[:60], preferred_field="outcome")
            evidence_items.append(EvidenceItem(page=page_num, text=snippet, field="outcome"))

        elapsed = round((time.time() - start_time) * 1000, 2)

        return AnalysisResponse(
            caseType=case_type,
            parties=Parties(petitioner=petitioner, respondent=respondent),
            legalProvisions=merged_provisions,
            issues=issues,
            summary=summary,
            advocateSummary=advocate_summary or summary,
            outcome=outcome,
            evidence=evidence_items,
            error=None,
            pageCount=pdf_doc.page_count,
            processingTimeMs=elapsed,
        )

    def _build_fallback_response(
        self,
        pdf_doc: PDFDocument,
        heuristic_provisions: List[str],
        start_time: float,
        error: str
    ) -> AnalysisResponse:
        """Constructs safe structured response using text heuristics when LLM is unavailable."""
        first_page = pdf_doc.pages_text[0] if pdf_doc.pages_text else ""
        evidence_items = []

        if heuristic_provisions:
            p_num, snip = pdf_doc.find_evidence_snippet(heuristic_provisions[0], "provisions")
            evidence_items.append(EvidenceItem(page=p_num, text=snip, field="provisions"))

        return AnalysisResponse(
            caseType="Civil / Criminal",
            parties=Parties(petitioner="See Document Header", respondent="See Document Header"),
            legalProvisions=heuristic_provisions,
            issues=["Extracted from judgment provisions"],
            summary=f"Automated fallback extraction. Text length: {len(pdf_doc.get_full_text())} characters across {pdf_doc.page_count} pages.",
            advocateSummary="A junior-advocate summary could not be generated because the language model is unavailable.",
            outcome="N/A",
            evidence=evidence_items,
            error=f"Model inference warning: {error}",
            pageCount=pdf_doc.page_count,
            processingTimeMs=round((time.time() - start_time) * 1000, 2),
        )
