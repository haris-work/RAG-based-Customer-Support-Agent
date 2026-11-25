
import uuid

from concurrent.futures import ThreadPoolExecutor

from services.ticketService import (
    FindOrCreateSupportTicket,
    GetAllTickets,
    UpdateTicketStatus
)


def TestTicketDeduplication():

    thread_id = str(uuid.uuid4())

    message = "I need a human representative."

    print("\nTEST 1: Create first ticket")

    first = FindOrCreateSupportTicket(
        thread_id,
        message,
        "human_support"
    )

    assert first["created"] is True

    first_id = first["ticket"]["ticket_id"]

    print("PASS: Created", first_id)

    print("\nTEST 2: Repeat same request")

    second = FindOrCreateSupportTicket(
        thread_id,
        "  i NEED a human representative! ",
        "human_support"
    )

    assert second["created"] is False
    assert second["ticket"]["ticket_id"] == first_id

    print("PASS: Existing ticket reused")

    print("\nTEST 3: Different request")

    different = FindOrCreateSupportTicket(
        thread_id,
        "Please investigate my damaged charger.",
        "human_support"
    )

    assert different["created"] is True
    assert different["ticket"]["ticket_id"] != first_id

    print("PASS: Different issue created separately")

    print("\nTEST 4: Different conversation")

    another = FindOrCreateSupportTicket(
        str(uuid.uuid4()),
        message,
        "human_support"
    )

    assert another["created"] is True
    assert another["ticket"]["ticket_id"] != first_id

    print("PASS: Conversations remain separate")

    print("\nTEST 5: In-progress ticket")

    UpdateTicketStatus(
        first_id,
        "in_progress"
    )

    repeated = FindOrCreateSupportTicket(
        thread_id,
        message,
        "human_support"
    )

    assert repeated["created"] is False
    assert repeated["ticket"]["ticket_id"] == first_id

    print("PASS: In-progress ticket reused")

    print("\nTEST 6: Resolved ticket")

    UpdateTicketStatus(
        first_id,
        "resolved"
    )

    reopened_request = FindOrCreateSupportTicket(
        thread_id,
        message,
        "human_support"
    )

    assert reopened_request["created"] is True
    assert reopened_request["ticket"]["ticket_id"] != first_id

    print("PASS: New ticket created after resolution")

    print("\nTEST 7: Concurrent requests")

    concurrent_thread = str(uuid.uuid4())

    def CreateConcurrentTicket(_):

        return FindOrCreateSupportTicket(
            concurrent_thread,
            "Please connect me with a representative.",
            "human_support"
        )

    with ThreadPoolExecutor(max_workers=5) as executor:

        results = list(
            executor.map(
                CreateConcurrentTicket,
                range(5)
            )
        )

    ids = {
        item["ticket"]["ticket_id"]
        for item in results
    }

    created_count = sum(
        item["created"]
        for item in results
    )

    assert len(ids) == 1
    assert created_count == 1

    print("PASS: Concurrent requests share one ticket")

    print("\nTEST 8: Verify database records")

    matching = [
        ticket
        for ticket in GetAllTickets()
        if ticket["thread_id"] == concurrent_thread
    ]

    assert len(matching) == 1

    print("PASS: Only one ticket stored")

    print("\n" + "=" * 60)
    print("ALL TICKET DEDUPLICATION TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    TestTicketDeduplication()
