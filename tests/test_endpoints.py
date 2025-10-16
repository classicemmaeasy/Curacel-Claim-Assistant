import io

# This test_endpoints.py contains integration tests for the FastAPI endpoints.
# I use the test client to simulate requests and validate responses.

def test_extract_returns_raw_text_json(client):
    """This ensure /extract returns valid structured JSON with raw_text."""
    fake_file = io.BytesIO(b"%PDF-fake-content")
    response = client.post(
        "/extract",
        files={"file": ("claim.pdf", fake_file, "application/pdf")},
    )
    assert response.status_code == 200
    data = response.json()
    assert "document_id" in data
    assert "extracted_data" in data
    assert "raw_text" in data["extracted_data"]


def test_ask_returns_answer(client):
    """ This function ensure /ask returns a concise and  answer."""
    payload = {"document_id": "mock-doc-id", "question": "How many tablets?"}
    response = client.post("/ask", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["answer"] == "10 tablets"
