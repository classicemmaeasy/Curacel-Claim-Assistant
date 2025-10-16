

## creating a virtual Environment
- python -m venv xenv
- cd xenv/Scripts
- ./activate
- cd..


## My Approach

### /extract endpoint

- Accepts an image or PDF.

- Passes it to Gemini Vision Pro 2.5.

- Extracts structured info in a flexible JSON schema.

- Stores result in memory with a generated document_id.

### /ask endpoint

- Receives document_id and user question.

- Waits 2 seconds (as instructed).

- Internally overrides any user question to "What medication is used and why?"

- Retrieves the stored structured data.

- Sends context + question to the LLM for reasoning.

- Returns a simple JSON answer.


