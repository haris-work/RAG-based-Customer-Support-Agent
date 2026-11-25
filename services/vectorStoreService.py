
from pathlib import Path

import chromadb

from services.documentChunkingService import ChunkDocuments


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "chromaDB"

COLLECTION_NAME = "novatech_knowledge"


def GetCollection():

    client = chromadb.PersistentClient(
        path=str(DB_PATH)
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    return collection


def BuildVectorStore():

    chunks = ChunkDocuments()

    if not chunks:
        raise ValueError("No document chunks found")

    collection = GetCollection()

    # Rebuild the local demo index so deleted or
    # changed documents do not leave stale chunks.
    existing = collection.get(include=[])

    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    batch_size = 100

    for start in range(0, len(chunks), batch_size):

        batch = chunks[start:start + batch_size]

        collection.upsert(
            ids=[item["id"] for item in batch],
            documents=[item["text"] for item in batch],
            metadatas=[item["metadata"] for item in batch]
        )

    print("Documents indexed:", len(chunks))
    print("Stored vectors:", collection.count())

    return collection


def SearchKnowledgeBase(question, top_k=5):

    if not question or not question.strip():
        raise ValueError("Question cannot be empty")

    if top_k < 1:
        raise ValueError("top_k must be positive")

    collection = GetCollection()

    if collection.count() == 0:
        raise ValueError(
            "Knowledge base is not indexed"
        )

    results = collection.query(
        query_texts=[question],
        n_results=min(top_k, collection.count()),
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    matches = []

    for index, document in enumerate(
        results["documents"][0]
    ):

        matches.append({
            "text": document,
            "source": results["metadatas"][0][index]["source"],
            "section": results["metadatas"][0][index]["section"],
            "distance": results["distances"][0][index]
        })

    return matches
