import os
from hashlib import sha256
from pinecone import Pinecone
from fastapi import HTTPException

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

def list_user_documents(user_id):
    results = index.describe_index_stats()
    vectors = results["namespaces"].get(user_id, {})
    vector_count = vectors.get("vector_count", 0)
    if vector_count == 0:
        return []

    fetch_res = index.fetch(ids=None, namespace=user_id)
    docs = {}
    for vid, item in fetch_res.vectors.items():
        meta = item.get("metadata", {})
        doc_id = meta.get("doc_id")
        if doc_id not in docs:
            docs[doc_id] = {
                "filename": meta.get("filename", "unknown"),
                "doc_id": doc_id,
                "chunks": 1
            }
        else:
            docs[doc_id]["chunks"] += 1
    return list(docs.values())

def delete_user_document(user_id, doc_id):
    fetch_res = index.fetch(ids=None, namespace=user_id)
    to_delete = [vid for vid, item in fetch_res.vectors.items() if item.get("metadata", {}).get("doc_id") == doc_id]
    if not to_delete:
        raise HTTPException(status_code=404, detail="No vectors found for doc")
    index.delete(ids=to_delete, namespace=user_id)
    return {"deleted": len(to_delete)}
