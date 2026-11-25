
import os
import uuid

from dotenv import load_dotenv
from fastapi.testclient import TestClient

from main import app

from services.ticketService import (
    GetSupportTicket,
    GetNotificationAttempts
)


load_dotenv()

client = TestClient(app)


def TestEndToEnd():

    admin_key = os.getenv("ADMIN_API_KEY")

    if not admin_key:
        raise RuntimeError(
            "ADMIN_API_KEY is missing from .env"
        )

    headers = {
        "X-Admin-Key": admin_key
    }

    print("\n" + "=" * 65)
    print("TEST 1: CUSTOMER ASKS A POLICY QUESTION")
    print("=" * 65)

    response = client.post(
        "/api/chat",
        json={
            "message": (
                "How long does standard shipping take?"
            )
        }
    )

    assert response.status_code == 200, response.text

    chat = response.json()

    assert chat["conversation_id"]
    assert chat["answer"]
    assert chat["intent"] == "policy_inquiry"

    print("Intent:", chat["intent"])
    print("Status:", chat["status"])
    print("Answer:", chat["answer"])
    print("Sources:", chat["sources"])

    # Model-answer quality is inspected separately.
    # This test verifies the API integration.

    print("\n" + "=" * 65)
    print("TEST 2: CUSTOMER REQUESTS HUMAN SUPPORT")
    print("=" * 65)

    response = client.post(
        "/api/chat",
        json={
            "message": (
                "I want to speak to a human "
                "representative about my order."
            )
        }
    )

    assert response.status_code == 200, response.text

    escalation = response.json()

    assert escalation["intent"] == "human_support"
    assert escalation["status"] == "needs_review"
    assert escalation["ticket_id"] is not None

    ticket_id = escalation["ticket_id"]

    print("Ticket ID:", ticket_id)
    print("Answer:", escalation["answer"])

    print("\n" + "=" * 65)
    print("TEST 3: VERIFY SQLITE TICKET")
    print("=" * 65)

    ticket = GetSupportTicket(ticket_id)

    assert ticket is not None
    assert ticket["status"] == "pending"

    print("Ticket saved:", ticket["ticket_id"])
    print("Status:", ticket["status"])

    print("\n" + "=" * 65)
    print("TEST 4: VERIFY WEBHOOK ATTEMPT")
    print("=" * 65)

    attempts = GetNotificationAttempts(ticket_id)

    assert len(attempts) >= 1

    latest_attempt = attempts[0]

    print(
        "Notification status:",
        latest_attempt["delivery_status"]
    )

    print(
        "HTTP status:",
        latest_attempt["http_status"]
    )

    assert latest_attempt["delivery_status"] == "sent", (
        "n8n did not acknowledge the webhook"
    )

    print("\n" + "=" * 65)
    print("TEST 5: ADMINISTRATOR RETRIEVES TICKET")
    print("=" * 65)

    response = client.get(
        f"/api/tickets/{ticket_id}",
        headers=headers
    )

    assert response.status_code == 200

    assert response.json()["ticket_id"] == ticket_id

    print("Administrator retrieved ticket")

    print("\n" + "=" * 65)
    print("TEST 6: ADMINISTRATOR STARTS WORK")
    print("=" * 65)

    response = client.patch(
        f"/api/tickets/{ticket_id}/status",
        headers=headers,
        json={
            "status": "in_progress"
        }
    )

    assert response.status_code == 200
    assert (
        response.json()["ticket"]["status"]
        == "in_progress"
    )

    print("Ticket status: in_progress")

    print("\n" + "=" * 65)
    print("TEST 7: ADMINISTRATOR RESOLVES TICKET")
    print("=" * 65)

    response = client.patch(
        f"/api/tickets/{ticket_id}/status",
        headers=headers,
        json={
            "status": "resolved"
        }
    )

    assert response.status_code == 200

    updated = GetSupportTicket(ticket_id)

    assert updated["status"] == "resolved"

    print("Ticket status:", updated["status"])

    print("\n" + "=" * 65)
    print("TEST 8: UNAUTHORIZED ACCESS")
    print("=" * 65)

    response = client.get(
        f"/api/tickets/{ticket_id}"
    )

    assert response.status_code == 401

    print("Unauthorized request rejected")

    print("\n" + "=" * 65)
    print("END-TO-END TEST RESULTS")
    print("=" * 65)

    print("Customer Chat API: PASS")
    print("LangGraph routing: PASS")
    print("SQLite ticket creation: PASS")
    print("n8n webhook acknowledgment: PASS")
    print("Admin ticket retrieval: PASS")
    print("Ticket lifecycle: PASS")
    print("Administrator authentication: PASS")

    print("\nEnd-to-end API integration test passed!")
    print(
        "Verify the Gmail message separately "
        "in n8n and your test inbox."
    )


if __name__ == "__main__":
    TestEndToEnd()
