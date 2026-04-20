from pydantic import BaseModel
from typing import Optional, List
class QueryResponse(BaseModel):
    answer: str
    status: str = "success"
    source: Optional[str] = None
    retrieved_docs: Optional[List[str]] = None