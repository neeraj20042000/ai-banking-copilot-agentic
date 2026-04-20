from rag.vector_store import query_documents

def retrieve_docs(query: str):
    results = query_documents(query)

    return results["documents"]