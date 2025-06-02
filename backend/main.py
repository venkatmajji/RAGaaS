# backend/main.py

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os


# Local imports (relative or absolute)
from .auth import get_current_user
from .embed import embed_and_store
from .docs import toggle_public, track_usage
from .ask import answer_question
from .parser import extract_text

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ragaas-ui.onrender.com/*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def health():
    return {"status": "RAG-as-a-Service backend live ✅"}

# --------- Upload ----------
@app.post("/upload")
async def upload_file(file: UploadFile = File(...), user_id: str = Depends(get_current_user)):
    try:
        contents = await file.read()
        text = extract_text(file.filename, contents)

        if not text:
            raise ValueError("Unsupported or unreadable file.")

        result = embed_and_store(text, file.filename, user_id)
        return result

    except Exception as e:
        print(f"[UPLOAD ERROR] {e}")
        raise HTTPException(status_code=500, detail="Upload failed.")


# --------- Ask -------------
class AskRequest(BaseModel):
    question: str
    doc_id: str = None  # Optional for per-doc chat

@app.post("/ask")
def ask_question(req: AskRequest, user_id: str = Depends(get_current_user)):
    return answer_question(req.question, user_id=user_id, doc_id=req.doc_id)

# --------- Toggle Public -----
@app.post("/toggle-public")
def toggle(doc_id: str = Form(...), is_public: bool = Form(...), user_id: str = Depends(get_current_user)):
    return toggle_public(doc_id, is_public, user_id)

# --------- Track Usage -------
@app.post("/usage/increment")
def track_usage_public(doc_id: str = Form(...)):
    return track_usage(doc_id)
