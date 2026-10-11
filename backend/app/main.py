import logging
import os
import time
from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse

from .config import HOST, PORT, OLLAMA_GENERATE_URL, OLLAMA_MODEL
from .models import AnalysisResponse, ErrorResponse, HealthResponse
from .ollama_client import OllamaClient
from .pdf_processor import InvalidPDFError, PDFDocument
from .analyzer import JudgmentAnalyzer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("courtlens.main")

app = FastAPI(
    title="CourtLens API",
    description="Offline Legal Document Analysis & Summarization API",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ollama_client = OllamaClient()
analyzer = JudgmentAnalyzer(ollama_client)


@app.get("/")
def read_root():
    return {
        "app": "CourtLens Legal AI",
        "version": "1.0.0",
        "health": "/api/health",
        "analyze": "/api/analyze",
    }


@app.get(
    "/api/health",
    response_model=HealthResponse,
    summary="Health check endpoint for API and local LLM model",
)
async def health_check():
    health = await ollama_client.check_health()
    status_code = status.HTTP_200_OK if health["ready"] else status.HTTP_503_SERVICE_UNAVAILABLE

    response_data = HealthResponse(
        status="ok" if health["ready"] else "degraded",
        model=health["model"],
        ready=health["ready"],
        engine="Ollama",
        ollama_url=OLLAMA_GENERATE_URL,
        available_models=health["available_models"],
        error=health["error"],
    )
    return JSONResponse(status_code=status_code, content=response_data.model_dump())


@app.get("/api/samples")
def list_samples():
    sample_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "sample_data"))
    if not os.path.exists(sample_dir):
        return []
    return [f for f in os.listdir(sample_dir) if f.endswith(".pdf")]


@app.get("/api/sample/{filename}")
def get_sample_file(filename: str):
    # Prevent path traversal
    safe_name = os.path.basename(filename)
    sample_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "sample_data"))
    file_path = os.path.join(sample_dir, safe_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Sample file not found")
    return FileResponse(file_path, media_type="application/pdf", filename=safe_name)


@app.post(
    "/api/analyze",
    response_model=AnalysisResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid or unreadable PDF"},
        422: {"model": ErrorResponse, "description": "Unprocessable entity"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Ingest PDF court judgment and extract structured case intelligence",
)
async def analyze_judgment(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided in upload.",
        )

    logger.info(f"Received file for analysis: {file.filename} (content_type={file.content_type})")

    # Read binary bytes
    try:
        raw_bytes = await file.read()
    except Exception as e:
        logger.error(f"Failed to read uploaded file: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not read uploaded file: {str(e)}",
        )

    if len(raw_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty (0 bytes).",
        )

    # Process PDF text and structure
    try:
        pdf_doc = PDFDocument(raw_bytes, filename=file.filename)
    except InvalidPDFError as ipe:
        logger.warning(f"Invalid PDF rejected: {ipe}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid or corrupted PDF: {str(ipe)}",
        )
    except Exception as e:
        logger.exception("Unexpected error opening PDF")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or corrupted PDF file.",
        )

    # Analyze document with local LLM and evidence linking
    try:
        result = await analyzer.analyze(pdf_doc)
        return result
    except Exception as e:
        logger.exception("Analysis execution failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis pipeline error: {str(e)}",
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
