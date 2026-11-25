
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from services.ticketService import (
    GetSupportTicket,
    RecordNotificationAttempt
)


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def NotifySupportWebhook(ticket_id):

    ticket = GetSupportTicket(ticket_id)

    if ticket is None:
        raise ValueError("Support ticket not found")

    webhook_url = os.getenv("N8N_SUPPORT_WEBHOOK_URL")

    webhook_secret = os.getenv("N8N_WEBHOOK_SECRET")

    if not webhook_url:
        RecordNotificationAttempt(
            ticket_id=ticket_id,
            delivery_status="not_configured"
        )

        return {
            "ticket_id": ticket_id,
            "delivery_status": "not_configured",
            "http_status": None
        }

    payload = {
        "ticket_id": ticket["ticket_id"],
        "thread_id": ticket["thread_id"],
        "customer_message": ticket["customer_message"],
        "intent": ticket["intent"],
        "status": ticket["status"],
        "created_at": ticket["created_at"]
    }

    delivery_status = "unconfirmed"
    http_status = None
    error_message = None


    if not webhook_secret:

        RecordNotificationAttempt(
            ticket_id=ticket_id,
            delivery_status="not_configured",
            error_message="Webhook authentication is not configured"
        )

        return {
            "ticket_id": ticket_id,
            "delivery_status": "not_configured",
            "http_status": None
        }

    try:
        response = requests.post(
            webhook_url,
            json=payload,
            headers={
                "X-NovaTech-Webhook-Key": webhook_secret
            },
            timeout=30
        )

        http_status = response.status_code

        response.raise_for_status()

        try:
            data = response.json()
        except ValueError:
            data = {}

        if (
            isinstance(data, dict)
            and data.get("ticket_id") == ticket_id
            and data.get("delivery_status") == "sent"
        ):
            delivery_status = "sent"
        else:
            delivery_status = "unconfirmed"
            error_message = (
                "Webhook acknowledged without "
                "matching Gmail send confirmation"
            )

    except requests.RequestException as error:

        delivery_status = "failed"

        error_response = getattr(
            error,
            "response",
            None
        )

        if error_response is not None:
            http_status = error_response.status_code

        error_message = str(error)[:500]

    RecordNotificationAttempt(
        ticket_id=ticket_id,
        delivery_status=delivery_status,
        http_status=http_status,
        error_message=error_message
    )

    return {
        "ticket_id": ticket_id,
        "delivery_status": delivery_status,
        "http_status": http_status
    }
