
from services.notificationRetryService import (
    RetryFailedNotifications
)


def main():

    results = RetryFailedNotifications()

    if not results:
        print("No failed notifications found.")
        return

    for result in results:
        print(
            result["ticket_id"],
            "->",
            result["status"]
        )


if __name__ == "__main__":
    main()
