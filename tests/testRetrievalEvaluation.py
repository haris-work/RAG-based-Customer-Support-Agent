
from services.vectorStoreService import SearchKnowledgeBase


TEST_CASES = [
    {
        "question": "How long does standard shipping take?",
        "expected": [
            "06_shipping_policy.md",
            "15_frequently_asked_questions.md"
        ]
    },
    {
        "question": "Where can I find my package tracking number?",
        "expected": [
            "07_order_tracking.md",
            "15_frequently_asked_questions.md"
        ]
    },
    {
        "question": "Can I return something after buying it?",
        "expected": [
            "08_returns_exchanges.md"
        ]
    },
    {
        "question": "When will my refund reach my bank?",
        "expected": [
            "09_refunds.md"
        ]
    },
    {
        "question": "My device stopped working during the warranty period.",
        "expected": [
            "10_warranty_policy.md"
        ]
    },
    {
        "question": "Why was my payment declined?",
        "expected": [
            "11_payment_billing.md"
        ]
    },
    {
        "question": "Can I use two promo codes together?",
        "expected": [
            "12_discounts_promotions.md"
        ]
    },
    {
        "question": "How do I reset my account password?",
        "expected": [
            "13_account_management.md"
        ]
    },
    {
        "question": "My Bluetooth speaker won't pair with my phone.",
        "expected": [
            "14_technical_troubleshooting.md"
        ]
    },
    {
        "question": "Can I talk to a real customer service person?",
        "expected": [
            "16_human_escalation_policy.md",
            "15_frequently_asked_questions.md"
        ]
    }
]


def TestRetrievalEvaluation():

    hits = 0
    missed_questions = []

    for index, case in enumerate(TEST_CASES, 1):

        results = SearchKnowledgeBase(
            case["question"],
            top_k=3
        )

        sources = [
            result["source"]
            for result in results
        ]

        matched = any(
            source in sources
            for source in case["expected"]
        )

        if matched:
            hits += 1
        else:
            missed_questions.append(case)

        print("\n" + "=" * 60)
        print(f"TEST {index}: {case['question']}")
        print("Acceptable sources:", case["expected"])
        print("Retrieved sources:", sources)
        print("Result:", "PASS" if matched else "MISS")

        if not matched:

            print("\nMISSED QUESTION:", case["question"])
            print("EXPECTED SOURCES:", case["expected"])
            print("\nTOP 5 RESULTS:")

            detailed_results = SearchKnowledgeBase(
                case["question"],
                top_k=5
            )

            for rank, result in enumerate(
                detailed_results, 1
            ):

                print(f"\nRank {rank}")
                print("Source:", result["source"])
                print("Section:", result["section"])
                print(
                    "Distance:",
                    round(result["distance"], 4)
                )
                print("Text:", result["text"][:300])

    accuracy = hits / len(TEST_CASES) * 100

    print("\n" + "=" * 60)
    print("RETRIEVAL EVALUATION")
    print("=" * 60)

    print("Total questions:", len(TEST_CASES))
    print("Successful matches:", hits)
    print("Missed questions:", len(missed_questions))
    print(f"Hit@3: {accuracy:.1f}%")

    if accuracy >= 80:
        print("Initial retrieval target achieved.")
    else:
        print("Retrieval needs improvement.")

    if missed_questions:

        print("\nQUESTIONS REQUIRING REVIEW:")

        for case in missed_questions:
            print("-", case["question"])

    return accuracy


def TestOutOfScopeRetrieval():

    question = "Who won the football World Cup in 1998?"

    results = SearchKnowledgeBase(
        question,
        top_k=3
    )

    print("\n" + "=" * 60)
    print("OUT-OF-SCOPE RETRIEVAL TEST")
    print("=" * 60)

    print("Question:", question)

    for rank, result in enumerate(results, 1):

        print(f"\nRank {rank}")
        print("Source:", result["source"])
        print("Section:", result["section"])
        print(
            "Distance:",
            round(result["distance"], 4)
        )

    print(
        "\nNote: ChromaDB can retrieve similar chunks "
        "even for questions unrelated to the company."
    )


if __name__ == "__main__":

    TestRetrievalEvaluation()

    TestOutOfScopeRetrieval()
