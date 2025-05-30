from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from auth import get_current_user
from embed import embed_and_store

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def health():
    return {"status": "RAG-as-a-Service backend live"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), user_id: str = Depends(get_current_user)):
    contents = await file.read()
    result = embed_and_store(contents, file.filename, user_id)
    return result

class AskRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(req: AskRequest, user_id: str = Depends(get_current_user)):
    return {
        "answer": f"Answer for '{req.question}' from user {user_id}.",
        "sources": []
    }
