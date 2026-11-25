
import sqlite3
import uuid

from pathlib import Path
from datetime import datetime, timezone

import hashlib
import re


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "supportTickets.db"


def GetConnection():

    DB_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        str(DB_PATH),
        timeout=10
    )

    connection.row_factory = sqlite3.Row

    return connection


def InitializeTicketDatabase():

    with GetConnection() as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS support_tickets (
                ticket_id TEXT PRIMARY KEY,
                thread_id TEXT NOT NULL,
                customer_message TEXT NOT NULL,
                intent TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_ticket_thread
            ON support_tickets(thread_id)
        """)


def CreateSupportTicket(
    thread_id,
    customer_message,
    intent
):

    if not isinstance(thread_id, str) or not thread_id.strip():
        raise ValueError("Invalid thread ID")

    if not isinstance(customer_message, str) or not customer_message.strip():
        raise ValueError("Customer message cannot be empty")

    if not isinstance(intent, str) or not intent.strip():
        raise ValueError("Intent cannot be empty")

    InitializeTicketDatabase()

    ticket_id = "NT-" + uuid.uuid4().hex[:12].upper()

    timestamp = datetime.now(
        timezone.utc
    ).isoformat()

    with GetConnection() as connection:

        connection.execute("""
            INSERT INTO support_tickets (
                ticket_id,
                thread_id,
                customer_message,
                intent,
                status,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            ticket_id,
            thread_id,
            customer_message,
            intent,
            "pending",
            timestamp,
            timestamp
        ))

    return {
        "ticket_id": ticket_id,
        "thread_id": thread_id,
        "intent": intent,
        "status": "pending",
        "created_at": timestamp
    }


def GetSupportTicket(ticket_id):

    InitializeTicketDatabase()

    with GetConnection() as connection:

        row = connection.execute("""
            SELECT *
            FROM support_tickets
            WHERE ticket_id = ?
        """, (ticket_id,)).fetchone()

    return dict(row) if row else None


def GetPendingTickets():

    InitializeTicketDatabase()

    with GetConnection() as connection:

        rows = connection.execute("""
            SELECT *
            FROM support_tickets
            WHERE status = 'pending'
            ORDER BY created_at ASC
        """).fetchall()

    return [dict(row) for row in rows]



def InitializeNotificationDatabase():

    with GetConnection() as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS ticket_notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT NOT NULL,
                delivery_status TEXT NOT NULL,
                http_status INTEGER,
                error_message TEXT,
                attempted_at TEXT NOT NULL,
                FOREIGN KEY (ticket_id)
                REFERENCES support_tickets(ticket_id)
            )
        """)


def RecordNotificationAttempt(
    ticket_id,
    delivery_status,
    http_status=None,
    error_message=None
):

    InitializeNotificationDatabase()

    timestamp = datetime.now(
        timezone.utc
    ).isoformat()

    with GetConnection() as connection:

        connection.execute("""
            INSERT INTO ticket_notifications (
                ticket_id,
                delivery_status,
                http_status,
                error_message,
                attempted_at
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            ticket_id,
            delivery_status,
            http_status,
            error_message,
            timestamp
        ))


def GetNotificationAttempts(ticket_id):

    InitializeNotificationDatabase()

    with GetConnection() as connection:

        rows = connection.execute("""
            SELECT *
            FROM ticket_notifications
            WHERE ticket_id = ?
            ORDER BY id DESC
        """, (ticket_id,)).fetchall()

    return [dict(row) for row in rows]




VALID_TRANSITIONS = {
    "pending": {"in_progress"},
    "in_progress": {"resolved"},
    "resolved": {"in_progress"}
}



def UpdateTicketStatus(
    ticket_id,
    new_status,
    actor="system"
):

    if new_status not in {
        "pending",
        "in_progress",
        "resolved"
    }:
        raise ValueError("Invalid ticket status")

    if not isinstance(actor, str) or not actor.strip():
        raise ValueError("Invalid audit actor")

    InitializeTicketDatabase()
    InitializeTicketAudit()

    with GetConnection() as connection:

        connection.execute("BEGIN IMMEDIATE")

        row = connection.execute("""
            SELECT status
            FROM support_tickets
            WHERE ticket_id = ?
        """, (ticket_id,)).fetchone()

        if row is None:
            raise ValueError("Support ticket not found")

        previous_status = row["status"]

        if previous_status == new_status:
            return GetSupportTicket(ticket_id)

        allowed = VALID_TRANSITIONS.get(
            previous_status,
            set()
        )

        if new_status not in allowed:
            raise ValueError(
                f"Invalid transition: "
                f"{previous_status} -> {new_status}"
            )

        timestamp = datetime.now(
            timezone.utc
        ).isoformat()

        connection.execute("""
            UPDATE support_tickets
            SET status = ?, updated_at = ?
            WHERE ticket_id = ?
        """, (
            new_status,
            timestamp,
            ticket_id
        ))

        connection.execute("""
            INSERT INTO ticket_audit_logs (
                ticket_id,
                previous_status,
                new_status,
                actor,
                changed_at
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            ticket_id,
            previous_status,
            new_status,
            actor.strip(),
            timestamp
        ))

    return GetSupportTicket(ticket_id)


def GetAllTickets(status=None):

    InitializeTicketDatabase()

    allowed_statuses = {
        "pending",
        "in_progress",
        "resolved"
    }

    if status is not None and status not in allowed_statuses:
        raise ValueError("Invalid ticket status")

    with GetConnection() as connection:

        if status is None:

            rows = connection.execute("""
                SELECT *
                FROM support_tickets
                ORDER BY created_at DESC
            """).fetchall()

        else:

            rows = connection.execute("""
                SELECT *
                FROM support_tickets
                WHERE status = ?
                ORDER BY created_at DESC
            """, (status,)).fetchall()

    return [dict(row) for row in rows]



def GetLatestNotificationAttempt(ticket_id):

    InitializeNotificationDatabase()

    with GetConnection() as connection:

        row = connection.execute("""
            SELECT *
            FROM ticket_notifications
            WHERE ticket_id = ?
            ORDER BY id DESC
            LIMIT 1
        """, (ticket_id,)).fetchone()

    return dict(row) if row else None


def GetFailedNotifications():

    InitializeNotificationDatabase()

    with GetConnection() as connection:

        rows = connection.execute("""
            SELECT
                n.ticket_id,
                n.delivery_status,
                n.http_status,
                n.error_message,
                n.attempted_at,
                (
                    SELECT COUNT(*)
                    FROM ticket_notifications AS history
                    WHERE history.ticket_id = n.ticket_id
                ) AS attempt_count
            FROM ticket_notifications AS n
            INNER JOIN (
                SELECT ticket_id, MAX(id) AS latest_id
                FROM ticket_notifications
                GROUP BY ticket_id
            ) AS latest
                ON latest.latest_id = n.id
            WHERE n.delivery_status IN (
                'failed',
                'not_configured',
                'unconfirmed'
            )
            ORDER BY n.attempted_at ASC
        """).fetchall()

    return [dict(row) for row in rows]





def NormalizeTicketRequest(message):

    if not isinstance(message, str) or not message.strip():
        raise ValueError("Customer message cannot be empty")

    normalized = re.sub(
        r"\s+",
        " ",
        message.strip().casefold()
    )

    normalized = normalized.rstrip(" .!?")

    return hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()


def InitializeTicketDeduplication():

    InitializeTicketDatabase()

    with GetConnection() as connection:

        columns = {
            row["name"]
            for row in connection.execute(
                "PRAGMA table_info(support_tickets)"
            ).fetchall()
        }

        if "issue_key" not in columns:

            connection.execute("""
                ALTER TABLE support_tickets
                ADD COLUMN issue_key TEXT
            """)

        connection.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS
                idx_unique_active_ticket
            ON support_tickets(
                thread_id,
                intent,
                issue_key
            )
            WHERE issue_key IS NOT NULL
            AND status IN (
                'pending',
                'in_progress'
            )
        """)


def FindOrCreateSupportTicket(
    thread_id,
    customer_message,
    intent
):

    if not isinstance(thread_id, str) or not thread_id.strip():
        raise ValueError("Invalid thread ID")

    if not isinstance(intent, str) or not intent.strip():
        raise ValueError("Invalid intent")

    issue_key = NormalizeTicketRequest(
        customer_message
    )

    InitializeTicketDeduplication()

    timestamp = datetime.now(
        timezone.utc
    ).isoformat()

    ticket_id = "NT-" + uuid.uuid4().hex[:12].upper()

    with GetConnection() as connection:

        connection.execute("BEGIN IMMEDIATE")

        existing = connection.execute("""
            SELECT *
            FROM support_tickets
            WHERE thread_id = ?
              AND intent = ?
              AND issue_key = ?
              AND status IN ('pending', 'in_progress')
            LIMIT 1
        """, (
            thread_id,
            intent,
            issue_key
        )).fetchone()

        if existing is not None:

            return {
                "ticket": dict(existing),
                "created": False
            }

        connection.execute("""
            INSERT INTO support_tickets (
                ticket_id,
                thread_id,
                customer_message,
                intent,
                status,
                created_at,
                updated_at,
                issue_key
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ticket_id,
            thread_id,
            customer_message,
            intent,
            "pending",
            timestamp,
            timestamp,
            issue_key
        ))

    saved = GetSupportTicket(ticket_id)

    return {
        "ticket": saved,
        "created": True
    }




def InitializeTicketAudit():

    with GetConnection() as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS ticket_audit_logs (
                audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT NOT NULL,
                previous_status TEXT NOT NULL,
                new_status TEXT NOT NULL,
                actor TEXT NOT NULL,
                changed_at TEXT NOT NULL,
                FOREIGN KEY (ticket_id)
                REFERENCES support_tickets(ticket_id)
            )
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_audit_ticket
            ON ticket_audit_logs(ticket_id)
        """)


def GetTicketAuditHistory(ticket_id):

    InitializeTicketAudit()

    with GetConnection() as connection:

        rows = connection.execute("""
            SELECT *
            FROM ticket_audit_logs
            WHERE ticket_id = ?
            ORDER BY audit_id ASC
        """, (ticket_id,)).fetchall()

    return [dict(row) for row in rows]


