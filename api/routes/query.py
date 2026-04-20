from fastapi import APIRouter
from api.schemas.request import QueryRequest
from api.schemas.response import QueryResponse
from rag.retriever import retrieve_docs

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
def process_query(request: QueryRequest):
    
    # Step 1: Extract user input
    user_query = request.query
    user_id = request.user_id

    # Step 2: Retrieve relevant docs
    docs = retrieve_docs(user_query)

    # Step 3: Create temporary response (before LLM in Day 6)
    answer = f"Retrieved {len(docs)} relevant documents for your query."

    # Step 4: Return structured response
    return QueryResponse(
        answer=answer,
        retrieved_docs=docs,
        source="vector_db"
    )