
from typing import Literal

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from pydantic import BaseModel

from services.authService import VerifyAdminKey

from services.ticketService import (
    GetAllTickets,
    GetSupportTicket,
    UpdateTicketStatus
)

from services.ticketService import GetTicketAuditHistory


router = APIRouter(
    prefix="/api/tickets",
    tags=["Support Ticket Management"],
    dependencies=[Depends(VerifyAdminKey)]
)


TicketStatus = Literal[
    "pending",
    "in_progress",
    "resolved"
]


class TicketStatusUpdate(BaseModel):
    status: TicketStatus


@router.get("")
def ListTickets(
    status: TicketStatus | None = Query(default=None)
):

    tickets = GetAllTickets(status=status)

    return {
        "total": len(tickets),
        "tickets": tickets
    }


@router.get("/{ticket_id}")
def GetTicket(ticket_id: str):

    ticket = GetSupportTicket(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Support ticket not found"
        )

    return ticket


@router.patch("/{ticket_id}/status")
def ChangeTicketStatus(
    ticket_id: str,
    request: TicketStatusUpdate
):

    existing_ticket = GetSupportTicket(ticket_id)

    if existing_ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Support ticket not found"
        )

    try:
        updated_ticket = UpdateTicketStatus(
            ticket_id,
            request.status,
            actor="admin_api_key"
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    return {
        "message": "Ticket status updated",
        "ticket": updated_ticket
    }




@router.get("/{ticket_id}/history")
def GetTicketHistory(ticket_id: str):

    ticket = GetSupportTicket(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Support ticket not found"
        )

    history = GetTicketAuditHistory(ticket_id)

    return {
        "ticket_id": ticket_id,
        "total_events": len(history),
        "history": history
    }

