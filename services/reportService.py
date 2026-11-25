
import csv
import io

from collections import Counter
from datetime import date, datetime, timezone

from services.ticketService import (
    GetConnection,
    InitializeTicketDatabase,
    InitializeTicketAudit
)


def ParseUTC(value):

    parsed = datetime.fromisoformat(
        value.replace("Z", "+00:00")
    )

    if parsed.tzinfo is None:
        raise ValueError("Timestamp has no timezone")

    return parsed.astimezone(timezone.utc)


def GetReportTickets(start_date=None, end_date=None):

    if start_date and end_date and start_date > end_date:
        raise ValueError("Start date cannot exceed end date")

    InitializeTicketDatabase()

    with GetConnection() as connection:
        rows = connection.execute("""
            SELECT ticket_id, intent, status,
                   created_at, updated_at
            FROM support_tickets
            ORDER BY created_at DESC
        """).fetchall()

    tickets = []

    for row in rows:
        ticket = dict(row)

        created_date = ParseUTC(
            ticket["created_at"]
        ).date()

        if start_date and created_date < start_date:
            continue

        if end_date and created_date > end_date:
            continue

        tickets.append(ticket)

    return tickets


def GetAnalyticsReport(start_date=None, end_date=None):

    tickets = GetReportTickets(start_date, end_date)

    statuses = Counter(
        ticket["status"] for ticket in tickets
    )

    intents = Counter(
        ticket["intent"] for ticket in tickets
    )

    total = len(tickets)
    resolved = statuses["resolved"]

    InitializeTicketAudit()

    ticket_ids = {
        ticket["ticket_id"] for ticket in tickets
    }

    with GetConnection() as connection:
        events = connection.execute("""
            SELECT ticket_id, changed_at
            FROM ticket_audit_logs
            WHERE new_status = 'resolved'
            ORDER BY audit_id DESC
        """).fetchall()

    latest_resolutions = {}

    for event in events:
        ticket_id = event["ticket_id"]

        if (
            ticket_id in ticket_ids
            and ticket_id not in latest_resolutions
        ):
            latest_resolutions[ticket_id] = event[
                "changed_at"
            ]

    durations = []

    for ticket in tickets:
        if ticket["status"] != "resolved":
            continue

        resolved_at = latest_resolutions.get(
            ticket["ticket_id"]
        )

        if not resolved_at:
            continue

        hours = (
            ParseUTC(resolved_at)
            - ParseUTC(ticket["created_at"])
        ).total_seconds() / 3600

        if hours >= 0:
            durations.append(hours)

    return {
        "start_date": (
            start_date.isoformat() if start_date else None
        ),
        "end_date": (
            end_date.isoformat() if end_date else None
        ),
        "total_tickets": total,
        "pending_tickets": statuses["pending"],
        "in_progress_tickets": statuses["in_progress"],
        "resolved_tickets": resolved,
        "open_tickets": (
            statuses["pending"]
            + statuses["in_progress"]
        ),
        "resolution_rate": (
            round(resolved / total * 100, 2)
            if total else 0.0
        ),
        "average_resolution_hours": (
            round(sum(durations) / len(durations), 2)
            if durations else None
        ),
        "resolution_time_sample_size": len(durations),
        "tickets_by_intent": dict(sorted(intents.items()))
    }


def GenerateTicketCSV(start_date=None, end_date=None):

    tickets = GetReportTickets(start_date, end_date)

    output = io.StringIO(newline="")
    writer = csv.writer(output)

    writer.writerow([
        "ticket_id",
        "intent",
        "status",
        "created_at",
        "updated_at"
    ])

    def SafeCell(value):
        text = str(value or "")

        if text.lstrip().startswith(
            ("=", "+", "-", "@", "\t", "\r")
        ):
            return "'" + text

        return text

    for ticket in tickets:
        writer.writerow([
            SafeCell(ticket["ticket_id"]),
            SafeCell(ticket["intent"]),
            SafeCell(ticket["status"]),
            SafeCell(ticket["created_at"]),
            SafeCell(ticket["updated_at"])
        ])

    return output.getvalue()
