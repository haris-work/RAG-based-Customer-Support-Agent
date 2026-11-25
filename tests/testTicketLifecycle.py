
from services.ticketService import (
    CreateSupportTicket,
    GetSupportTicket,
    UpdateTicketStatus,
    GetAllTickets
)


def TestTicketLifecycle():

    ticket = CreateSupportTicket(
        thread_id="lifecycle_test_001",
        customer_message=(
            "My order was delivered damaged."
        ),
        intent="order_account"
    )

    ticket_id = ticket["ticket_id"]

    print("\n" + "=" * 60)
    print("TICKET CREATED")
    print("=" * 60)

    print("Ticket ID:", ticket_id)
    print("Status:", ticket["status"])

    assert ticket["status"] == "pending"

    print("\n" + "=" * 60)
    print("MOVING TO IN_PROGRESS")
    print("=" * 60)

    updated = UpdateTicketStatus(
        ticket_id,
        "in_progress"
    )

    assert updated["status"] == "in_progress"

    print("Updated status:", updated["status"])

    print("\n" + "=" * 60)
    print("RESOLVING TICKET")
    print("=" * 60)

    updated = UpdateTicketStatus(
        ticket_id,
        "resolved"
    )

    assert updated["status"] == "resolved"

    print("Updated status:", updated["status"])

    print("\n" + "=" * 60)
    print("TESTING INVALID TRANSITION")
    print("=" * 60)

    try:
        UpdateTicketStatus(ticket_id, "pending")
        raise AssertionError(
            "Invalid transition was accepted"
        )

    except ValueError as error:
        print("Correctly rejected:", error)

    print("\n" + "=" * 60)
    print("REOPENING TICKET")
    print("=" * 60)

    updated = UpdateTicketStatus(
        ticket_id,
        "in_progress"
    )

    assert updated["status"] == "in_progress"

    print("Reopened status:", updated["status"])

    print("\n" + "=" * 60)
    print("FILTERING TICKETS")
    print("=" * 60)

    active_tickets = GetAllTickets(
        status="in_progress"
    )

    assert any(
        item["ticket_id"] == ticket_id
        for item in active_tickets
    )

    print(
        "In-progress tickets:",
        len(active_tickets)
    )

    saved = GetSupportTicket(ticket_id)

    assert saved["status"] == "in_progress"

    print("\nTicket lifecycle test passed!")


if __name__ == "__main__":
    TestTicketLifecycle()
