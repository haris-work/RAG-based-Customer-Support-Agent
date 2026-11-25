
from agents.customerSupportAgent import (
    RunCustomerSupportAgent
)


def TestConversationMemory():

    thread_id = "customer_001"

    questions = [
        "What is your return policy?",
        "What if I already opened the box?",
        "Can I speak to a human representative?"
    ]

    for index, question in enumerate(questions, 1):

        result = RunCustomerSupportAgent(
            question,
            thread_id=thread_id
        )

        print("\n" + "=" * 65)
        print(f"TURN {index}")
        print("QUESTION:", question)
        print("ROUTE:", result["route"])
        print("STATUS:", result["status"])
        print("ANSWER:", result["answer"])
        print("HISTORY LENGTH:", len(result["messages"]))

        assert len(result["messages"]) == index * 2

    print("\n" + "=" * 65)
    print("TESTING SEPARATE CUSTOMER SESSION")

    separate_result = RunCustomerSupportAgent(
        "What is your shipping policy?",
        thread_id="customer_002"
    )

    assert len(separate_result["messages"]) == 2

    print("Customer 002 history length:",
          len(separate_result["messages"]))

    print("\nConversation memory test passed!")


if __name__ == "__main__":
    TestConversationMemory()
