import config


def calculate(changes):

    score = 0

    scored = []

    for field in changes:

        metadata = config.FIELD_METADATA.get(field)

        if metadata is None:
            continue

        score += metadata["weight"]

        scored.append({
            "field": field,
            "label": metadata["label"],
            "weight": metadata["weight"]
        })

    scored.sort(
        key=lambda item: item["weight"],
        reverse=True
    )

    return score, scored
