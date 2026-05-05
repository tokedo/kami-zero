"""Pick the top-N survivors. Trivial in v0 (sort by margin desc); the
optimizer can swap for a weighted-EV scorer later.
"""


def rank(survivors: list[dict]) -> list[dict]:
    return sorted(
        survivors,
        key=lambda c: c.get("margin", 0) or 0,
        reverse=True,
    )
