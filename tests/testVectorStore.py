
from services.vectorStoreService import (
    BuildVectorStore,
    SearchKnowledgeBase
)


def TestVectorStore():

    collection = BuildVectorStore()

    assert collection.count() > 18

    questions = [
        "How many days do I have to return a product?",
        "How can I track my order?",
        "What should I do if my Bluetooth speaker won't connect?"
    ]

    for question in questions:

        print("\n" + "=" * 60)
        print("QUESTION:", question)

        results = SearchKnowledgeBase(
            question,
            top_k=3
        )

        assert results

        for index, result in enumerate(results, 1):

            print(f"\nResult {index}")
            print("Source:", result["source"])
            print("Section:", result["section"])
            print("Distance:", round(result["distance"], 4))
            print("Text:", result["text"][:250])

    print("\nVector store test passed!")


if __name__ == "__main__":
    TestVectorStore()
