
import sqlite3

from pathlib import Path
from langgraph.checkpoint.sqlite import SqliteSaver


BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "conversationMemory.db"

DB_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)


def CreateConversationCheckpointer():

    connection = sqlite3.connect(
        str(DB_PATH),
        check_same_thread=False
    )

    checkpointer = SqliteSaver(connection)

    checkpointer.setup()

    return checkpointer


def GetConversationConfig(thread_id):

    if not isinstance(thread_id, str) or not thread_id.strip():
        raise ValueError("Invalid conversation ID")

    return {
        "configurable": {
            "thread_id": thread_id
        }
    }
