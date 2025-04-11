from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel
from app.api import messages

app = FastAPI()
app.include_router(messages.router)

BASE_PATH = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_PATH / "app" / "templates"))

# Mount the static directory
app.mount("/static", StaticFiles(directory=str(BASE_PATH / "static")), name="static")

class TextInput(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "base.html", 
        {"request": request, "title": "Hello", "content": "Tokeniser"}
    )

@app.post("/tokenize")
async def tokenize(text_input: TextInput):
    # Simple tokenization (split by spaces)
    tokens = text_input.text.strip().split()
    return {"tokens": tokens}

@app.post("/detokenize")
async def detokenize(text_input: TextInput):
    # Join tokens back into text
    text = " ".join(text_input.text.strip().split())
    return {"text": text}

