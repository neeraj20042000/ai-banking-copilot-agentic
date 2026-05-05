from sentence_transformers import SentenceTransformer
import tiktoken

# Load HuggingFace model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def count_tokens(text: str, encoder: tiktoken.Encoding) -> int:
    """Count tokens in text using tiktoken."""
    return len(encoder.encode(text))


def chunk_text(text: str, chunk_size: int = 200, overlap: int = 30) -> list[str]:
    """
    Split text into overlapping token-based chunks.

    Args:
        text: Input text to chunk
        chunk_size: Max tokens per chunk
        overlap: Number of overlapping tokens between chunks

    Returns:
        List of cleaned text chunks
    """
    if not text or not text.strip():
        return []

    # Use cl100k_base encoding (GPT-4, GPT-3.5 Turbo)
    encoder = tiktoken.get_encoding("cl100k_base")

    # Encode entire text to tokens
    tokens = encoder.encode(text.strip())
    chunks = []

    # Split tokens into chunks
    start = 0
    total_tokens = len(tokens)

    while start < total_tokens:
        end = min(start + chunk_size, total_tokens)

        chunk_tokens = tokens[start:end]
        chunk_text = encoder.decode(chunk_tokens).strip()

        if chunk_text:
            chunks.append(chunk_text)

        # Move window with overlap
        if end == total_tokens:
            break

        start = end - overlap

        # Safety guard to avoid infinite loops.
        if start < 0 or start >= total_tokens:
            break

    return chunks


def get_embedding(text: str) -> list[float]:
    """
    Generate embedding for a single text (used in queries)
    """
    text = text.strip()

    if not text:
        return []

    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding.tolist()


def get_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for multiple texts (used in indexing)
    """
    if not texts:
        return []

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return embeddings.tolist()
