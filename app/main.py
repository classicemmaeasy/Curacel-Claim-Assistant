from fastapi import FastAPI, UploadFile, File, HTTPException
from app.services.ocr_extractor import extract_data_from_image
from app.services.storage import save_document, get_document
from app.utils.helpers import delay_processing
from app.models.schemas import AskRequest, AskResponse
import google.generativeai as genai
from app.config import GEMINI_API_KEY
import tempfile
import os
import json
import time

app = FastAPI(title="Intelligent Claims QA Service")

# Configuring my Gemini model
genai.configure(api_key=GEMINI_API_KEY)
qa_model = genai.GenerativeModel(
    "gemini-2.5-pro",
    generation_config={"temperature": 0.1}
)


@app.get("/")
def home():
    return {
        "message": "Intelligent Claims QA Service is running.",
        "docs": "Visit /docs to test the API interactively."
    }


@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    try:
        file_ext = os.path.splitext(file.filename)[1] or ".jpg"
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        # Extracting  information from the image or PDF
        result = extract_data_from_image(temp_file_path)

        # Cleanup temporary file
        os.remove(temp_file_path)

        # Validate result structure
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        if "document_id" not in result or "extracted_data" not in result:
            raise HTTPException(status_code=500, detail="Unexpected response structure from extractor")

        # I'm saving persistently to JSON file for later retrieval using my in-memory storage service as instucted
        save_document(result["document_id"], result["extracted_data"])

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ask", response_model=AskResponse)
async def ask(payload: AskRequest):
    delay_processing(2)  # Required 2-second pause

    # actual question from request body
    question = payload.question.strip()

    data = get_document(payload.document_id)
    if not data:
        raise HTTPException(status_code=404, detail="Document not found")

    context = json.dumps(data, indent=2, ensure_ascii=False)

    prompt = f"""
    You are an intelligent medical claims QA assistant.
    You must answer questions strictly using the structured claim data provided below.

    CLAIM DATA:
    {context}

    USER QUESTION: {question}

    RULES:
    - Do not hallucinate or add information not found in the claim.
    - If asked for a number, dosage, unit price, Total price or quantity, return only that numeric value with its unit (e.g., "10 tablets") and any information found in the claim.
    - If asked for a descriptive answer, use one short factual sentence.
    - Keep the answer concise and accurate (under 20 words).

    ANSWER:
    """

    # Retry logic for API timeouts or quota limits
    for attempt in range(2):
        try:
            response = qa_model.generate_content(prompt, request_options={"timeout": 120})
            answer = response.text.strip()
            break
        except Exception as e:
            if "429" in str(e) or "504" in str(e):
                time.sleep(10)
                continue
            raise HTTPException(status_code=400, detail=f"Gemini processing error: {e}")
    else:
        raise HTTPException(status_code=400, detail="Gemini failed after retrying twice.")

    # my clean up formatting
    answer = answer.replace("*", "").replace("-", "").replace("\n", " ").strip()

    return {"answer": answer}
