
from services.ragService import AnswerQuestion


TEST_QUESTIONS = [
    "How long does standard shipping take?",
    "Where can I find my tracking number?",
    "Can I use two discount codes together?",
    "My Bluetooth speaker won't connect. What should I do?",
    "What is the current status of my order?",
    "Who won the football World Cup in 1998?"
]


def TestRagService():

    for question in TEST_QUESTIONS:

        print("\n" + "=" * 70)
        print("QUESTION:", question)

        result = AnswerQuestion(question)

        print("\nSTATUS:", result["status"])
        print("\nANSWER:", result["answer"])

        print("\nSOURCES:")

        for source in result["sources"]:
            print(
                f"[{source['reference']}] "
                f"{source['file']} — "
                f"{source['section']}"
            )

        assert result["answer"]

        if result["status"] == "answered":
            assert len(result["sources"]) > 0

    print("\nRAG answer generation test completed!")


if __name__ == "__main__":
    TestRagService()
