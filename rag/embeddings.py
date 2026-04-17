from sentence_transformers import SentenceTransformer

# Load HuggingFace model once
model = SentenceTransformer("all-MiniLM-L6-v2")


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
    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    return embeddings.tolist()