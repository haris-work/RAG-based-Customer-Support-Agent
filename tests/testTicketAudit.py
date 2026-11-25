
import os
import secrets

from fastapi.testclient import TestClient

from main import app

from services.ticketService import (
    CreateSupportTicket,
    GetSupportTicket,
    GetTicketAuditHistory
)


def TestTicketAudit():

    previous_key = os.environ.get("ADMIN_API_KEY")
    test_key = secrets.token_urlsafe(32)

    os.environ["ADMIN_API_KEY"] = test_key

    client = TestClient(app)

    headers = {
        "X-Admin-Key": test_key
    }

    try:
        ticket = CreateSupportTicket(
            thread_id="audit_test_customer_001",
            customer_message=(
                "My order arrived damaged."
            ),
            intent="order_account"
        )

        ticket_id = ticket["ticket_id"]

        print("\nTEST 1: Initial history")

        history = GetTicketAuditHistory(ticket_id)

        assert len(history) == 0

        print("PASS: No status changes recorded")

        print("\nTEST 2: Start working")

        response = client.patch(
            f"/api/tickets/{ticket_id}/status",
            headers=headers,
            json={"status": "in_progress"}
        )

        assert response.status_code == 200

        history = GetTicketAuditHistory(ticket_id)

        assert len(history) == 1
        assert history[0]["previous_status"] == "pending"
        assert history[0]["new_status"] == "in_progress"
        assert history[0]["actor"] == "admin_api_key"

        print("PASS: First audit event recorded")

        print("\nTEST 3: Resolve ticket")

        response = client.patch(
            f"/api/tickets/{ticket_id}/status",
            headers=headers,
            json={"status": "resolved"}
        )

        assert response.status_code == 200

        history = GetTicketAuditHistory(ticket_id)

        assert len(history) == 2
        assert history[1]["previous_status"] == "in_progress"
        assert history[1]["new_status"] == "resolved"

        print("PASS: Resolution event recorded")

        print("\nTEST 4: Repeated status update")

        response = client.patch(
            f"/api/tickets/{ticket_id}/status",
            headers=headers,
            json={"status": "resolved"}
        )

        assert response.status_code == 200

        assert len(GetTicketAuditHistory(ticket_id)) == 2

        print("PASS: No duplicate audit event")

        print("\nTEST 5: Invalid transition")

        response = client.patch(
            f"/api/tickets/{ticket_id}/status",
            headers=headers,
            json={"status": "pending"}
        )

        assert response.status_code == 400
        assert len(GetTicketAuditHistory(ticket_id)) == 2
        assert GetSupportTicket(ticket_id)["status"] == "resolved"

        print("PASS: Invalid transition rejected")

        print("\nTEST 6: Retrieve audit history through API")

        response = client.get(
            f"/api/tickets/{ticket_id}/history",
            headers=headers
        )

        assert response.status_code == 200
        assert response.json()["total_events"] == 2

        print("PASS: Audit history retrieved")

        print("\nTEST 7: Unauthorized access")

        response = client.get(
            f"/api/tickets/{ticket_id}/history"
        )

        assert response.status_code == 401

        print("PASS: Unauthorized access blocked")

        print("\n" + "=" * 60)
        print("ALL TICKET AUDIT TESTS PASSED")
        print("=" * 60)

    finally:
        if previous_key is None:
            os.environ.pop("ADMIN_API_KEY", None)
        else:
            os.environ["ADMIN_API_KEY"] = previous_key


if __name__ == "__main__":
    TestTicketAudit()
