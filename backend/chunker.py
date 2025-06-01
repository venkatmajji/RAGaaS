import tiktoken

# You can set this to match your model (e.g. text-embedding-3-small: 8192 max tokens)
MAX_TOKENS = 750

# Get tokenizer for your embedding model
encoding = tiktoken.encoding_for_model("text-embedding-3-small")

def chunk_text(text: str, max_tokens: int = MAX_TOKENS) -> list[str]:
    """
    Splits the input text into chunks of approximately `max_tokens` tokens each.
    """
    if not isinstance(text, str):
        raise TypeError("Text must be a decoded string, not bytes.")

    tokens = encoding.encode(text)
    total_tokens = len(tokens)

    print(f"[CHUNKER] Total tokens: {total_tokens}, Chunk size: {max_tokens}")

    chunks = [
        encoding.decode(tokens[i:i + max_tokens])
        for i in range(0, total_tokens, max_tokens)
    ]

    print(f"[CHUNKER] Generated {len(chunks)} chunks.")
    return chunks
