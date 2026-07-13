import config


def calculate(changes):

    score = 0

    scored = []

    for change in changes:

        field = change.field

        metadata = config.FIELD_METADATA.get(field)

        if metadata is None:
            continue

        score += metadata["weight"]

        scored.append(
            {
                "field": field,
                "label": metadata["label"],
                "weight": metadata["weight"],
                "previous": change.previous,
                "current": change.current,
            }
        )

    scored.sort(
        key=lambda x: x["weight"],
        reverse=True,
    )

    return score, scored
