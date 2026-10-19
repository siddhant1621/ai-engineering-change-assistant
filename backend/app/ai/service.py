def analyze_engineering_change(
    change,
    affected_part,
    impacted_assemblies,
):
    """
    Temporary mock AI service.

    Later this function will call a real LLM.
    """

    risks = []

    if affected_part.lifecycle_state != "Released":
        risks.append(
            f"Affected part {affected_part.part_number} "
            f"is currently in {affected_part.lifecycle_state} state."
        )

    if impacted_assemblies:
        risks.append(
            f"The change impacts {len(impacted_assemblies)} "
            "assembly level(s)."
        )

    risks.append(
        "Existing drawings and manufacturing documentation "
        "may require review."
    )

    return {
        "risk_level": "Medium",
        "summary": (
            f"The proposed change affects {affected_part.part_number} "
            f"({affected_part.name}) and may propagate through "
            f"{len(impacted_assemblies)} related assemblies."
        ),
        "potential_risks": risks,
        "missing_information": [
            "Updated validation report",
            "Updated engineering drawing",
            "Compatibility verification",
        ],
        "suggested_reviewers": [
            "Mechanical Engineering",
            "Quality Engineering",
            "Manufacturing Engineering",
        ],
    }