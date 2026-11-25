
from agents.customerSupportAgent import RunCustomerSupportAgent

from services.ticketService import (
    GetSupportTicket,
    GetNotificationAttempts
)


def TestWebhookNotification():

    result = RunCustomerSupportAgent(
        question=(
            "I want to speak to a human "
            "representative about my order."
        ),
        thread_id="webhook_integration_test"
    )

    ticket_id = result["ticket_id"]

    print("\n" + "=" * 60)
    print("LANGGRAPH RESULT")
    print("=" * 60)

    print("Intent:", result["intent"])
    print("Route:", result["route"])
    print("Ticket ID:", ticket_id)
    print(
        "Notification status:",
        result["notification_status"]
    )

    assert result["route"] == "human"
    assert ticket_id is not None

    ticket = GetSupportTicket(ticket_id)

    assert ticket is not None
    assert ticket["status"] == "pending"

    attempts = GetNotificationAttempts(ticket_id)

    print("\n" + "=" * 60)
    print("NOTIFICATION HISTORY")
    print("=" * 60)

    for attempt in attempts:
        print("Status:", attempt["delivery_status"])
        print("HTTP:", attempt["http_status"])
        print("Error:", attempt["error_message"])

    assert len(attempts) >= 1

    assert result["notification_status"] == "sent", (
        "n8n did not acknowledge the webhook"
    )

    print("\nWebhook integration test passed!")


if __name__ == "__main__":
    TestWebhookNotification()
