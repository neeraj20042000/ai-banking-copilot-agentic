from agents.state import AgentState
from rag.retriever import retrieve_docs


def rag_agent(state: AgentState) -> AgentState:
    """Retrieve relevant docs and attach the RAG context to the shared state."""
    query = state.get("query", "")
    
    # Use memory context injected via state (modular approach)
    short_term_context = state.get("short_term_context", "")
    
    # Enhance query with conversation context if available
    if short_term_context:
        enhanced_query = f"{query}\n\nRecent conversation:\n{short_term_context}"
    else:
        enhanced_query = query
    
    docs = retrieve_docs(enhanced_query)
    state["rag_context"] = "\n".join(docs)
    return state
