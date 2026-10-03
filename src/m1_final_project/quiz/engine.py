import questionary

from m1_final_project.quiz.questions import AXES, QUESTIONS


async def run_quiz():
    """Ask every question with arrow-key selection.
    Returns a list with the deltas dict of each picked choice."""
    picked_deltas = []

    for q in QUESTIONS:
        choices = q["choices"]

        labels = [c["label"] for c in choices]

        picked = await questionary.select(q["question"], choices=labels).ask_async()

        picked_deltas.append(next(c["deltas"] for c in choices if c["label"] == picked))

    return picked_deltas


def score_answers(picked_deltas):
    """picked_deltas: output of run_quiz().
    Returns {axis_id: score 0-100}, where 100 = fully the right label."""
    scores = {}
    for axis_id, _, _ in AXES:
        # what the user actually accumulated on this axis
        raw = sum(d.get(axis_id, 0) for d in picked_deltas)
        # best and worst sum anyone could reach on this axis
        hi = sum(
            max(c["deltas"].get(axis_id, 0) for c in q["choices"]) for q in QUESTIONS
        )
        lo = sum(
            min(c["deltas"].get(axis_id, 0) for c in q["choices"]) for q in QUESTIONS
        )
        # scale to 0-100 (guard against dividing by zero)
        scores[axis_id] = round((raw - lo) / (hi - lo) * 100) if hi != lo else 50
    return scores


def dominant_trait(scores):
    """Returns the label of the strongest lean, e.g. 'Bold' or 'Solo'."""
    axis_id, left, right = max(AXES, key=lambda a: abs(scores[a[0]] - 50))
    return right if scores[axis_id] >= 50 else left


# How this decides the category:
# - `score_answers`:
#       gives three numbers, one per axis.
# - `dominant_trait`:
#       picks the axis with the strongest lean and returns its label.
#       That label is the key into a results table. This replaces PRODUCT_MATCHES from the reference, which mapped to LangChain products.
#       For recruiters, you'll want your own builder types, for example "Bold": "The Shipper". We'll define that table in step 3, next to the card.
