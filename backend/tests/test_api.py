import os
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Verify GET /api/health returns HTTP 200 or 503 and proper JSON schema."""
    response = client.get("/api/health")
    assert response.status_code in (200, 503)
    data = response.json()
    assert "status" in data
    assert "model" in data
    assert "ready" in data
    assert data["engine"] == "Ollama"


def test_corrupted_pdf_returns_400():
    """Verify User Story 4: corrupted PDF returns HTTP 400 without crashing."""
    corrupted_path = os.path.join("sample_data", "corrupted_document.pdf")
    with open(corrupted_path, "rb") as f:
        response = client.post(
            "/api/analyze",
            files={"file": ("corrupted.pdf", f, "application/pdf")},
        )
    assert response.status_code == 400
    detail = response.json().get("detail", "")
    assert "Invalid or corrupted PDF" in detail


def test_empty_file_returns_400():
    """Verify uploading an empty file returns HTTP 400."""
    response = client.post(
        "/api/analyze",
        files={"file": ("empty.pdf", b"", "application/pdf")},
    )
    assert response.status_code == 400
    assert "empty" in response.json().get("detail", "").lower()


def test_civil_judgment_analysis():
    """Verify User Story 1 & 2: civil judgment extracts parties, provisions, outcome and evidence."""
    sample_path = os.path.join("sample_data", "civil_judgment.pdf")
    with open(sample_path, "rb") as f:
        response = client.post(
            "/api/analyze",
            files={"file": ("civil_judgment.pdf", f, "application/pdf")},
        )
    assert response.status_code == 200
    data = response.json()
    assert "caseType" in data
    assert "parties" in data
    assert "petitioner" in data["parties"]
    assert "respondent" in data["parties"]
    assert "legalProvisions" in data
    assert "summary" in data
    assert "outcome" in data
    assert "evidence" in data
    assert isinstance(data["evidence"], list)
    # Check evidence structure
    for ev in data["evidence"]:
        assert "page" in ev
        assert "text" in ev
        assert "field" in ev
        assert ev["page"] >= 1


def test_interim_order_no_final_outcome():
    """Verify User Story 3: interim order explicitly handles missing final outcome without inventing one."""
    sample_path = os.path.join("sample_data", "interim_order.pdf")
    with open(sample_path, "rb") as f:
        response = client.post(
            "/api/analyze",
            files={"file": ("interim_order.pdf", f, "application/pdf")},
        )
    assert response.status_code == 200
    data = response.json()
    outcome = data.get("outcome", "").lower()
    # Should reflect interim / stay / notice or N/A
    assert any(term in outcome for term in ["interim", "stay", "n/a", "no final", "adjourned"])
