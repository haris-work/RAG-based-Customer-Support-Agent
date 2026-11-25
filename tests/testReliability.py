
import uuid
import requests

from unittest.mock import patch
from fastapi.testclient import TestClient

from main import app

from services.ticketService import (
    GetSupportTicket,
    GetNotificationAttempts
)


client = TestClient(app)


def TestGroqFailure():

    print("\nTEST 1: Groq API failure")

    with patch(
        "services.intentClassifierService.ChatGroq",
        side_effect=RuntimeError(
            "Simulated Groq service failure"
        )
    ):

        response = client.post(
            "/api/chat",
            json={
                "message": "What is your return policy?"
            }
        )

    assert response.status_code == 503

    assert "temporarily unavailable" in (
        response.json()["detail"].lower()
    )

    assert "Simulated Groq" not in response.text

    print("PASS: Safe API error returned")


def TestChromaFailure():

    print("\nTEST 2: ChromaDB failure")

    with patch(
        "agents.customerSupportAgent.ClassifyIntent",
        return_value="policy_inquiry"
    ), patch(
        "services.vectorStoreService.GetCollection",
        side_effect=RuntimeError(
            "Simulated ChromaDB failure"
        )
    ):

        response = client.post(
            "/api/chat",
            json={
                "message": "How long does shipping take?"
            }
        )

    assert response.status_code == 503

    assert "Simulated ChromaDB" not in response.text

    print("PASS: Database error handled safely")


def TestWebhookFailure():

    print("\nTEST 3: n8n webhook failure")

    conversation_id = str(uuid.uuid4())

    with patch(
        "agents.customerSupportAgent.ClassifyIntent",
        return_value="human_support"
    ), patch(
        "services.webhookNotificationService.requests.post",
        side_effect=requests.ConnectionError(
            "Simulated n8n connection failure"
        )
    ):

        response = client.post(
            "/api/chat",
            json={
                "message": (
                    "I want to speak with a human "
                    "representative."
                ),
                "conversation_id": conversation_id
            }
        )

    assert response.status_code == 200

    result = response.json()

    assert result["status"] == "needs_review"
    assert result["ticket_id"] is not None

    ticket_id = result["ticket_id"]

    ticket = GetSupportTicket(ticket_id)

    assert ticket is not None
    assert ticket["status"] == "pending"

    attempts = GetNotificationAttempts(ticket_id)

    assert len(attempts) >= 1

    assert attempts[0]["delivery_status"] == "failed"

    print("PASS: Ticket preserved")
    print("Ticket ID:", ticket_id)
    print("Notification status: failed")


def TestUnauthorizedAccess():

    print("\nTEST 4: Unauthorized admin access")

    response = client.get("/api/tickets")

    assert response.status_code == 401

    response = client.get(
        "/api/tickets",
        headers={
            "X-Admin-Key": "incorrect-development-key"
        }
    )

    assert response.status_code == 401

    print("PASS: Unauthorized access rejected")


def TestInvalidInput():

    print("\nTEST 5: Invalid customer input")

    response = client.post(
        "/api/chat",
        json={"message": " "}
    )

    assert response.status_code == 422

    response = client.post(
        "/api/chat",
        json={"message": "A" * 2001}
    )

    assert response.status_code == 422

    print("PASS: Invalid input rejected")


def TestReliability():

    print("=" * 65)
    print("NOVATECH RELIABILITY TEST SUITE")
    print("=" * 65)

    TestGroqFailure()
    TestChromaFailure()
    TestWebhookFailure()
    TestUnauthorizedAccess()
    TestInvalidInput()

    print("\n" + "=" * 65)
    print("ALL RELIABILITY TESTS PASSED")
    print("=" * 65)


if __name__ == "__main__":
    TestReliability()
