
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

KNOWLEDGE_BASE_DIR = BASE_DIR / "data" / "knowledgeBase"


def LoadKnowledgeBase():

    if not KNOWLEDGE_BASE_DIR.exists():
        raise FileNotFoundError(
            "Knowledge base directory does not exist"
        )

    documents = []

    for file_path in sorted(KNOWLEDGE_BASE_DIR.glob("*.md")):

        content = file_path.read_text(
            encoding="utf-8"
        ).strip()

        if not content:
            continue

        documents.append({
            "source": file_path.name,
            "content": content
        })

    if not documents:
        raise ValueError("Knowledge base is empty")

    return documents
