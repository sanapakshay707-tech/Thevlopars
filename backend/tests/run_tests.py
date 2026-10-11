import os
import sys
import unittest
from fastapi.testclient import TestClient

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from backend.app.main import app

client = TestClient(app)

class TestCourtLensAPI(unittest.TestCase):

    def test_01_health_endpoint(self):
        """Verify GET /api/health returns HTTP 200/503 and proper JSON schema."""
        response = client.get("/api/health")
        self.assertIn(response.status_code, [200, 503])
        data = response.json()
        self.assertIn("status", data)
        self.assertIn("model", data)
        self.assertIn("ready", data)
        self.assertEqual(data["engine"], "Ollama")
        print("  [PASS] test_01_health_endpoint:", data["status"], data["model"])

    def test_02_corrupted_pdf_returns_400(self):
        """Verify User Story 4: corrupted PDF returns HTTP 400 without crashing."""
        corrupted_path = os.path.join("sample_data", "corrupted_document.pdf")
        with open(corrupted_path, "rb") as f:
            response = client.post(
                "/api/analyze",
                files={"file": ("corrupted.pdf", f, "application/pdf")},
            )
        self.assertEqual(response.status_code, 400)
        detail = response.json().get("detail", "")
        self.assertIn("Invalid or corrupted PDF", detail)
        print("  [PASS] test_02_corrupted_pdf_returns_400: Received 400 Bad Request as expected")

    def test_03_empty_file_returns_400(self):
        """Verify uploading an empty file returns HTTP 400."""
        response = client.post(
            "/api/analyze",
            files={"file": ("empty.pdf", b"", "application/pdf")},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("empty", response.json().get("detail", "").lower())
        print("  [PASS] test_03_empty_file_returns_400: Handled empty file properly")

    def test_04_civil_judgment_analysis(self):
        """Verify User Story 1 & 2: civil judgment extracts parties, provisions, outcome and evidence."""
        sample_path = os.path.join("sample_data", "civil_judgment.pdf")
        with open(sample_path, "rb") as f:
            response = client.post(
                "/api/analyze",
                files={"file": ("civil_judgment.pdf", f, "application/pdf")},
            )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("caseType", data)
        self.assertIn("parties", data)
        self.assertIn("legalProvisions", data)
        self.assertIn("summary", data)
        self.assertIn("outcome", data)
        self.assertIn("evidence", data)
        self.assertIsInstance(data["evidence"], list)

        # Check evidence citations have valid pages
        for ev in data["evidence"]:
            self.assertIn("page", ev)
            self.assertIn("text", ev)
            self.assertIn("field", ev)
            self.assertGreaterEqual(ev["page"], 1)

        print("  [PASS] test_04_civil_judgment_analysis: Extracted CaseType =", data["caseType"])
        print("         Parties:", data["parties"])
        print("         Provisions:", data["legalProvisions"])
        print("         Outcome:", data["outcome"][:80])

    def test_05_interim_order_no_final_outcome(self):
        """Verify User Story 3: interim order explicitly handles missing final outcome without inventing one."""
        sample_path = os.path.join("sample_data", "interim_order.pdf")
        with open(sample_path, "rb") as f:
            response = client.post(
                "/api/analyze",
                files={"file": ("interim_order.pdf", f, "application/pdf")},
            )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        outcome = data.get("outcome", "").lower()
        has_interim_indicator = any(term in outcome for term in ["interim", "stay", "n/a", "no final", "adjourned"])
        self.assertTrue(has_interim_indicator, f"Expected interim indicator in outcome, got: {outcome}")
        print("  [PASS] test_05_interim_order_no_final_outcome: Outcome recognized as interim ->", data["outcome"])


if __name__ == "__main__":
    unittest.main()
