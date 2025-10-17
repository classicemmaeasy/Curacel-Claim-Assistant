
## Intelligent Claims QA Service
This project implements a FastAPI-based microservice that accepts uploaded claim sheets (PDF or image), extracts key details using OCR and LLM reasoning, and enables users to ask natural-language questions about the extracted data.

The system demonstrates the integration of computer vision, language processing, and structured reasoning into a cohesive and practical solution.




## Assumptions and my thought process
- I decided to use Fastapi because of its async concurency capability (handling multiple users at the same time) and it improve overall system throughput and responsiveness, particularly in I/O-bound scenarios.

- I chose Gemini 2.5 Vision Pro because it combines powerful OCR, visual understanding, and natural language reasoning into a single step unlike traditional OCR tools like Tesseract that require multiple stages and struggle with unstructured or low-quality claim documents. Gemini 2.5 Vision Pro accurately extracts structured medical data (e.g., diagnoses, medications, dosages) directly from scanned or photographed forms, understands context, and handles variations in layout effortlessly. Its efficiency, contextual intelligence, and seamless integration made it the ideal choice for building a robust, scalable, and intelligent claims QA service.
- Its multimodal reasoning also allows for deeper contextual understanding of medical data (e.g., differentiating between medication dosage and total cost). This made it superior for structured extraction and QA accuracy within limited development time.

- I added the time module to handle retry logic for Gemini API calls specifically to manage rate limits (429 errors) and timeout errors (504 errors). Gemini’s free-tier API occasionally rejects requests when the quota is exceeded or when the model takes too long to respond. By introducing a short delay using time.sleep(10) before retrying, the service avoids crashing and ensures stability under temporary API issues. This improves reliability and user experience, allowing the app to recover gracefully instead of failing abruptly.

- I implemented persistent storage using a JSON file (extracted_docs.json) to ensure that extracted claim data from uploaded documents remains available for subsequent /ask queries, even after the API restarts. While in-memory storage (like a Python dictionary) would have been simpler, it would lose all data once the server stops. By using a lightweight JSON-based approach, I achieved a balance between simplicity, persistence, and maintainability ideal for this small-scale microservice. This design avoids the overhead of setting up a full database while ensuring that document data can be easily retrieved, tested, and debugged, which aligns well with the task’s focus on practicality and reliability.

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

## How to use Locally
### clone the  repo
```
- git clone https://github.com/classicemmaeasy/Curacel-Claim-Assistant.git
- cd Curacel-Claim-Assistant
```
## creating a virtual Environment
```
- python -m venv xenv
- xenv\Scripts\activate    # For Windows
# OR
- source xenv/bin/activate # For Mac/Linux
```
# dependencies
```
pip install --upgrade pip
pip install -r requirements.txt
```

# Package to install
- poppler: it helps pdf2image to convert pdf to images.
- install it here : https://github.com/oschwartz10612/poppler-windows/releases/

# setup api key in  .env
- create .env file
- GEMINI_API_KEY=your_google_gemini_api_key_here
- get it here
https://makersuite.google.com/app/apikey

# run the app
uvicorn app.main:app --reload
- make sure the path you run it is the same folder w
App runs at: http://127.0.0.1:8000

