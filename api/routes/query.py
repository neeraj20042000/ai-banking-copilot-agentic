from fastapi import APIRouter
from api.schemas.request import QueryRequest
from api.schemas.response import QueryResponse

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
def process_query(request: QueryRequest):
    
    # Step 1: Extract user input
    user_query = request.query
    user_id = request.user_id

    # Step 2: Placeholder logic (will be replaced by agents)
    response_text = f"Processed query: {user_query}"

    # Step 3: Return structured response
    return QueryResponse(
        response=response_text,
        agent_used="basic-placeholder-agent"
    )