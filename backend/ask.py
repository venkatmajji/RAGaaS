import os
from openai import OpenAI
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))
embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

def answer_question(query: str, user_id: str = "guest", doc_id: str = None):
    print(f"[ASK] User: {user_id} | Question: {query}")

    # Step 1: Embed the question
    try:
        embedding = client.embeddings.create(
            input=[query],
            model=embedding_model
        ).data[0].embedding
    except Exception as e:
        return {"error": f"Embedding failed: {str(e)}"}

    # Step 2: Query Pinecone
    try:
        query_filter = {"user_id": user_id}
        if doc_id:
            query_filter["doc_id"] = doc_id

        results = index.query(
            vector=embedding,
            top_k=10,
            include_metadata=True,
            filter=query_filter,
            namespace=user_id
        )

        matches = results.matches or []

        # Log raw matches
        for i, m in enumerate(matches):
            preview = m.metadata.get("text", "")[:80].replace("\n", " ").strip()
            print(f"🔍 Match {i+1} | Score={m.score:.4f} | {preview}")

        # Fallback: keyword scan if no matches
        if not matches:
            print("⚠️ No semantic matches. Attempting keyword fallback...")
            all_results = index.query(
                vector=embedding,
                top_k=50,
                include_metadata=True,
                filter={"user_id": user_id},
                namespace=user_id
            ).matches

            keyword = query.lower()
            matches = [
                m for m in all_results
                if keyword in m.metadata.get("text", "").lower()
            ]

            if matches:
                print(f"✅ Keyword fallback found {len(matches)} matches.")
            else:
                return {"answer": "No relevant documents found.", "sources": []}

        # Step 3: Prepare context for GPT
        context_chunks = [m.metadata.get("text", "") for m in matches]
        context_block = "\n\n".join(context_chunks)

    except Exception as e:
        return {"error": f"Pinecone query failed: {str(e)}"}

    # Step 4: Call OpenAI GPT
    prompt = f"""You are a helpful assistant. Use the following document excerpts to answer the question.

{context_block}

Q: {query}
A:"""

    try:
        chat = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        answer = chat.choices[0].message.content.strip()
    except Exception as e:
        return {"error": f"OpenAI completion failed: {str(e)}"}

    return {
        "answer": answer if answer else "No meaningful answer generated.",
        "sources": [m.metadata.get("filename", "N/A") for m in matches]
    }
