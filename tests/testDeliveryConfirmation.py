
from unittest.mock import patch, Mock

from services.ticketService import (
    CreateSupportTicket,
    GetLatestNotificationAttempt
)

from services.webhookNotificationService import (
    NotifySupportWebhook
)


def TestDeliveryConfirmation():

    ticket = CreateSupportTicket(
        thread_id="delivery_confirmation_test",
        customer_message=(
            "I need a human support representative."
        ),
        intent="human_support"
    )

    ticket_id = ticket["ticket_id"]

    webhook_url = (
        "http://localhost:5678/webhook/"
        "novatech-support-ticket"
    )

    print("\nTEST 1: Confirmed Gmail send")

    confirmed_response = Mock()
    confirmed_response.status_code = 200
    confirmed_response.json.return_value = {
        "ticket_id": ticket_id,
        "delivery_status": "sent"
    }
    confirmed_response.raise_for_status.return_value = None

    with patch.dict(
        "os.environ",
        {"N8N_SUPPORT_WEBHOOK_URL": webhook_url,
         "N8N_WEBHOOK_SECRET": "test-secret"}
    ), patch(
        "services.webhookNotificationService.requests.post",
        return_value=confirmed_response
    ):
        result = NotifySupportWebhook(ticket_id)

    assert result["delivery_status"] == "sent"

    print("PASS: Gmail send confirmation recorded")

    print("\nTEST 2: Unconfirmed webhook response")

    unconfirmed_response = Mock()
    unconfirmed_response.status_code = 200
    unconfirmed_response.json.return_value = {
        "message": "Workflow started"
    }
    unconfirmed_response.raise_for_status.return_value = None

    with patch.dict(
        "os.environ",
        {"N8N_SUPPORT_WEBHOOK_URL": webhook_url,
         "N8N_WEBHOOK_SECRET": "test-secret"}
    ), patch(
        "services.webhookNotificationService.requests.post",
        return_value=unconfirmed_response
    ):
        result = NotifySupportWebhook(ticket_id)

    assert result["delivery_status"] == "unconfirmed"

    print("PASS: Unconfirmed response detected")

    print("\nTEST 3: Notification history")

    latest = GetLatestNotificationAttempt(ticket_id)

    assert latest["delivery_status"] == "unconfirmed"

    print("Latest status:", latest["delivery_status"])

    print("\nDelivery confirmation tests passed!")


if __name__ == "__main__":
    TestDeliveryConfirmation()
