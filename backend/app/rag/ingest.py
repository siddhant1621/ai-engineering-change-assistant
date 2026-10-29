from pathlib import Path

import chromadb
import requests


PROJECT_ROOT = Path(__file__).resolve().parents[3]
KNOWLEDGE_DIR = PROJECT_ROOT / "docs" / "knowledge"
CHROMA_DIR = PROJECT_ROOT / "database" / "chroma"

OLLAMA_EMBED_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"


client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_or_create_collection(
    name="engineering_knowledge"
)


def get_embedding(text: str) -> list[float]:
    response = requests.post(
        OLLAMA_EMBED_URL,
        json={
            "model": EMBED_MODEL,
            "prompt": text,
        },
        timeout=120,
    )

    response.raise_for_status()

    return response.json()["embedding"]


def split_text(
    text: str,
    chunk_size: int = 700,
    overlap: int = 100,
) -> list[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def get_document_type(filename: str) -> str:
    filename = filename.lower()

    if "wiring_harness" in filename:
        return "wiring_harness"

    if "bracket" in filename:
        return "bracket"

    if "vibration" in filename:
        return "generic"

    if "engineering_change" in filename:
        return "generic"

    return "generic"


def ingest_documents():
    if not KNOWLEDGE_DIR.exists():
        raise RuntimeError(
            f"Knowledge folder not found: {KNOWLEDGE_DIR}"
        )

    txt_files = list(
        KNOWLEDGE_DIR.glob("*.txt")
    )

    if not txt_files:
        raise RuntimeError(
            "No .txt files found in docs/knowledge."
        )

    document_ids = []
    documents = []
    embeddings = []
    metadatas = []

    for file_path in txt_files:
        text = file_path.read_text(
            encoding="utf-8"
        )

        chunks = split_text(text)

        document_type = get_document_type(
            file_path.name
        )

        for index, chunk in enumerate(chunks):
            chunk_id = (
                f"{file_path.stem}_{index}"
            )

            embedding = get_embedding(chunk)

            document_ids.append(chunk_id)
            documents.append(chunk)
            embeddings.append(embedding)

            metadatas.append(
                {
                    "source": file_path.name,
                    "chunk": index,
                    "document_type": document_type,
                }
            )

    collection.upsert(
        ids=document_ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(
        f"Ingested {len(document_ids)} document chunks."
    )


if __name__ == "__main__":
    ingest_documents()