
import hashlib
import secrets
import sqlite3
import time
import uuid

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "customerSessions.db"

SESSION_LIFETIME = 7 * 24 * 60 * 60


def GetSessionConnection():

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


def InitializeSessionDatabase():

    with GetSessionConnection() as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS customer_sessions (
                session_id TEXT PRIMARY KEY,
                token_hash TEXT UNIQUE NOT NULL,
                expires_at INTEGER NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS customer_conversations (
                conversation_id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                created_at INTEGER NOT NULL,
                FOREIGN KEY (session_id)
                REFERENCES customer_sessions(session_id)
            )
        """)


def HashToken(token):

    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()


def CreateCustomerSession():

    InitializeSessionDatabase()

    token = secrets.token_urlsafe(48)
    session_id = str(uuid.uuid4())

    expires_at = int(time.time()) + SESSION_LIFETIME

    with GetSessionConnection() as connection:

        connection.execute("""
            INSERT INTO customer_sessions (
                session_id,
                token_hash,
                expires_at
            )
            VALUES (?, ?, ?)
        """, (
            session_id,
            HashToken(token),
            expires_at
        ))

    return {
        "session_id": session_id,
        "token": token
    }


def GetCustomerSession(token):

    if not token:
        return None

    InitializeSessionDatabase()

    with GetSessionConnection() as connection:

        row = connection.execute("""
            SELECT session_id
            FROM customer_sessions
            WHERE token_hash = ?
            AND expires_at > ?
        """, (
            HashToken(token),
            int(time.time())
        )).fetchone()

    return row["session_id"] if row else None


def CreateCustomerConversation(session_id):

    InitializeSessionDatabase()

    conversation_id = str(uuid.uuid4())

    with GetSessionConnection() as connection:

        connection.execute("""
            INSERT INTO customer_conversations (
                conversation_id,
                session_id,
                created_at
            )
            VALUES (?, ?, ?)
        """, (
            conversation_id,
            session_id,
            int(time.time())
        ))

    return conversation_id


def OwnsConversation(session_id, conversation_id):

    InitializeSessionDatabase()

    with GetSessionConnection() as connection:

        row = connection.execute("""
            SELECT 1
            FROM customer_conversations
            WHERE conversation_id = ?
            AND session_id = ?
        """, (
            str(conversation_id),
            session_id
        )).fetchone()

    return row is not None
