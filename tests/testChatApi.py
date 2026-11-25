
from uuid import UUID
from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def TestChatApi():

    calls = []

    def MockAgent(question, thread_id):

        calls.append({
            "question": question,
            "thread_id": thread_id
        })

        if "human" in question.lower():
            return {
                "answer": "Your support ticket was created.",
                "intent": "human_support",
                "status": "needs_review",
                "sources": [],
                "ticket_id": "NT-TEST123456"
            }

        return {
            "answer": "Standard delivery takes 5–7 business days.",
            "intent": "policy_inquiry",
            "status": "answered",
            "sources": [{
                "reference": 1,
                "file": "06_shipping_policy.md",
                "section": "Standard shipping"
            }],
            "ticket_id": None
        }

    with patch(
        "routes.chatRoutes.RunCustomerSupportAgent",
        side_effect=MockAgent
    ):

        print("\nTEST 1: New conversation")

        response = client.post(
            "/api/chat",
            json={
                "message": "How long does shipping take?"
            }
        )

        assert response.status_code == 200

        data = response.json()
        conversation_id = data["conversation_id"]

        UUID(conversation_id)

        assert data["status"] == "answered"
        assert len(data["sources"]) == 1
        assert data["ticket_id"] is None

        print("PASS: Conversation created")

        print("\nTEST 2: Conversation continuity")

        response = client.post(
            "/api/chat",
            json={
                "message": "What about delays?",
                "conversation_id": conversation_id
            }
        )

        assert response.status_code == 200
        assert response.json()["conversation_id"] == conversation_id
        assert calls[0]["thread_id"] == calls[1]["thread_id"]

        print("PASS: Conversation ID preserved")

        print("\nTEST 3: Human escalation")

        response = client.post(
            "/api/chat",
            json={
                "message": "I want to speak to a human."
            }
        )

        assert response.status_code == 200
        assert response.json()["status"] == "needs_review"
        assert response.json()["ticket_id"] == "NT-TEST123456"

        print("PASS: Ticket reference returned")

        print("\nTEST 4: Empty message")

        response = client.post(
            "/api/chat",
            json={"message": "   "}
        )

        assert response.status_code == 422

        print("PASS: Empty message rejected")

        print("\nTEST 5: Invalid conversation ID")

        response = client.post(
            "/api/chat",
            json={
                "message": "Hello",
                "conversation_id": "invalid-id"
            }
        )

        assert response.status_code == 422

        print("PASS: Invalid ID rejected")

    print("\nAll chat API tests passed!")


if __name__ == "__main__":
    TestChatApi()
