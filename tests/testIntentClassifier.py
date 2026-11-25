
from agents.customerSupportAgent import RunCustomerSupportAgent


TEST_CASES = [
    {
        "question": "How many days do I have to return an item?",
        "expected": "policy_inquiry"
    },
    {
        "question": "Does this charger work with an iPhone?",
        "expected": "product_inquiry"
    },
    {
        "question": "My Bluetooth speaker keeps disconnecting.",
        "expected": "technical_support"
    },
    {
        "question": "Where is my order right now?",
        "expected": "order_account"
    },
    {
        "question": "I want to speak with a human representative.",
        "expected": "human_support"
    },
    {
        "question": "Who won the football World Cup in 1998?",
        "expected": "out_of_scope"
    },
    {
        "question": "Where can I find my tracking number?",
        "expected": "policy_inquiry"
    },
    {
        "question": "Where is my refund?",
        "expected": "order_account"
    }
]


def TestIntentClassifier():

    correct = 0

    for index, case in enumerate(TEST_CASES, 1):

        result = RunCustomerSupportAgent(
            question=case["question"],
            thread_id=f"intent_test_{index}"
        )

        actual = result["intent"]
        expected = case["expected"]

        matched = actual == expected

        if matched:
            correct += 1

        print("\n" + "=" * 60)
        print("QUESTION:", case["question"])
        print("EXPECTED:", expected)
        print("ACTUAL:", actual)
        print("ROUTE:", result["route"])
        print("RESULT:", "PASS" if matched else "MISS")

    accuracy = correct / len(TEST_CASES) * 100

    print("\n" + "=" * 60)
    print("INTENT CLASSIFICATION EVALUATION")
    print("=" * 60)
    print("Total questions:", len(TEST_CASES))
    print("Correct:", correct)
    print(f"Accuracy: {accuracy:.1f}%")

    if accuracy >= 90:
        print("Initial classification target achieved.")
    else:
        print("Classification needs improvement.")


if __name__ == "__main__":
    TestIntentClassifier()
