import os
from openai import OpenAI
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI and Pinecone clients
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))
embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

def answer_question(query: str, user_id: str = "guest", doc_id: str = None):
    # Step 1: Embed the query
    try:
        embedding = client.embeddings.create(
            input=[query],
            model=embedding_model
        ).data[0].embedding
    except Exception as e:
        return {"error": f"Embedding failed: {str(e)}"}

    # Step 2: Query Pinecone with optional filtering
    try:
        query_filter = {"user_id": user_id}
        if doc_id:
            query_filter["doc_id"] = doc_id

        results = index.query(
            vector=embedding,
            top_k=5,
            include_metadata=True,
            filter=query_filter
        )

        matches = results.matches or []
        contexts = [f"{m.metadata.get('title', '')}\n{m.metadata.get('url', '')}" for m in matches]
        context_block = "\n\n".join(contexts) if contexts else "No matching context found."

    except Exception as e:
        return {"error": f"Pinecone query failed: {str(e)}"}

    # Step 3: Generate answer using GPT
    prompt = f"""You are a helpful assistant. Use the following documentation snippets to answer the question as accurately as possible.

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
        "answer": answer,
        "sources": contexts
    }
