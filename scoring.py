import config


def calculate(changes):

    total = 0

    scored_changes = []

    for change in changes:

        metadata = config.FIELD_METADATA.get(
            change.field,
            {
                "label": change.field,
                "weight": 1
            }
        )

        scored_changes.append({
            "change": change,
            "label": metadata["label"],
            "weight": metadata["weight"]
        })

        total += metadata["weight"]

    return total, scored_changes


def level(score):

    if score >= 8:
        return "★★★★★ VERY HIGH"

    if score >= 5:
        return "★★★★ HIGH"

    if score >= 3:
        return "★★★ MEDIUM"

    return "★ LOW"
