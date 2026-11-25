
import os
import secrets
import tempfile

from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app

from services.ticketService import (
    CreateSupportTicket,
    UpdateTicketStatus
)


def TestAnalyticsReporting():

    old_key = os.environ.get("ADMIN_API_KEY")
    os.environ["ADMIN_API_KEY"] = secrets.token_urlsafe(32)

    try:
        with tempfile.TemporaryDirectory() as folder:

            database = Path(folder) / "reportTest.db"

            with patch(
                "services.ticketService.DB_PATH",
                database
            ):

                client = TestClient(app)

                headers = {
                    "X-Admin-Key": os.environ["ADMIN_API_KEY"]
                }

                today = datetime.now(
                    timezone.utc
                ).date()

                today_text = today.isoformat()

                ticket1 = CreateSupportTicket(
                    "report_customer_001",
                    "I need human assistance.",
                    "human_support"
                )

                CreateSupportTicket(
                    "report_customer_002",
                    "Where is my order?",
                    "order_account"
                )

                UpdateTicketStatus(
                    ticket1["ticket_id"],
                    "in_progress"
                )

                UpdateTicketStatus(
                    ticket1["ticket_id"],
                    "resolved"
                )

                print("\nTEST 1: Filter today's tickets")

                response = client.get(
                    "/api/analytics/report",
                    params={
                        "start_date": today_text,
                        "end_date": today_text
                    },
                    headers=headers
                )

                assert response.status_code == 200

                report = response.json()

                assert report["total_tickets"] == 2
                assert report["resolved_tickets"] == 1
                assert report["resolution_rate"] == 50.0

                print("PASS: Date filtering works")

                print("\nTEST 2: Date range with no tickets")

                future = (
                    today + timedelta(days=30)
                ).isoformat()

                response = client.get(
                    "/api/analytics/report",
                    params={
                        "start_date": future,
                        "end_date": future
                    },
                    headers=headers
                )

                assert response.status_code == 200
                assert response.json()["total_tickets"] == 0

                print("PASS: Empty range handled")

                print("\nTEST 3: Reject reversed dates")

                response = client.get(
                    "/api/analytics/report",
                    params={
                        "start_date": future,
                        "end_date": today_text
                    },
                    headers=headers
                )

                assert response.status_code == 422

                print("PASS: Invalid range rejected")

                print("\nTEST 4: CSV export")

                response = client.get(
                    "/api/analytics/export",
                    params={
                        "start_date": today_text,
                        "end_date": today_text
                    },
                    headers=headers
                )

                assert response.status_code == 200

                csv_text = response.text

                assert ticket1["ticket_id"] in csv_text
                assert "ticket_id,intent,status" in csv_text
                assert "I need human assistance" not in csv_text

                print("PASS: CSV generated without message text")

                print("\nTEST 5: Unauthorized access")

                response = client.get(
                    "/api/analytics/export"
                )

                assert response.status_code == 401

                response = client.get(
                    "/api/analytics/report"
                )

                assert response.status_code == 401

                print("PASS: Authentication enforced")

                print("\nALL ANALYTICS REPORTING TESTS PASSED")

    finally:
        if old_key is None:
            os.environ.pop("ADMIN_API_KEY", None)
        else:
            os.environ["ADMIN_API_KEY"] = old_key


if __name__ == "__main__":
    TestAnalyticsReporting()
