from fastapi import FastAPI, File, UploadFile
from pdf2image import convert_from_bytes
from PIL import Image
import json
from utils import extract_text, extract_line_items

app = FastAPI()

@app.post("/upload")
async def upload_bill(file: UploadFile = File(...)):

    contents = await file.read()

    if file.filename.endswith(".pdf"):
        pages = convert_from_bytes(contents)
    else:
        pages = [Image.open(file.file)]

    full_text = ""

    for img in pages:
        full_text += extract_text(img) + "\n"

    result = extract_line_items(full_text)

    output = {
        "file_name": file.filename,
        "extracted_data": result
    }

    return output
