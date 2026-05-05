import re
import uuid

import chromadb
from pypdf import PdfReader

from rag.embeddings import get_embedding, get_embeddings, chunk_text


CHROMA_DB_PATH = "./chroma_db"

client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_or_create_collection(
    name="banking_knowledge",
    metadata={"description": "Banking knowledge base with chunked documents"},
)


def clear_collection():
    """
    Delete all documents from the collection for re-indexing.
    """
    try:
        client.delete_collection(name="banking_knowledge")
        global collection
        collection = client.get_or_create_collection(
            name="banking_knowledge",
            metadata={"description": "Banking knowledge base with chunked documents"},
        )
        print("Collection cleared successfully")
    except Exception as e:
        print(f"Error clearing collection: {e}")


def clean_text(text: str) -> str:
    """
    Normalize whitespace in extracted text.
    """
    if not text:
        return ""

    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)

    return text.strip()


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract and clean text from a PDF file.
    """
    reader = PdfReader(pdf_path)
    pages = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            pages.append(page_text)

    raw_text = "\n".join(pages)
    return clean_text(raw_text)


def load_and_chunk_documents(file_path: str) -> list[str]:
    """
    Load a PDF document and split it into overlapping chunks.

    Args:
        file_path: Path to the document

    Returns:
        List of chunked text segments
    """
    text = extract_text_from_pdf(file_path)
    chunks = chunk_text(text)

    print(f"Extracted {len(text)} characters into {len(chunks)} chunks")

    return chunks


def index_documents(docs: list[str], source_name: str = "document"):
    """
    Efficient batch indexing with chunked documents.

    Args:
        docs: List of text chunks to index
        source_name: Source identifier for metadata
    """
    if not docs:
        print("No documents to index")
        return

    ids = [str(uuid.uuid4()) for _ in docs]
    embeddings = get_embeddings(docs)
    metadatas = [
        {
            "source": source_name,
            "chunk_index": i,
            "total_chunks": len(docs),
        }
        for i in range(len(docs))
    ]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=docs,
        metadatas=metadatas,
    )

    print(f"Indexed {len(docs)} document chunks")


def query_documents(query: str, n_results: int = 3):
    """
    Retrieve similar documents.

    Args:
        query: Query text
        n_results: Number of results to return

    Returns:
        Dictionary with documents, scores, and metadata
    """
    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "distances", "metadatas"],
    )

    return {
        "documents": results["documents"][0],
        "scores": results["distances"][0],
        "metadata": results.get("metadatas", [[]])[0],
    }
