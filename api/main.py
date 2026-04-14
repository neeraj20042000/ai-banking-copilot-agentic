# Import FastAPI framework
from fastapi import FastAPI
from api.routes import health, query


# Create an instance of FastAPI application
app = FastAPI(
    title="GenAI Banking Copilot API",
    description="Backend API for Agentic AI Banking System",
    version="1.0.0"
)

# Root endpoint for basic health check
@app.get("/")
def read_root():
    return {
        "status": "success",
        "message": "AI Banking Copilot API is running"
    }

# Include route modules
app.include_router(health.router)
app.include_router(query.router)
