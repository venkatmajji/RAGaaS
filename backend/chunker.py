import tiktoken

# You can set this to match your model (e.g. text-embedding-3-small: 8192 max tokens)
MAX_TOKENS = 750

# Get tokenizer for your embedding model
encoding = tiktoken.encoding_for_model("text-embedding-3-small")

def chunk_text(text: str, max_tokens: int = MAX_TOKENS) -> list[str]:
    if not isinstance(text, str):
        raise TypeError("Text must be a decoded string, not bytes.")

    tokens = encoding.encode(text)
    total_tokens = len(tokens)

    print(f"[CHUNKER] Total tokens: {total_tokens}, Chunk size: {max_tokens}")

    chunks = []
    for i in range(0, total_tokens, max_tokens):
        token_slice = tokens[i:i + max_tokens]
        try:
            chunk = encoding.decode(token_slice).strip()
        except Exception as e:
            print(f"[CHUNKER] Decode error: {e}")
            continue

        if chunk and len(chunk) > 10:
            chunks.append(chunk)

    print(f"[CHUNKER] Generated {len(chunks)} clean chunks.")
    return chunks

