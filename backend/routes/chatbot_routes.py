"""
chatbot_routes.py — FastAPI router for DriveBot

Responsibilities:
  - Define request/response Pydantic models
  - Expose the /chat and /health endpoints
  - Translate service-layer errors into appropriate HTTP responses
  - Wire the router into the main FastAPI app (see main.py)

Usage in main.py:
    from fastapi import FastAPI
    from backend.routes.chatbot_routes import router as chatbot_router
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI(title="DriveBot API")
    app.add_middleware(CORSMiddleware, allow_origins=["*"],
                       allow_methods=["*"], allow_headers=["*"])
    app.include_router(chatbot_router)
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, field_validator
from typing import Literal
from groq import AuthenticationError, RateLimitError, APIStatusError, APIConnectionError

from backend.services.chatbot_service import get_chat_reply

router = APIRouter(prefix="", tags=["chatbot"])


# ── Pydantic models ───────────────────────────────────────────────────────────

class Message(BaseModel):
    """A single turn in the conversation."""
    role: Literal["user", "assistant"]
    content: str

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Message content must not be empty.")
        return v


class ChatRequest(BaseModel):
    """Request body for POST /chat."""
    messages: list[Message]

    @field_validator("messages")
    @classmethod
    def at_least_one_message(cls, v: list) -> list:
        if not v:
            raise ValueError("The messages list must contain at least one message.")
        if v[-1].role != "user":
            raise ValueError("The last message must be from the user.")
        return v


class ChatResponse(BaseModel):
    """Response body for POST /chat."""
    reply: str


class HealthResponse(BaseModel):
    """Response body for GET /health."""
    status: str
    bot: str


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Send a message and receive a driving-assistance reply",
)
async def chat(req: ChatRequest) -> ChatResponse:
    """
    Accepts the full conversation history and returns the next assistant reply.

    - **messages**: ordered list of user/assistant turns; last must be 'user'.
    """
    # Convert Pydantic models → plain dicts for the service layer
    history = [{"role": m.role, "content": m.content} for m in req.messages]

    try:
        reply = get_chat_reply(history)
    except AuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Groq API key. Set the GROQ_API_KEY environment variable.",
        )
    except RateLimitError:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Groq rate limit reached. Please wait a moment and try again.",
        )
    except APIStatusError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Groq API error {exc.status_code}: {exc.message}",
        )
    except APIConnectionError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not reach the Groq API. Check your network connection.",
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        )

    return ChatResponse(reply=reply)


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
)
async def health() -> HealthResponse:
    """Returns 200 OK when the service is up."""
    return HealthResponse(status="ok", bot="DriveBot")