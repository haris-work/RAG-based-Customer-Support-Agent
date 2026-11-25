
import logging

from pathlib import Path

from services.recoveryLockService import (
    AcquireRecoveryLease,
    ReleaseRecoveryLease
)

from services.notificationRetryService import (
    RetryFailedNotifications
)


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "data" / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=str(LOG_DIR / "notificationRecovery.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def RunScheduledRecovery():

    owner = AcquireRecoveryLease()

    if owner is None:
        logging.info(
            "Recovery skipped: another worker holds the lease"
        )

        return {
            "status": "skipped",
            "results": []
        }

    try:
        results = RetryFailedNotifications(
            max_tickets=10
        )

        for result in results:

            logging.info(
                "Ticket %s: %s",
                result["ticket_id"],
                result["status"]
            )

        logging.info(
            "Recovery completed: %s tickets examined",
            len(results)
        )

        return {
            "status": "completed",
            "results": results
        }

    except Exception:
        logging.exception(
            "Notification recovery failed"
        )
        raise

    finally:
        ReleaseRecoveryLease(owner)


if __name__ == "__main__":

    result = RunScheduledRecovery()

    print("Recovery status:", result["status"])

    for item in result["results"]:
        print(
            item["ticket_id"],
            "->",
            item["status"]
        )
