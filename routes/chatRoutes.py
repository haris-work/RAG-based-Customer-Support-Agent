
import os
import uuid

from typing import Literal

from fastapi import (
    APIRouter,
    HTTPException,
    Request,
    Response
)

from pydantic import BaseModel, Field

from agents.customerSupportAgent import RunCustomerSupportAgent

from services.customerSessionService import (
    CreateCustomerSession,
    GetCustomerSession,
    CreateCustomerConversation,
    OwnsConversation,
    SESSION_LIFETIME
)


router = APIRouter(
    prefix="/api/chat",
    tags=["Customer Chat"]
)

COOKIE_NAME = "novatech_session"


class ChatRequest(BaseModel):

    message: str = Field(
        min_length=1,
        max_length=2000
    )

    conversation_id: uuid.UUID | None = None


class ChatSource(BaseModel):

    reference: int
    file: str
    section: str


class ChatResponse(BaseModel):

    conversation_id: uuid.UUID
    answer: str
    intent: str
    status: Literal[
        "answered",
        "needs_review"
    ]
    sources: list[ChatSource]
    ticket_id: str | None = None


@router.post("", response_model=ChatResponse)
def CustomerChat(
    chat: ChatRequest,
    request: Request,
    response: Response
):

    message = chat.message.strip()

    if not message:
        raise HTTPException(
            status_code=422,
            detail="Message cannot be empty"
        )

    token = request.cookies.get(COOKIE_NAME)

    session_id = GetCustomerSession(token)

    new_session_token = None

    if session_id is None:

        # An expired or unknown session cannot
        # claim an existing conversation.
        if chat.conversation_id is not None:
            raise HTTPException(
                status_code=401,
                detail="Customer session expired or missing"
            )

        session = CreateCustomerSession()

        session_id = session["session_id"]
        new_session_token = session["token"]

    if chat.conversation_id is None:

        conversation_id = CreateCustomerConversation(
            session_id
        )

    else:

        conversation_id = str(chat.conversation_id)

        if not OwnsConversation(
            session_id,
            conversation_id
        ):
            raise HTTPException(
                status_code=403,
                detail="Conversation access denied"
            )

    try:

        result = RunCustomerSupportAgent(
            question=message,
            thread_id=conversation_id
        )

    except Exception:

        raise HTTPException(
            status_code=503,
            detail=(
                "The support service is temporarily "
                "unavailable. Please try again later."
            )
        )

    if new_session_token is not None:

        response.set_cookie(
            key=COOKIE_NAME,
            value=new_session_token,
            max_age=SESSION_LIFETIME,
            httponly=True,
            secure=os.getenv(
                "COOKIE_SECURE", "false"
            ).lower() == "true",
            samesite="strict",
            path="/"
        )

    return ChatResponse(
        conversation_id=uuid.UUID(conversation_id),
        answer=result["answer"],
        intent=result["intent"],
        status=result["status"],
        sources=result.get("sources", []),
        ticket_id=result.get("ticket_id")
    )
