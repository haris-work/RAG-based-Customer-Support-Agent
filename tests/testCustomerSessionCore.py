
import secrets
import tempfile
import time

from pathlib import Path
from unittest.mock import patch

from services.customerSessionService import (
    CreateCustomerSession,
    GetCustomerSession,
    CreateCustomerConversation,
    OwnsConversation,
    GetSessionConnection,
    HashToken
)


def TestCustomerSessionCore():

    with tempfile.TemporaryDirectory() as folder:

        test_database = Path(folder) / "sessionsTest.db"

        with patch(
            "services.customerSessionService.DB_PATH",
            test_database
        ):

            print("\nTEST 1: Create customer session")

            customer_a = CreateCustomerSession()

            assert customer_a["session_id"]
            assert customer_a["token"]

            print("PASS: Session created")

            print("\nTEST 2: Validate session token")

            session_id = GetCustomerSession(
                customer_a["token"]
            )

            assert session_id == customer_a["session_id"]

            print("PASS: Valid session accepted")

            print("\nTEST 3: Reject invalid token")

            invalid = GetCustomerSession(
                secrets.token_urlsafe(48)
            )

            assert invalid is None

            print("PASS: Invalid token rejected")

            print("\nTEST 4: Protect stored credentials")

            with GetSessionConnection() as connection:

                row = connection.execute("""
                    SELECT token_hash
                    FROM customer_sessions
                    WHERE session_id = ?
                """, (
                    customer_a["session_id"],
                )).fetchone()

            assert row["token_hash"] == HashToken(
                customer_a["token"]
            )

            assert row["token_hash"] != customer_a["token"]

            print("PASS: Raw token not stored")

            print("\nTEST 5: Conversation ownership")

            conversation_id = CreateCustomerConversation(
                customer_a["session_id"]
            )

            assert OwnsConversation(
                customer_a["session_id"],
                conversation_id
            )

            customer_b = CreateCustomerSession()

            assert not OwnsConversation(
                customer_b["session_id"],
                conversation_id
            )

            print("PASS: Cross-session ownership denied")

            print("\nTEST 6: Expired session")

            with GetSessionConnection() as connection:

                connection.execute("""
                    UPDATE customer_sessions
                    SET expires_at = ?
                    WHERE session_id = ?
                """, (
                    int(time.time()) - 10,
                    customer_a["session_id"]
                ))

            assert GetCustomerSession(
                customer_a["token"]
            ) is None

            print("PASS: Expired session rejected")

    print("\nALL CUSTOMER SESSION CORE TESTS PASSED")


if __name__ == "__main__":
    TestCustomerSessionCore()
