from pydantic import BaseModel
from typing import Optional
class QueryResponse(BaseModel):
    answer: str
    status: str = "success"
    source: Optional[str] = None