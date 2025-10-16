import sys
import os
import pytest
from fastapi.testclient import TestClient

# This conftest.py applies mocks to prevent real external calls during tests.
# I use pytest fixtures to patch methods in the app's services.

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


@pytest.fixture(autouse=True)
def apply_mocks(monkeypatch):
    """
    I Apply mocks at function-scope (monkeypatch is function-scoped).
    This runs before each test and prevents real OCR/Gemini/storage calls.
    """
    # --- fake OCR extractor ---
    def fake_extract_data_from_image(file_path: str):
        return {
            "document_id": "mock-doc-id",
            "extracted_data": {
                "raw_text": """
                {
                    "patient_details": {"name": "John Doe", "age": 40, "gender": "Male"},
                    "diagnoses": ["Malaria"],
                    "medications": [
                        {"name": "Paracetamol", "dosage": "500mg", "quantity": "10 tablets"}
                    ],
                    "total_amount": "₦15,000"
                }
                """
            },
        }

    monkeypatch.setattr(
        "app.services.ocr_extractor.extract_data_from_image",
        fake_extract_data_from_image,
        raising=False,
    )

    # --- fake storage ---
    mock_db = {
        "mock-doc-id": {
            "patient_details": {"name": "John Doe"},
            "medications": [
                {"name": "Paracetamol", "dosage": "500mg", "quantity": "10 tablets"}
            ],
        }
    }

    def fake_save_document(doc_id, data):
        mock_db[doc_id] = data

    def fake_get_document(doc_id):
        return mock_db.get(doc_id)

    monkeypatch.setattr("app.services.storage.save_document", fake_save_document, raising=False)
    monkeypatch.setattr("app.services.storage.get_document", fake_get_document, raising=False)

    # --- fake Gemini QA ---
    class FakeResponse:
        text = "10 tablets"

    def fake_generate_content(prompt, **kwargs):
        return FakeResponse()

    # patch the generate_content method on the qa_model object that your app creates.
    # I cannot reliably import app.main.qa_model here (it may not exist yet), so I patch the attribute on the module after import.
    # To ensure this fixture runs before client uses app, I let client import app after this fixture runs.
    monkeypatch.setattr("app.main.qa_model.generate_content", fake_generate_content, raising=False)

    yield
    # monkeypatch will automatically undo on function teardown


@pytest.fixture
def client():
    """
    Create TestClient AFTER autouse apply_mocks has run for the test,
    so imports in app.main will use the patched targets.
    """
    from app.main import app
    return TestClient(app)
