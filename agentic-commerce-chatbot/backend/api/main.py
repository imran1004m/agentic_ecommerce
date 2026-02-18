from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import uuid
import time
import mlflow

from backend.agents.supervisor import build_graph

# ======================================
# FastAPI App
# ======================================

app = FastAPI(title="Agentic Commerce Chatbot API")

graph = build_graph()

# In-memory session store
sessions: Dict[str, dict] = {}


# ======================================
# Request / Response Models
# ======================================

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    session_id: str
    response: str


# ======================================
# Health Check
# ======================================

@app.get("/")
def health():
    return {"status": "API Running 🚀"}


# ======================================
# Chat Endpoint
# ======================================

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    # Create session if not exists
    if not request.session_id:
        session_id = str(uuid.uuid4())
        sessions[session_id] = {}
    else:
        session_id = request.session_id
        if session_id not in sessions:
            sessions[session_id] = {}

    state = sessions[session_id]

    # Add required fields
    state["session_id"] = session_id
    state["user_input"] = request.message

    # Run LangGraph
    updated_state = graph.invoke(state)

    # Save back to memory
    sessions[session_id] = updated_state

    return ChatResponse(
        session_id=session_id,
        response=updated_state.get("response", "")
    )
