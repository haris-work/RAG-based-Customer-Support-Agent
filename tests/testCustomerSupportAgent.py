
from agents.customerSupportAgent import RunCustomerSupportAgent


TEST_CASES = [
    "How long does standard shipping take?",
    "Where can I find my tracking number?",
    "Can I use two discount codes together?",
    "What is the current status of my order?",
    "I want to speak to a human agent.",
    "Who won the football World Cup in 1998?"
]


def TestCustomerSupportAgent():

    for question in TEST_CASES:

        result = RunCustomerSupportAgent(question)

        print("\n" + "=" * 65)
        print("QUESTION:", question)
        print("ROUTE:", result["route"])
        print("STATUS:", result["status"])
        print("ANSWER:", result["answer"])
        print("SOURCES:", result["sources"])

        assert result["answer"]
        assert result["status"] in [
            "answered",
            "needs_review"
        ]

        if "current status of my order" in question:
            assert result["route"] == "human"
            assert result["status"] == "needs_review"

        if "speak to a human" in question:
            assert result["route"] == "human"

    print("\nCustomer Support Agent test passed!")


if __name__ == "__main__":
    TestCustomerSupportAgent()
