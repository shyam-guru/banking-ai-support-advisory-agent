"""
Phase 8 - Banking AI REST API

Read-only deployment interface for the Banking AI
Support & Advisory Agent.

No transaction execution endpoints are provided.
"""

import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from phase7_agent import Phase7BankingAgent


# ============================================================
# Application
# ============================================================

app = FastAPI(
    title="Banking AI Support & Advisory Agent",
    description=(
        "Non-transactional banking support and advisory API."
    ),
    version="1.0.0",
)


# ============================================================
# Safe operational logging
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("banking_ai")


# ============================================================
# Agent initialization
# ============================================================

agent = Phase7BankingAgent()


# ============================================================
# Request model
# ============================================================

class ChatRequest(BaseModel):
    question: str


# ============================================================
# Response model
# ============================================================

class ChatResponse(BaseModel):
    route: str
    answer: str
    response_style: str


# ============================================================
# Health endpoint
# ============================================================

@app.get("/health")
def health():
    """
    Basic service health check.
    """

    return {
        "status": "healthy",
        "service": "banking-ai-support-agent",
        "version": "1.0.0",
    }


# ============================================================
# Readiness endpoint
# ============================================================

@app.get("/ready")
def ready():
    """
    Report deployment capabilities.

    The application deliberately exposes no transaction
    execution capability.
    """

    return {
        "status": "ready",
        "rag_available": True,
        "read_only_tools_available": True,
        "transaction_execution": False,
    }


# ============================================================
# Chat endpoint
# ============================================================

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Process a non-transactional banking support question.
    """

    question = request.question.strip()

    # --------------------------------------------------------
    # Input validation
    # --------------------------------------------------------

    if not question:

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:

        # IMPORTANT:
        # Do not log the actual user question.
        #
        # This prevents accidental PII or sensitive
        # authentication information from entering logs.

        logger.info(
            "Chat request received | question_length=%d",
            len(question),
        )

        # ----------------------------------------------------
        # Existing Phase 7 agent
        # ----------------------------------------------------

        result = agent.ask(question)

        logger.info(
            "Chat request completed | route=%s",
            result.get("route"),
        )

        return ChatResponse(
            route=result.get("route", "UNKNOWN"),
            answer=result.get("adapted_answer", ""),
            response_style=result.get(
                "response_style",
                "standard",
            ),
        )

    except Exception as exc:

        # Log only the exception type rather than the
        # user's question or potentially sensitive content.

        logger.exception(
            "Chat request failed | error_type=%s",
            type(exc).__name__,
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "The banking support service could not "
                "complete the request."
            ),
        )