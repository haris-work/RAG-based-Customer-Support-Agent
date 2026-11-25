
import os
import secrets
import tempfile

from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app

from services.ticketService import (
    CreateSupportTicket,
    UpdateTicketStatus
)

from services.analyticsService import GetSupportAnalytics


def TestSupportAnalytics():

    previous_key = os.environ.get("ADMIN_API_KEY")
    os.environ["ADMIN_API_KEY"] = secrets.token_urlsafe(32)

    try:
        with tempfile.TemporaryDirectory() as directory:

            test_db = Path(directory) / "analyticsTest.db"

            with patch(
                "services.ticketService.DB_PATH",
                test_db
            ):

                print("\nTEST 1: Empty database")

                empty = GetSupportAnalytics()

                assert empty["total_tickets"] == 0
                assert empty["resolution_rate"] == 0
                assert empty["average_resolution_hours"] is None

                print("PASS: Empty database handled")

                print("\nTEST 2: Create sample tickets")

                first = CreateSupportTicket(
                    "analytics_customer_001",
                    "I need assistance with my order.",
                    "order_account"
                )

                second = CreateSupportTicket(
                    "analytics_customer_002",
                    "I need a human representative.",
                    "human_support"
                )

                third = CreateSupportTicket(
                    "analytics_customer_003",
                    "Where is my package?",
                    "order_account"
                )

                UpdateTicketStatus(
                    second["ticket_id"],
                    "in_progress"
                )

                UpdateTicketStatus(
                    third["ticket_id"],
                    "in_progress"
                )

                UpdateTicketStatus(
                    third["ticket_id"],
                    "resolved"
                )

                analytics = GetSupportAnalytics()

                assert analytics["total_tickets"] == 3
                assert analytics["pending_tickets"] == 1
                assert analytics["in_progress_tickets"] == 1
                assert analytics["resolved_tickets"] == 1
                assert analytics["open_tickets"] == 2

                print("PASS: Ticket counts correct")

                print("\nTEST 3: Resolution rate")

                assert analytics["resolution_rate"] == 33.33

                print("PASS: Resolution rate is 33.33%")

                print("\nTEST 4: Escalation categories")

                assert analytics["tickets_by_intent"] == {
                    "human_support": 1,
                    "order_account": 2
                }

                print("PASS: Intent distribution correct")

                print("\nTEST 5: Resolution time")

                assert analytics["resolution_time_sample_size"] == 1
                assert analytics["average_resolution_hours"] is not None
                assert analytics["average_resolution_hours"] >= 0

                print("PASS: Resolution duration calculated")

                print("\nTEST 6: Authenticated analytics API")

                client = TestClient(app)

                response = client.get(
                    "/api/analytics/overview",
                    headers={
                        "X-Admin-Key": os.environ["ADMIN_API_KEY"]
                    }
                )

                assert response.status_code == 200
                assert response.json()["total_tickets"] == 3

                print("PASS: Analytics endpoint works")

                print("\nTEST 7: Unauthorized request")

                response = client.get(
                    "/api/analytics/overview"
                )

                assert response.status_code == 401

                print("PASS: Unauthorized access blocked")

                print("\n" + "=" * 60)
                print("ALL SUPPORT ANALYTICS TESTS PASSED")
                print("=" * 60)

    finally:
        if previous_key is None:
            os.environ.pop("ADMIN_API_KEY", None)
        else:
            os.environ["ADMIN_API_KEY"] = previous_key


if __name__ == "__main__":
    TestSupportAnalytics()
