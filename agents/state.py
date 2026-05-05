from typing import TypedDict, Optional, Dict, Any

class AgentState(TypedDict, total=False):
    query: str
    intent: Optional[str]
    user_data: Optional[Dict[str, Any]]
    loan_result: Optional[Dict]
    risk_result: Optional[str]
    rag_context: Optional[str]
    response: Optional[str]
    # Memory context injected via state for modularity
    short_term_context: Optional[str]  # Conversational history
    long_term_context: Optional[str]   # User profile & preferences
    # Internal graph metadata preserved across execution
    _progress: Optional[list]
    _current_agent: Optional[str]
    _conversation_to_save: Optional[Dict[str, str]]
    _keywords_to_save: Optional[list]
    _takeaway_to_save: Optional[str]
