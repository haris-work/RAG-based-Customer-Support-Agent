
import subprocess
import sys
import uuid

from unittest.mock import patch

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

from agents.customerSupportAgent import (
    RunCustomerSupportAgent,
    customerSupportAgent
)

from services.conversationMemoryService import (
    GetConversationConfig
)


def ReadHistory(thread_id):

    snapshot = customerSupportAgent.get_state(
        GetConversationConfig(thread_id)
    )

    return snapshot.values.get("messages", [])


def WriteFirstTurn(thread_id):

    with patch(
        "agents.customerSupportAgent.ClassifyIntent",
        return_value="policy_inquiry"
    ), patch(
        "agents.customerSupportAgent.AnswerQuestion",
        return_value={
            "answer": "Our return policy is available.",
            "sources": [],
            "status": "answered"
        }
    ):
        result = RunCustomerSupportAgent(
            "What is your return policy?",
            thread_id=thread_id
        )

    assert len(result["messages"]) == 2

    print("PASS: First turn saved")


def VerifyAndContinue(thread_id):

    messages = ReadHistory(thread_id)

    assert len(messages) == 2
    assert isinstance(messages[0], HumanMessage)
    assert isinstance(messages[1], AIMessage)

    assert messages[0].content == (
        "What is your return policy?"
    )

    print("PASS: Previous conversation restored")

    with patch(
        "agents.customerSupportAgent.ClassifyIntent",
        return_value="policy_inquiry"
    ), patch(
        "agents.customerSupportAgent.AnswerQuestion",
        return_value={
            "answer": "Opened-box eligibility depends on the policy.",
            "sources": [],
            "status": "answered"
        }
    ):
        result = RunCustomerSupportAgent(
            "What if I opened the box?",
            thread_id=thread_id
        )

    assert len(result["messages"]) == 4

    print("PASS: Follow-up appended")

    other_thread = str(uuid.uuid4())

    assert ReadHistory(other_thread) == []

    print("PASS: Different thread has no history")


def RunChild(mode, thread_id):

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "tests.testPersistentMemory",
            mode,
            thread_id
        ],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.returncode != 0:
        print(result.stderr)

    assert result.returncode == 0


def TestPersistentMemory():

    thread_id = str(uuid.uuid4())

    print("\nTEST 1: Save conversation")

    RunChild("write", thread_id)

    print("\nTEST 2: Reload in a new Python process")

    RunChild("read", thread_id)

    print("\nTEST 3: Confirm history persisted")

    messages = ReadHistory(thread_id)

    assert len(messages) == 4

    print("PASS: Four messages persisted")

    print("\nPersistent memory tests passed!")


if __name__ == "__main__":

    if len(sys.argv) == 3:

        mode = sys.argv[1]
        thread_id = sys.argv[2]

        if mode == "write":
            WriteFirstTurn(thread_id)

        elif mode == "read":
            VerifyAndContinue(thread_id)

        else:
            raise ValueError("Invalid test mode")

    else:
        TestPersistentMemory()
