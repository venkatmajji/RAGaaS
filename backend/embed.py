import os
import tiktoken
import json
from hashlib import sha256
from openai import OpenAI
from pinecone import Pinecone
from chunker import chunk_text

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

def embed_and_store(content, filename, user_id):
    chunks = chunk_text(content, max_tokens=750)
    vectors = []
    for i, chunk in enumerate(chunks):
        response = client.embeddings.create(
            input=[chunk],
            model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
        )
        vector = response.data[0].embedding
        doc_id = sha256(f"{user_id}-{filename}-{i}".encode()).hexdigest()
        vectors.append((doc_id, vector, {"filename": filename, "user_id": user_id, "chunk": i}))

    index.upsert(vectors=vectors, namespace=user_id)
    return {"status": "embedded", "chunks": len(vectors)}
