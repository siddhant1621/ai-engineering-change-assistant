from pathlib import Path

import chromadb
import requests


PROJECT_ROOT = Path(__file__).resolve().parents[3]
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


def detect_document_type(
    part_name: str,
) -> str:
    name = part_name.lower()

    if "wiring harness" in name:
        return "wiring_harness"

    if "bracket" in name:
        return "bracket"

    return "generic"


def retrieve_documents(
    query: str,
    part_name: str | None = None,
    n_results: int = 3,
):
    query_embedding = get_embedding(query)

    document_type = (
        detect_document_type(part_name)
        if part_name
        else "generic"
    )

    # First retrieve part-specific knowledge.
    specific_results = []

    if document_type != "generic":
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where={
                "document_type": document_type
            },
        )

        for document, metadata, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            specific_results.append(
                {
                    "content": document,
                    "source": metadata["source"],
                    "distance": distance,
                }
            )

    # Also retrieve generic engineering guidance.
    generic_results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where={
            "document_type": "generic"
        },
    )

    generic_documents = []

    for document, metadata, distance in zip(
        generic_results["documents"][0],
        generic_results["metadatas"][0],
        generic_results["distances"][0],
    ):
        generic_documents.append(
            {
                "content": document,
                "source": metadata["source"],
                "distance": distance,
            }
        )

    combined = (
        specific_results
        + generic_documents
    )

    # Avoid duplicate chunks/sources.
    unique = []
    seen = set()

    for item in combined:
        key = (
            item["source"],
            item["content"],
        )

        if key in seen:
            continue

        seen.add(key)
        unique.append(item)

    # Sort best semantic match first.
    unique.sort(
        key=lambda item: item["distance"]
    )

    return unique[:n_results]


if __name__ == "__main__":
    test_query = (
        "What should be reviewed when changing "
        "wiring harness routing because of vibration "
        "and insufficient clearance?"
    )

    results = retrieve_documents(
        query=test_query,
        part_name="Wiring Harness",
        n_results=3,
    )

    print("\nRetrieved Documents:\n")

    for index, item in enumerate(
        results,
        start=1,
    ):
        print(f"Result {index}")
        print(f"Source: {item['source']}")
        print(f"Distance: {item['distance']}")
        print(item["content"])
        print("-" * 60)