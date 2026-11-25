
import re
import hashlib

from services.knowledgeBaseService import LoadKnowledgeBase


MAX_CHARS = 1200
OVERLAP_CHARS = 150


def SplitText(text, max_chars=MAX_CHARS, overlap=OVERLAP_CHARS):
    if max_chars <= 0 or overlap < 0 or overlap >= max_chars:
        raise ValueError("Invalid chunk settings")

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + max_chars, len(text))

        if end < len(text):
            boundary = text.rfind("\n", start, end)

            if boundary > start + max_chars // 2:
                end = boundary

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def ChunkDocuments(documents=None):
    if documents is None:
        documents = LoadKnowledgeBase()

    chunks = []

    for document in documents:
        source = document["source"]
        content = document["content"]

        heading = "General"
        section_lines = []

        def AddSection():
            if not section_lines:
                return

            section_text = "\n".join(section_lines).strip()

            for part in SplitText(section_text):
                chunk_id = hashlib.sha256(
                    f"{source}|{heading}|{part}".encode("utf-8")
                ).hexdigest()[:24]

                chunks.append({
                    "id": chunk_id,
                    "text": f"Section: {heading}\n{part}",
                    "metadata": {
                        "source": source,
                        "section": heading
                    }
                })

        for line in content.splitlines():
            if re.match(r"^#{1,6}\s+", line):
                AddSection()

                heading = re.sub(
                    r"^#{1,6}\s+",
                    "",
                    line
                ).strip()

                section_lines = []
            else:
                section_lines.append(line)

        AddSection()

    return chunks
