
import os
import secrets

from fastapi.testclient import TestClient

from main import app

from services.ticketService import CreateSupportTicket


def TestTicketApi():

    # Use a temporary administrator key for testing.
    previous_key = os.environ.get("ADMIN_API_KEY")

    test_key = secrets.token_urlsafe(32)
    os.environ["ADMIN_API_KEY"] = test_key

    client = TestClient(app)

    headers = {
        "X-Admin-Key": test_key
    }

    try:
        ticket = CreateSupportTicket(
            thread_id="api_test_customer_001",
            customer_message=(
                "My delivery arrived damaged."
            ),
            intent="order_account"
        )

        ticket_id = ticket["ticket_id"]

        print("\nTEST 1: Unauthorized access")

        response = client.get("/api/tickets")

        assert response.status_code == 401

        print("PASS: Unauthorized request rejected")

        print("\nTEST 2: List tickets")

        response = client.get(
            "/api/tickets",
            headers=headers
        )

        assert response.status_code == 200
        assert response.json()["total"] >= 1

        print("PASS: Ticket list retrieved")

        print("\nTEST 3: Retrieve specific ticket")

        response = client.get(
            f"/api/tickets/{ticket_id}",
            headers=headers
        )

        assert response.status_code == 200
        assert response.json()["ticket_id"] == ticket_id

        print("PASS: Ticket retrieved")

        print("\nTEST 4: Update ticket status")

        response = client.patch(
            f"/api/tickets/{ticket_id}/status",
            headers=headers,
            json={"status": "in_progress"}
        )

        assert response.status_code == 200

        assert (
            response.json()["ticket"]["status"]
            == "in_progress"
        )

        print("PASS: Ticket moved to in_progress")

        print("\nTEST 5: Resolve ticket")

        response = client.patch(
            f"/api/tickets/{ticket_id}/status",
            headers=headers,
            json={"status": "resolved"}
        )

        assert response.status_code == 200

        print("PASS: Ticket resolved")

        print("\nTEST 6: Reject invalid transition")

        response = client.patch(
            f"/api/tickets/{ticket_id}/status",
            headers=headers,
            json={"status": "pending"}
        )

        assert response.status_code == 400

        print("PASS: Invalid transition rejected")

        print("\nTEST 7: Reject invalid API key")

        response = client.get(
            "/api/tickets",
            headers={"X-Admin-Key": "incorrect-key"}
        )

        assert response.status_code == 401

        print("PASS: Invalid key rejected")

        print("\nAll ticket API tests passed!")

    finally:
        if previous_key is None:
            os.environ.pop("ADMIN_API_KEY", None)
        else:
            os.environ["ADMIN_API_KEY"] = previous_key


if __name__ == "__main__":
    TestTicketApi()
