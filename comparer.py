def compare(previous: dict, current: dict):

    changes = []

    keys = set(previous.keys()) | set(current.keys())

    for key in sorted(keys):

        if previous.get(key) != current.get(key):

            changes.append({
                "field": key,
                "previous": previous.get(key),
                "current": current.get(key)
            })

    return changes
