
from agents.customerSupportAgent import RunCustomerSupportAgent

from services.ticketService import (
    GetSupportTicket,
    GetPendingTickets
)


def TestSupportTickets():

    result = RunCustomerSupportAgent(
        question="I want to speak to a human representative.",
        thread_id="ticket_test_customer_001"
    )

    print("\n" + "=" * 60)
    print("CUSTOMER SUPPORT REQUEST")
    print("=" * 60)

    print("Intent:", result["intent"])
    print("Route:", result["route"])
    print("Status:", result["status"])
    print("Answer:", result["answer"])

    assert result["intent"] == "human_support"
    assert result["route"] == "human"
    assert result["status"] == "needs_review"

    ticket_id = result["ticket_id"]

    assert ticket_id is not None

    ticket = GetSupportTicket(ticket_id)

    assert ticket is not None
    assert ticket["ticket_id"] == ticket_id
    assert ticket["status"] == "pending"
    assert ticket["thread_id"] == "ticket_test_customer_001"

    print("\n" + "=" * 60)
    print("SAVED SUPPORT TICKET")
    print("=" * 60)

    for key, value in ticket.items():
        print(f"{key}: {value}")

    pending_tickets = GetPendingTickets()

    assert any(
        item["ticket_id"] == ticket_id
        for item in pending_tickets
    )

    print("\nPending tickets:", len(pending_tickets))
    print("\nSupport ticket test passed!")


if __name__ == "__main__":
    TestSupportTickets()
