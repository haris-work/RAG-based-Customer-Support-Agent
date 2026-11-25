
from services.knowledgeBaseService import LoadKnowledgeBase
from services.documentChunkingService import ChunkDocuments


def TestDocumentChunking():

    documents = LoadKnowledgeBase()
    chunks = ChunkDocuments(documents)

    assert len(documents) == 18
    assert len(chunks) > 18

    ids = [chunk["id"] for chunk in chunks]
    assert len(ids) == len(set(ids))

    for chunk in chunks:
        assert chunk["text"].strip()
        assert chunk["metadata"]["source"]
        assert chunk["metadata"]["section"]

    print("Documents loaded:", len(documents))
    print("Chunks generated:", len(chunks))

    print("\nFirst 3 chunks:")

    for chunk in chunks[:3]:
        print("\nID:", chunk["id"])
        print("Source:", chunk["metadata"]["source"])
        print("Section:", chunk["metadata"]["section"])
        print("Text preview:", chunk["text"][:200])

    print("\nDocument chunking test passed!")


if __name__ == "__main__":
    TestDocumentChunking()
