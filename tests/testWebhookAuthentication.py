
import os
from unittest.mock import patch, Mock

from services.ticketService import CreateSupportTicket

from services.webhookNotificationService import (
    NotifySupportWebhook
)


def TestWebhookAuthentication():

    ticket = CreateSupportTicket(
        thread_id="webhook_auth_test",
        customer_message="I need human assistance.",
        intent="human_support"
    )

    ticket_id = ticket["ticket_id"]

    test_secret = "test-secret-not-for-production"

    webhook_url = (
        "http://localhost:5678/webhook/"
        "novatech-support-ticket"
    )

    print("\nTEST 1: Authenticated request")

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "ticket_id": ticket_id,
        "delivery_status": "sent"
    }
    mock_response.raise_for_status.return_value = None

    with patch.dict(
        os.environ,
        {
            "N8N_SUPPORT_WEBHOOK_URL": webhook_url,
            "N8N_WEBHOOK_SECRET": test_secret
        }
    ), patch(
        "services.webhookNotificationService.requests.post",
        return_value=mock_response
    ) as mock_post:

        result = NotifySupportWebhook(ticket_id)

        assert result["delivery_status"] == "sent"

        mock_post.assert_called_once()

        headers = mock_post.call_args.kwargs["headers"]

        assert (
            headers["X-NovaTech-Webhook-Key"]
            == test_secret
        )

        print("PASS: Authentication header included")

    print("\nTEST 2: Missing webhook secret")

    with patch.dict(
        os.environ,
        {
            "N8N_SUPPORT_WEBHOOK_URL": webhook_url
        }
    ), patch.dict(
        os.environ,
        {"N8N_WEBHOOK_SECRET": ""},
        clear=False
    ), patch(
        "services.webhookNotificationService.requests.post"
    ) as mock_post:

        result = NotifySupportWebhook(ticket_id)

        assert result["delivery_status"] == "not_configured"

        mock_post.assert_not_called()

        print("PASS: Unauthenticated request blocked")

    print("\nWebhook authentication tests passed!")


if __name__ == "__main__":
    TestWebhookAuthentication()
