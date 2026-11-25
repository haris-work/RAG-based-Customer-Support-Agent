from services.knowledgeBaseService import LoadKnowledgeBase


def TestKnowledgeBase():

    documents = LoadKnowledgeBase()

    assert len(documents) == 18

    for document in documents:
        assert document["source"]
        assert document["content"]

        print(
            document["source"],
            "-",
            len(document["content"]),
            "characters"
        )

    print("Knowledge base test passed!")


if __name__ == "__main__":
    TestKnowledgeBase()
