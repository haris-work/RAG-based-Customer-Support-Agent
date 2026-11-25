
from unittest.mock import patch

from services.recoveryLockService import (
    AcquireRecoveryLease,
    ReleaseRecoveryLease
)

from scripts.scheduledRecovery import (
    RunScheduledRecovery
)


def TestScheduledRecovery():

    print("\nTEST 1: Acquire recovery lease")

    owner = AcquireRecoveryLease()

    assert owner is not None

    try:
        second_owner = AcquireRecoveryLease()

        assert second_owner is None

        print("PASS: Overlapping worker blocked")

    finally:
        ReleaseRecoveryLease(owner)

    print("\nTEST 2: Run scheduled recovery")

    simulated_results = [{
        "ticket_id": "NT-SIMULATED001",
        "status": "sent",
        "attempt_count": 2
    }]

    with patch(
        "scripts.scheduledRecovery.RetryFailedNotifications",
        return_value=simulated_results
    ) as retry_mock:

        result = RunScheduledRecovery()

        retry_mock.assert_called_once_with(
            max_tickets=10
        )

    assert result["status"] == "completed"
    assert len(result["results"]) == 1

    print("PASS: Recovery worker executed")

    print("\nTEST 3: Verify lease released")

    new_owner = AcquireRecoveryLease()

    assert new_owner is not None

    ReleaseRecoveryLease(new_owner)

    print("PASS: Lease released successfully")

    print("\nScheduled recovery tests passed!")


if __name__ == "__main__":
    TestScheduledRecovery()
