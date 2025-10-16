import uuid
import json
from typing import Dict, Any
from PIL import Image
from pdf2image import convert_from_path
import google.generativeai as genai
import tempfile
import os
from app.config import GEMINI_API_KEY

# this ocr extractor is to extract the text from the image or pdf file I was given

genai.configure(api_key=GEMINI_API_KEY)

def extract_data_from_image(file_path: str) -> Dict[str, Any]:
    model = genai.GenerativeModel("gemini-2.5-pro")
    temp_images = []

    try:
        #  to Detect the  file type
        if file_path.lower().endswith(".pdf"):
            # Convert PDF pages to temporary images
            temp_dir = tempfile.mkdtemp()
            pages = convert_from_path(
                file_path,
                dpi=200,
                poppler_path=r"C:\poppler\poppler-24.08.0\Library\bin"  
            )
            print(f"Converted {len(pages)} PDF page(s) successfully.")

            for i, page in enumerate(pages):
                temp_img_path = os.path.join(temp_dir, f"page_{i}.jpg")
                page.save(temp_img_path, "JPEG")
                temp_images.append(Image.open(temp_img_path))
        else:
            # Regular image file
            temp_images.append(Image.open(file_path))
    except Exception as e:
        return {"error": f"Invalid or unreadable image/PDF: {e}"}

    prompt = """
    You are an intelligent medical claim document parser.
    Analyze this medical claim document and extract all key structured information:
    - Patient details (name, age, gender)
    - Diagnosis / Diagnoses
    - Number of Dosage (numbers)
    - Medications (name, dosage, quantity, unit price, total price)
    - Procedures / Tests
    - Admission details (admission/discharge date, admission status)
    - Total amount billed or settlement amount
    Output strictly as clean JSON with descriptive keys.
    """

    try:
        print("Sending images to Gemini for extraction...")
        response = model.generate_content([prompt] + temp_images, request_options={"timeout": 180})

        try:
            data = json.loads(response.text)
        except Exception:
            data = {"raw_text": response.text.strip()}

        document_id = str(uuid.uuid4())
        print(f"Extraction complete. Document ID: {document_id}")
        return {"document_id": document_id, "extracted_data": data}

    except Exception as e:
        return {"error": f"Gemini processing error: {e}"}

    finally:
        for img in temp_images:
            try:
                img.close()
            except:
                pass
