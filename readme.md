

## creating a virtual Environment
- python -m venv xenv
- cd xenv/Scripts
- ./activate
- cd..


## My Approach

### /extract endpoint

- User uploads a PDF or image.

- The file is temporarily saved and processed using an OCR model (e.g., Google Gemini Vision pro 2.5).

- Extracted text is parsed and structured into key-value JSON.

- Structured data is stored in in-memory storage for quick access.

- The API returns the structured JSON and a unique document_id.

### /ask endpoint

- Receives document_id and user question.

- Waits 2 seconds (as instructed).

- Internally overrides any user question to "What medication is used and why?"

- Retrieves the stored structured data.

- Sends context + question to the LLM for reasoning.

- Returns a simple JSON answer.


## My file Structure

```
DATA_EXTRACTION/
│
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py              # Defines data schemas for requests/responses
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ocr_extractor.py        # OCR + Gemini Vision data extraction logic
│   │   └── storage.py              # Handles saving & retrieving structured data
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── config.py               # Environment + Gemini API key configuration
│   │
│   └── main.py                     # FastAPI entrypoint with /extract & /ask endpoints
│
├── tests/
│   ├── conftest.py                 # Pytest fixtures (mocks OCR, storage, Gemini)
│   └── test_endpoints.py           # Unit tests for endpoints
│
├── xenv/                           # Virtual environment (ignored in deployment)
│
├── .env                            # API keys and local environment variables
├── check.py                        # Verifies PDF-to-image conversion (requires Poppler path)
├── extracted_docs.json             # Stores mock or sample extracted data
├── requirements.txt                # Python dependencies
└── readme.md                       # Project documentation
```
