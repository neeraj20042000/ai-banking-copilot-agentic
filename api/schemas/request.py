from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=500)
    user_id: str = Field(default="test_user", min_length=3)