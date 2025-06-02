import os
import tiktoken
import json
from hashlib import sha256
from openai import OpenAI
from pinecone import Pinecone
from .chunker import chunk_text

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

def embed_and_store(content, filename, user_id):
    chunks = chunk_text(content, max_tokens=750)
    vectors = []
    failed = 0

    for i, chunk in enumerate(chunks):
        chunk_preview = chunk[:120].replace("\n", " ").strip()
        print(f"[EMBED] Chunk {i+1}/{len(chunks)}: {chunk_preview}...")

        if len(chunk) < 10:
            print(f"[EMBED] Skipping short chunk {i+1}")
            continue

        try:
            response = client.embeddings.create(
                input=[chunk],
                model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
            )
            vector = response.data[0].embedding
            doc_id = sha256(f"{user_id}-{filename}-{i}".encode()).hexdigest()

            metadata = {
                "filename": filename,
                "user_id": user_id,
                "chunk": i,
                "text": chunk_preview
            }

            vectors.append((doc_id, vector, metadata))

        except Exception as e:
            print(f"[EMBED ERROR] Chunk {i+1} failed: {e}")
            failed += 1

    if vectors:
        index.upsert(vectors=vectors, namespace=user_id)
        print(f"[EMBED] ✅ Upserted {len(vectors)} chunks to Pinecone.")

    return {
        "status": "embedded",
        "chunks": len(vectors),
        "failed": failed
    }
