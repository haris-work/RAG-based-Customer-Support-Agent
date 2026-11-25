
import time
import uuid

from contextlib import closing

from services.ticketService import GetConnection


LEASE_NAME = "notification_recovery"
LEASE_SECONDS = 900


def AcquireRecoveryLease():

    owner = uuid.uuid4().hex
    now = time.time()

    with closing(GetConnection()) as connection:

        connection.isolation_level = None
        connection.execute("BEGIN IMMEDIATE")

        try:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS recovery_leases (
                    lease_name TEXT PRIMARY KEY,
                    owner TEXT NOT NULL,
                    expires_at REAL NOT NULL
                )
            """)

            row = connection.execute("""
                SELECT owner, expires_at
                FROM recovery_leases
                WHERE lease_name = ?
            """, (LEASE_NAME,)).fetchone()

            if row and row["expires_at"] > now:
                connection.execute("COMMIT")
                return None

            connection.execute("""
                INSERT INTO recovery_leases (
                    lease_name,
                    owner,
                    expires_at
                )
                VALUES (?, ?, ?)
                ON CONFLICT(lease_name)
                DO UPDATE SET
                    owner = excluded.owner,
                    expires_at = excluded.expires_at
            """, (
                LEASE_NAME,
                owner,
                now + LEASE_SECONDS
            ))

            connection.execute("COMMIT")

        except Exception:
            connection.execute("ROLLBACK")
            raise

    return owner


def ReleaseRecoveryLease(owner):

    with closing(GetConnection()) as connection:

        connection.execute("""
            DELETE FROM recovery_leases
            WHERE lease_name = ?
            AND owner = ?
        """, (
            LEASE_NAME,
            owner
        ))

        connection.commit()
