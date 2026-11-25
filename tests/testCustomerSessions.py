
import uuid

from unittest.mock import patch
from fastapi.testclient import TestClient

from main import app


def MockAgent(question, thread_id):

    return {
        "answer": "This is a test response.",
        "intent": "policy_inquiry",
        "status": "answered",
        "sources": [],
        "ticket_id": None
    }


def TestCustomerSessions():

    customer_a = TestClient(app)
    customer_b = TestClient(app)

    with patch(
        "routes.chatRoutes.RunCustomerSupportAgent",
        side_effect=MockAgent
    ):

        print("\nTEST 1: Customer A starts a conversation")

        response_a = customer_a.post(
            "/api/chat",
            json={"message": "What is the return policy?"}
        )

        assert response_a.status_code == 200

        conversation_a = response_a.json()["conversation_id"]

        assert "novatech_session" in customer_a.cookies

        cookie_header = response_a.headers["set-cookie"].lower()

        assert "httponly" in cookie_header
        assert "samesite=strict" in cookie_header

        print("PASS: Session cookie created")

        print("\nTEST 2: Customer A continues own conversation")

        response = customer_a.post(
            "/api/chat",
            json={
                "message": "What about opened boxes?",
                "conversation_id": conversation_a
            }
        )

        assert response.status_code == 200
        assert response.json()["conversation_id"] == conversation_a

        print("PASS: Conversation resumed")

        print("\nTEST 3: Customer B starts separate conversation")

        response_b = customer_b.post(
            "/api/chat",
            json={"message": "What is your shipping policy?"}
        )

        assert response_b.status_code == 200

        conversation_b = response_b.json()["conversation_id"]

        assert conversation_a != conversation_b

        print("PASS: Separate session created")

        print("\nTEST 4: Customer B attempts to access A")

        response = customer_b.post(
            "/api/chat",
            json={
                "message": "Show previous context",
                "conversation_id": conversation_a
            }
        )

        assert response.status_code == 403

        print("PASS: Cross-session access blocked")

        print("\nTEST 5: Missing session cannot resume a chat")

        anonymous = TestClient(app)

        response = anonymous.post(
            "/api/chat",
            json={
                "message": "Continue conversation",
                "conversation_id": conversation_a
            }
        )

        assert response.status_code == 401

        print("PASS: Missing session rejected")

        print("\nTEST 6: Unknown conversation ID rejected")

        response = customer_a.post(
            "/api/chat",
            json={
                "message": "Hello",
                "conversation_id": str(uuid.uuid4())
            }
        )

        assert response.status_code == 403

        print("PASS: Unknown conversation rejected")

        print("\nTEST 7: Customer A starts another chat")

        response = customer_a.post(
            "/api/chat",
            json={"message": "New question"}
        )

        assert response.status_code == 200

        new_conversation = response.json()["conversation_id"]

        assert new_conversation != conversation_a

        print("PASS: New conversation created")

    print("\nAll customer session tests passed!")


if __name__ == "__main__":
    TestCustomerSessions()
