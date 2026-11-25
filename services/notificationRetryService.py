
import os

from dotenv import load_dotenv

from services.ticketService import (
    GetFailedNotifications,
    GetLatestNotificationAttempt
)

from services.webhookNotificationService import (
    NotifySupportWebhook
)


load_dotenv()

MAX_ATTEMPTS = 3


def IsRetryableFailure(attempt):

    if attempt["delivery_status"] == "unconfirmed":
        return False

    if attempt["delivery_status"] == "not_configured":
        return bool(os.getenv("N8N_SUPPORT_WEBHOOK_URL"))

    if attempt["delivery_status"] != "failed":
        return False

    # An HTTP response means the server was reached.
    # Do not automatically replay such requests.
    if attempt["http_status"] is not None:
        return False

    error = (attempt["error_message"] or "").lower()

    # Only retry a clear connection-refused error.
    # Timeouts and ambiguous network failures
    # require manual investigation.
    return any(
        marker in error
        for marker in [
            "connection refused",
            "actively refused",
            "winerror 10061"
        ]
    )


def RetryFailedNotifications(max_tickets=10):

    failed = GetFailedNotifications()

    results = []

    for item in failed[:max_tickets]:

        ticket_id = item["ticket_id"]
        attempt_count = item["attempt_count"]

        if attempt_count >= MAX_ATTEMPTS:

            results.append({
                "ticket_id": ticket_id,
                "status": "retry_limit_reached"
            })

            continue

        if not IsRetryableFailure(item):

            results.append({
                "ticket_id": ticket_id,
                "status": "requires_manual_review"
            })

            continue

        notification = NotifySupportWebhook(ticket_id)

        latest = GetLatestNotificationAttempt(ticket_id)

        results.append({
            "ticket_id": ticket_id,
            "status": notification["delivery_status"],
            "attempt_count": attempt_count + 1,
            "http_status": latest["http_status"]
        })

    return results
