from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
import string

app = FastAPI()

# Mount static and template directories
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Pydantic model for input validation
class InputData(BaseModel):
    data: List[str]  # Expects format: {"data": ["M", "1", ...]}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process")
async def process_text(input_data: InputData):
    items = input_data.data

    alphabets = []
    numbers = []
    lowercase_letters = []

    # Filter through the input items
    for item in items:
        if isinstance(item, str):
            stripped = item.strip()

            # Check for alphabetic characters (Latin only)
            if stripped.isalpha() and stripped.islower():
                lowercase_letters.append(stripped)
                alphabets.append(stripped)

            # Check for numeric strings (whole items)
            elif stripped.isdigit():
                numbers.append(stripped)

    # Find the highest value lowercase letter (based on ASCII value)
    highest_alpha = max(lowercase_letters, key=ord) if lowercase_letters else None

    return {
        "alphabets": alphabets,
        "numbers": numbers,
        "highest_alpha": highest_alpha
    }

# Optional route for testing without frontend
@app.post("/test-process")
async def test_process(input_data: InputData):
    return await process_text(input_data)
