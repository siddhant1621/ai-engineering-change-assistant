import json
import urllib.error
import urllib.request

from app.rag.retriever import retrieve_documents


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"


def calculate_baseline_risk(impacted_assemblies):
    if not impacted_assemblies:
        return "Low"

    max_level = max(
        item["level"]
        for item in impacted_assemblies
    )

    if max_level >= 2:
        return "High"

    return "Medium"


def analyze_engineering_change(
    change,
    affected_part,
    impacted_assemblies,
):
    baseline_risk = calculate_baseline_risk(
        impacted_assemblies
    )

    impact_depth = (
        max(
            item["level"]
            for item in impacted_assemblies
        )
        if impacted_assemblies
        else 0
    )

    impact_text = "\n".join(
        [
            (
                f"- Level {item['level']}: "
                f"{item['part_number']} — {item['name']} "
                f"(quantity: {item['quantity']})"
            )
            for item in impacted_assemblies
        ]
    )

    if not impact_text:
        impact_text = "No impacted assemblies were found."

    rag_query = f"""
Engineering change involving:

Part: {affected_part.part_number}
Name: {affected_part.name}

Change:
{change.title}

Reason:
{change.reason}
"""
    retrieved_docs = retrieve_documents(
    query=rag_query,
    part_name=affected_part.name,
    n_results=3,
)

    knowledge_text = "\n\n".join(
        [
            (
                f"SOURCE: {item['source']}\n"
                f"{item['content']}"
            )
            for item in retrieved_docs
        ]
    )

    prompt = f"""
You are an engineering change analysis assistant
for a Product Lifecycle Management system.

Your role is advisory only.

IMPORTANT RULES:

1. Do not approve or reject the engineering change.
2. Do not claim that database records were modified.
3. Use only the supplied PLM data and engineering knowledge.
4. Do not invent test results.
5. Do not invent BOM relationships.
6. Do not invent engineering standards.
7. The impacted assemblies were calculated deterministically.
8. Do not claim impacted assemblies are unknown.
9. The baseline risk level was calculated by the backend.
10. You MUST use exactly the supplied baseline risk level.
11. Use the retrieved engineering documents when relevant.
12. If information is not available, list it under missing_information.

ENGINEERING CHANGE

Change Number: {change.change_number}
Title: {change.title}
Description: {change.description}
Reason: {change.reason}
Status: {change.status}
Owner: {change.owner}

AFFECTED PART

Part Number: {affected_part.part_number}
Name: {affected_part.name}
Revision: {affected_part.revision}
Lifecycle State: {affected_part.lifecycle_state}

DETERMINISTIC IMPACT ANALYSIS

Impact Depth: {impact_depth}

Impacted Assemblies:
{impact_text}

SYSTEM-CALCULATED BASELINE RISK

{baseline_risk}

RETRIEVED ENGINEERING KNOWLEDGE

{knowledge_text}

Return valid JSON using exactly this structure:

{{
  "risk_level": "{baseline_risk}",
  "summary": "short engineering assessment",
  "potential_risks": [
    "risk 1",
    "risk 2"
  ],
  "missing_information": [
    "missing item 1",
    "missing item 2"
  ],
  "suggested_reviewers": [
    "reviewer role 1",
    "reviewer role 2"
  ]
}}
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.2
        },
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=120,
        ) as response:
            ollama_response = json.loads(
                response.read().decode("utf-8")
            )

    except urllib.error.URLError as error:
        raise RuntimeError(
            "Could not connect to Ollama."
        ) from error

    model_output = ollama_response["response"]

    try:
        analysis = json.loads(model_output)

    except json.JSONDecodeError as error:
        raise RuntimeError(
            "The local AI model returned invalid JSON."
        ) from error

    # Never allow the LLM to override deterministic risk.
    analysis["risk_level"] = baseline_risk

    # Unique source filenames.
    analysis["sources"] = list(
        dict.fromkeys(
            item["source"]
            for item in retrieved_docs
        )
    )

    # Actual retrieved RAG evidence.
    analysis["evidence"] = [
        {
            "source": item["source"],
            "content": item["content"],
        }
        for item in retrieved_docs
    ]

    return analysis