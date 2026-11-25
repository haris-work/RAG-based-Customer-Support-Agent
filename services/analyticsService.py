
from collections import Counter
from datetime import datetime

from services.ticketService import (
    GetConnection,
    InitializeTicketDatabase,
    InitializeTicketAudit
)


def GetSupportAnalytics():

    InitializeTicketDatabase()
    InitializeTicketAudit()

    with GetConnection() as connection:

        tickets = connection.execute("""
            SELECT ticket_id, intent, status, created_at
            FROM support_tickets
        """).fetchall()

        resolution_events = connection.execute("""
            SELECT ticket_id, changed_at
            FROM ticket_audit_logs
            WHERE new_status = 'resolved'
            ORDER BY audit_id DESC
        """).fetchall()

    total = len(tickets)

    statuses = Counter(
        ticket["status"]
        for ticket in tickets
    )

    intents = Counter(
        ticket["intent"]
        for ticket in tickets
    )

    pending = statuses["pending"]
    in_progress = statuses["in_progress"]
    resolved = statuses["resolved"]

    resolution_rate = (
        round(resolved / total * 100, 2)
        if total > 0
        else 0.0
    )

    # Keep the latest resolution event per ticket.
    latest_resolutions = {}

    for event in resolution_events:
        if event["ticket_id"] not in latest_resolutions:
            latest_resolutions[event["ticket_id"]] = (
                event["changed_at"]
            )

    durations = []

    for ticket in tickets:

        if ticket["status"] != "resolved":
            continue

        resolved_at = latest_resolutions.get(
            ticket["ticket_id"]
        )

        if not resolved_at:
            continue

        try:
            created_time = datetime.fromisoformat(
                ticket["created_at"]
            )

            resolved_time = datetime.fromisoformat(
                resolved_at
            )

            duration_hours = (
                resolved_time - created_time
            ).total_seconds() / 3600

            if duration_hours >= 0:
                durations.append(duration_hours)

        except (ValueError, TypeError):
            continue

    average_resolution_hours = (
        round(sum(durations) / len(durations), 2)
        if durations
        else None
    )

    return {
        "total_tickets": total,
        "pending_tickets": pending,
        "in_progress_tickets": in_progress,
        "resolved_tickets": resolved,
        "open_tickets": pending + in_progress,
        "resolution_rate": resolution_rate,
        "average_resolution_hours": average_resolution_hours,
        "resolution_time_sample_size": len(durations),
        "tickets_by_intent": dict(sorted(intents.items()))
    }
