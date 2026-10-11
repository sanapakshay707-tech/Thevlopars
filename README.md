# CourtLens ⚖️

> **AI-Powered Legal Document Analysis & Summarization Tool**  
> Ingests court judgments (PDFs) and extracts structured case information, summaries, and clickable evidence citations using a local Large Language Model (`qwen2.5:1.5b` via Ollama). 100% offline, privacy-preserving, and attorney-client compliant.

---

## 🌟 Overview & SRS Compliance

CourtLens is built strictly in accordance with the **CourtLens - Software Requirements Specification (SRS)**:
- **Local AI Inference**: Runs entirely offline with zero remote cloud API calls. Inference is driven by a local Ollama server running at `http://localhost:11434/api/generate` using `qwen2.5:1.5b`.
- **FastAPI Backend**: Uses PyMuPDF (`fitz`) for fast binary PDF parsing and text extraction with OCR fallback capabilities.
- **Modern React Frontend**: Clean, responsive legal tech interface featuring dual-pane analysis and interactive PDF document preview.
- **Clickable Textual Evidence**: Pinpoints the exact page and sentence context for parties, statutes, issues, and rulings, preventing AI hallucinations (User Story 2).
- **Error Resilience**: Gracefully handles corrupt, invalid, or empty PDFs without crashing, and explicitly identifies interim orders without hallucinating non-existent final outcomes (User Story 3 & 4).

---

## 🏗️ System Architecture

```
   ┌────────────────────────────────────────────────────────┐
   │             React SPA (Vite + React 18)                │
   │  • File Upload & Dropzone      • Evidence Viewer       │
   │  • Structured Case Cards       • Side-by-side PDF View │
   └───────────────────────────┬────────────────────────────┘
                               │ HTTP / JSON (Port 5173 / Proxy)
                               ▼
   ┌────────────────────────────────────────────────────────┐
   │                 FastAPI Backend Server                 │
   │  • GET  /api/health       • GET /api/samples           │
   │  • POST /api/analyze      • GET /api/sample/{filename} │
   └─────────────┬───────────────────────────┬──────────────┘
                 │                           │
                 ▼                           ▼
   ┌───────────────────────────┐ ┌───────────────────────────┐
   │   PyMuPDF PDF Engine      │ │   Local Ollama Server     │
   │  • Fast Page Extraction   │ │   http://localhost:11434  │
   │  • Regex Statutes Finder  │ │   Model: qwen2.5:1.5b     │
   │  • Context Snippet Search │ │   Structured JSON Mode    │
   └───────────────────────────┘ └───────────────────────────┘
```

---

## 📋 Directory Structure

```
Courtlens/
├── CourtLens - Software Requirements Specification.docx   # Original SRS document
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application & endpoints
│   │   ├── config.py            # Ollama & server settings
│   │   ├── models.py            # Pydantic schemas (SRS contract compliant)
│   │   ├── pdf_processor.py     # PyMuPDF extraction & evidence locator
│   │   ├── ollama_client.py     # Ollama API client (http://localhost:11434/api/generate)
│   │   └── analyzer.py          # Structured prompt engineering & cross-validation
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── run_tests.py         # Automated unit test suite (5 test cases)
│   │   └── test_api.py          # Pytest suite
│   └── requirements.txt
├── frontend/
│   ├── package.json
│   ├── vite.config.js          # Vite config with backend proxy
│   ├── index.html
│   └── src/
│       ├── App.jsx             # Main interactive application
│       ├── main.jsx
│       ├── index.css           # Modern legal-tech design styles
│       └── components/
│           ├── Navbar.jsx           # Status badge & privacy indicator
│           ├── FileUpload.jsx       # Drag & drop upload + 1-click QA cases
│           ├── AnalysisViewer.jsx   # Case type, parties, statutes, issues, outcome
│           ├── SummaryCard.jsx      # Narrative factual summary + copy action
│           ├── EvidenceViewer.jsx   # Clickable evidence references
│           └── DocumentPreview.jsx  # Side-by-side PDF preview with highlight spotlight
├── sample_data/                     # QA Test Judgments (Civil, Criminal, Interim, Corrupt)
├── start_courtlens.bat              # Master 1-click startup script
├── run_backend.bat                  # Start FastAPI backend (port 8000)
├── run_frontend.bat                 # Start React frontend (port 5173)
├── run_tests.bat                    # Run QA test suite
└── README.md
```

---

## 🚀 Quick Start & 3-Minute Demo Runbook

### Option 1: One-Click Launch (Windows)
Double-click `start_courtlens.bat` in the root folder.  
It will automatically:
1. Verify Ollama is running at `http://localhost:11434` with model `qwen2.5:1.5b`.
2. Start the FastAPI backend on `http://localhost:8000`.
3. Start the Vite React frontend on `http://localhost:5173`.
4. Open your browser directly to `http://localhost:5173`.

### Option 2: Step-by-Step Manual Launch

#### Step 1: Ensure Ollama is running
```bash
ollama list
# Should display qwen2.5:1.5b
```

#### Step 2: Start the Backend
```bash
# In Courtlens/ root
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
Test health:
```bash
curl http://localhost:8000/api/health
# Returns {"status":"ok","model":"qwen2.5:1.5b","ready":true,...}
```

#### Step 3: Start the Frontend
```bash
cd frontend
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 🧪 Testing & Verification Matrix

Run the automated test suite with:
```bash
python backend\tests\run_tests.py
```
Or double-click `run_tests.bat`.

All 5 core requirements from the SRS Testing Plan are verified:

| Test Case | Description | Verified Criteria | Result |
|---|---|---|---|
| **Health Check** | `GET /api/health` | Connects to Ollama model, reports readiness | **PASS** ✅ |
| **Civil Judgment** | `POST /api/analyze` | Extracted parties (Ramesh Sharma vs Modern Real Estate), Section 73 Contract Act, Section 34 CPC, final decree, evidence snippets | **PASS** ✅ |
| **Criminal Judgment** | `POST /api/analyze` | Extracted state vs accused, Section 420 IPC, Section 313 CrPC, final acquittal order | **PASS** ✅ |
| **Interim Order** | `POST /api/analyze` | Detects stay/notice and reports `N/A - Interim Order / No final outcome` without hallucinating | **PASS** ✅ |
| **Corrupted Document** | `POST /api/analyze` | Returns HTTP 400 Bad Request with clear explanation; server does not crash | **PASS** ✅ |

---

## 📡 API Contract Specification

### `GET /api/health`
**Response (200 OK):**
```json
{
  "status": "ok",
  "model": "qwen2.5:1.5b",
  "ready": true,
  "engine": "Ollama",
  "ollama_url": "http://localhost:11434/api/generate",
  "available_models": ["qwen2.5:1.5b"]
}
```

### `POST /api/analyze`
**Request:** `multipart/form-data` with `file=<binary PDF>`

**Response (200 OK):**
```json
{
  "caseType": "Civil",
  "parties": {
    "petitioner": "Ramesh Sharma",
    "respondent": "Modern Real Estate Developers Pvt. Ltd."
  },
  "legalProvisions": [
    "Section 73 of the Indian Contract Act, 1872",
    "Section 34 of the Code of Civil Procedure, 1908"
  ],
  "issues": [
    "Whether appellant is entitled to liquidated damages for breach of commercial lease"
  ],
  "summary": "The appellant Ramesh Sharma entered into a commercial lease agreement...",
  "outcome": "Appeal allowed. Respondent directed to refund Rs. 25,00,000 with 9% interest.",
  "evidence": [
    {
      "page": 1,
      "text": "...Ramesh Sharma ... Appellant versus Modern Real Estate Developers...",
      "field": "parties"
    },
    {
      "page": 2,
      "text": "...Section 73 of the Indian Contract Act, 1872...",
      "field": "provisions"
    }
  ],
  "error": null,
  "pageCount": 2,
  "processingTimeMs": 2450.0
}
```

**Error Response (400 Bad Request):**
```json
{
  "detail": "Invalid or corrupted PDF: Failed to open stream"
}
```
