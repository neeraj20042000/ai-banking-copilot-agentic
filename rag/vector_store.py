import chromadb
from chromadb.config import Settings
from rag.embeddings import get_embeddings, get_embedding
import uuid

# Initialize persistent client
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="banking_knowledge"
)


def load_documents(file_path: str):
    """
    Load and clean documents
    """
    with open(file_path, "r", encoding="utf-8") as file:
        docs = file.readlines()

    return [doc.strip() for doc in docs if doc.strip()]


def index_documents(docs):
    """
    Efficient batch indexing
    """
    ids = [str(uuid.uuid4()) for _ in docs]
    embeddings = get_embeddings(docs)

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=docs,
        metadatas=[{"source": "banking_docs"} for _ in docs]
    )

def query_documents(query: str, n_results: int = 3):
    """
    Retrieve similar documents
    """
    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "distances", "metadatas"]
    )

    return {
        "documents": results["documents"][0],
        "scores": results["distances"][0],
        "metadata": results.get("metadatas", [[]])[0]
    }