import json
import os

STORAGE_FILE = "extracted_docs.json"

# this storage file will hold extracted claim data that my ocr extractor gets

# this is to Ensure storage file exists
if not os.path.exists(STORAGE_FILE):
    with open(STORAGE_FILE, "w") as f:
        json.dump({}, f)

def save_document(document_id: str, data: dict):
    """Save extracted claim data to a persistent JSON file."""
    with open(STORAGE_FILE, "r+", encoding="utf-8") as f:
        store = json.load(f)
        store[document_id] = data
        f.seek(0)
        json.dump(store, f, indent=2, ensure_ascii=False)
        f.truncate()

def get_document(document_id: str):
    """Retrieve a stored claim by its document_id."""
    with open(STORAGE_FILE, "r", encoding="utf-8") as f:
        store = json.load(f)
        return store.get(document_id)
