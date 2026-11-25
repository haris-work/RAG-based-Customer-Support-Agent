
from unittest.mock import patch
import requests

from services.ticketService import (
    CreateSupportTicket,
    GetNotificationAttempts,
    GetLatestNotificationAttempt
)

from services.webhookNotificationService import (
    NotifySupportWebhook
)

from services.notificationRetryService import (
    RetryFailedNotifications
)


def TestNotificationRetry():

    ticket = CreateSupportTicket(
        thread_id="retry_test_customer_001",
        customer_message=(
            "I need a human representative."
        ),
        intent="human_support"
    )

    ticket_id = ticket["ticket_id"]

    print("\nTEST 1: Simulate webhook failure")

    with patch.dict(
        "os.environ",
        {
            "N8N_SUPPORT_WEBHOOK_URL":
            "http://localhost:5678/webhook-test/test",
            "N8N_WEBHOOK_SECRET": "test-secret"
        }
    ), patch(
        "services.webhookNotificationService.requests.post",
        side_effect=requests.ConnectionError(
            "Connection refused"
        )
    ):

        result = NotifySupportWebhook(ticket_id)

    assert result["delivery_status"] == "failed"

    print("PASS: Failed attempt recorded")

    print("\nTEST 2: Retry after recovery")

    import json

    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = json.dumps({
        "ticket_id": ticket_id,
        "delivery_status": "sent"
    }).encode("utf-8")

    with patch.dict(
        "os.environ",
        {
            "N8N_SUPPORT_WEBHOOK_URL":
            "http://localhost:5678/webhook-test/test",
            "N8N_WEBHOOK_SECRET": "test-secret"
        }
    ), patch(
        "services.webhookNotificationService.requests.post",
        return_value=mock_response
    ):

        results = RetryFailedNotifications()

    matching = [
        item for item in results
        if item["ticket_id"] == ticket_id
    ]

    assert len(matching) == 1
    assert matching[0]["status"] == "sent"

    print("PASS: Retry accepted")

    print("\nTEST 3: Verify notification history")

    attempts = GetNotificationAttempts(ticket_id)

    assert len(attempts) == 2

    assert attempts[0]["delivery_status"] == "accepted"
    assert attempts[1]["delivery_status"] == "failed"

    print("Attempt 1:", attempts[1]["delivery_status"])
    print("Attempt 2:", attempts[0]["delivery_status"])

    print("\nTEST 4: Confirm accepted ticket is excluded")

    latest = GetLatestNotificationAttempt(ticket_id)

    assert latest["delivery_status"] == "accepted"

    print("PASS: Latest status is accepted")

    print("\nNotification retry test passed!")


if __name__ == "__main__":
    TestNotificationRetry()
