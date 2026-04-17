from rag.vector_store import load_documents, index_documents

docs = load_documents("rag/data/banking_docs.txt")
index_documents(docs)

print("✅ Documents indexed successfully!")