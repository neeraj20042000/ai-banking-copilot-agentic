from pydantic import BaseModel, Field
from typing import Optional
class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=500)
    user_id: str = Field(..., min_length=3)
    context: Optional[str] = None