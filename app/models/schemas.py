# this is my schema to define the request and response models for the API endpoints
# basically it is for my data validation and serialization

from pydantic import BaseModel
from typing import Optional, Dict, Any

class ExtractResponse(BaseModel):
    document_id: str
    extracted_data: Dict[str, Any]

class AskRequest(BaseModel):
    document_id: str
    question: str

class AskResponse(BaseModel):
    answer: str
