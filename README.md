# 🚀 GenAI Banking Copilot

GenAI Banking Copilot is an agentic banking assistant built to handle financial questions, loan assessments, risk evaluation, and personalized recommendations with a structured AI workflow.

The project combines a lightweight FastAPI backend, Streamlit frontend, a modular LangGraph agent pipeline, RAG grounding with ChromaDB, and both short-term and long-term memory support.

---

## 📖 What this project does

This system is designed to simulate a practical, production-style banking AI assistant by:

- Classifying user intent into loan-related or recommendation-related requests.
- Running specialized agents for loan calculation, risk evaluation, and recommendation generation.
- Using retrieval-augmented generation to ground answers in domain knowledge from indexed documents.
- Persisting conversation history and session takeaways for better context over time.
- Applying safety checks and compliance disclaimers before returning a final response.

---

## 🧠 How it works

1. **User query arrives via frontend**
   - The Streamlit app sends POST requests to `http://localhost:8000/query`.

2. **Backend builds initial agent state**
   - `api.routes.query.process_query` loads short-term and long-term memory.
   - It injects recent conversation history and user profile context into the agent state.

3. **Agent pipeline executes**
   - `agents.orchestrator.build_graph` creates an execution graph using `langgraph`.
   - Agents are executed in order, and each step stores state snapshots for progress tracking.

4. **Guardrail & intent detection**
   - `agents.guardrail_agent` is injected early in the pipeline to ensure the query is safe before any business logic runs.
   - `agents.intent_agent` classifies the query as `loan` or `recommendation`.

5. **Loan or recommendation flow**
   - If intent is `loan`, `agents.loan_agent` extracts loan parameters and calculates eligibility.
   - `agents.risk_agent` evaluates credit risk.
   - If intent is `recommendation`, `agents.rag_agent` retrieves context from the document store and `agents.recommendation_agent` generates advice.

6. **Compliance step**
   - `agents.compliance_agent` validates the final response and adds a compliance disclaimer.
   - It also checks for banned content using `guardrails.moderation`.

7. **Memory persistence**
   - Conversation turns are stored in short-term memory.
   - Extracted keywords and takeaways are appended to long-term memory.

---

##  Pipeline overview

```
ai-banking-copilot-agentic/
├── api/
│   ├── main.py                # FastAPI app entrypoint
│   ├── routes/
│   │   ├── health.py          # Health check route
│   │   ├── query.py           # Query processing and agent orchestration
│   ├── schemas/
│   │   ├── request.py         # Request validation model
│   │   ├── response.py        # Response model definitions
├── agents/
│   ├── orchestrator.py        # LangGraph execution graph
│   ├── intent_agent.py        # Intent classification logic
│   ├── loan_agent.py          # Loan extraction and eligibility
│   ├── risk_agent.py          # Risk evaluation logic
│   ├── recommendation_agent.py# Response generation and memory extraction
│   ├── compliance_agent.py    # Safety, disclaimer, and compliance step
│   ├── rag_agent.py           # Document retrieval and RAG context
│   ├── llm.py                 # LLM API wrapper
│   ├── state.py               # Shared agent state type
├── rag/
│   ├── embeddings.py          # Embeddings and chunking utilities
│   ├── vector_store.py        # ChromaDB storage and retrieval
├── memory/
│   ├── short_term.py          # Ephemeral conversation memory
│   ├── long_term.py           # Persistent user profile and keywords
├── guardrails/
│   ├── compliance.py          # Disclaimer and output compliance
│   ├── moderation.py          # Basic toxicity checks
├── frontend/
│   ├── app.py                 # Streamlit user interface
├── tools/
│   ├── loan_calculator.py     # Loan calculation utilities
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## 🧪 Key features

- **Agentic orchestration** using `langgraph` with explicit state tracking.
- **RAG grounding** through ChromaDB and HuggingFace embeddings.
- **Persistent memory** via JSON-backed user profile storage.
- **Loan-focused intelligence**: extraction, eligibility, and risk scoring.
- **Safety layer** with content moderation and compliance disclaimers.
- **Progress tracking**: backend returns agent state history for debugging and UI display.

---

## ⚙️ Dependencies

The main runtime dependencies used by this project include:

- `fastapi`
- `streamlit`
- `groq`
- `langgraph`
- `chromadb`
- `sentence-transformers`
- `tiktoken`
- `pypdf`
- `python-dotenv`
- `pydantic`
- `requests`

---

## 🚀 Getting started

1. Create and activate your virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set environment variables in a `.env` file if needed:

```bash
GROQ_API_KEY=your_groq_api_key
BACKEND_URL=http://localhost:8000/query
```

4. Start the backend API:

```bash
uvicorn api.main:app --reload
```

5. Run the frontend app:

```bash
streamlit run frontend/app.py
```

6. Open the Streamlit UI in your browser and start sending banking queries.

---

## 📌 Example use cases

- Calculate loan eligibility from user-provided or inferred values.
- Evaluate credit risk and explain potential issues.
- Generate personalized banking recommendations with memory-aware context.
- Retrieve financial knowledge from indexed PDF documents.
- Keep conversational context across short-term sessions and long-term user profiles.

---

## 📝 Notes

- The current guardrail system is intentionally simple and can be extended for stronger moderation.
- Long-term memory is persisted to `memory/user_memory.json`.
- Document indexing is performed via `rag/vector_store.py` and the ChromaDB collection at `./chroma_db`.

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome. Please open issues or submit pull requests to improve the banking copilot.
