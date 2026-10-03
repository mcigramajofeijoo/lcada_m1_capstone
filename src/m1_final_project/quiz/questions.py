# Cada eje: (id, etiqueta izquierda, etiqueta derecha).
# Un score alto significa que el usuario se inclina hacia la etiqueta DERECHA.
AXES = [
    ("order", "Chaotic", "Organized"),
    ("risk", "Cautious", "Bold"),
    ("team", "Solo", "Collaborative"),
]


# Cada pregunta tiene un texto y una lista de opciones.
# Cada opción tiene: label (lo que ve el usuario) y
# deltas (cuánto mueve cada eje; un eje que no aparece vale 0).
QUESTIONS = [
    {
        "question": "It's 9am, you have 3 unread pings and one big task due today.",
        "choices": [
            {
                "label": "Reply to all three immediately, big task can wait",
                "deltas": {"order": -2, "team": 2},
            },
            {
                "label": "Silence notifications, focus on the big task first",
                "deltas": {"order": 2, "team": -2},
            },
            {
                "label": "Skim them, answer only the urgent one, then dive in",
                "deltas": {"risk": 1},
            },
        ],
    },
    {
        "question": "You find a bug in code you didn't write. It's not blocking you.",
        "choices": [
            {
                "label": "Fix it immediately, mid-task",
                "deltas": {"order": -1, "risk": 2},
            },
            {
                "label": "File a ticket, get back to what you were doing",
                "deltas": {"order": 1, "risk": -1, "team": 1},
            },
            {
                "label": "Leave a comment, let the original author decide",
                "deltas": {"risk": -2, "team": 1},
            },
        ],
    },
    {
        "question": "Your project's plan just changed with zero warning.",
        "choices": [
            {
                "label": "Thrilling. Let's improvise.",
                "deltas": {"order": -2, "risk": 1},
            },
            {
                "label": "Panic quietly, then rebuild the plan from scratch.",
                "deltas": {"order": 2, "risk": -1},
            },
            {
                "label": "Ask the team what changed and why before reacting.",
                "deltas": {"team": 2},
            },
        ],
    },
    {
        "question": "How do you feel about shipping code you haven't fully tested?",
        "choices": [
            {
                "label": "Ship it, fix forward.",
                "deltas": {"order": -1, "risk": 2},
            },
            {
                "label": "Absolutely not, I need to be sure.",
                "deltas": {"order": 1, "risk": -2},
            },
            {
                "label": "Depends who's watching the deploy.",
                "deltas": {"team": 1},
            },
        ],
    },
    {
        "question": "Pick your ideal work session:",
        "choices": [
            {
                "label": "Solo, headphones on, no meetings.",
                "deltas": {"team": -2},
            },
            {
                "label": "Pair programming, thinking out loud with someone.",
                "deltas": {"team": 2},
            },
            {
                "label": "Whiteboarding with the whole team.",
                "deltas": {"order": -1, "risk": 1, "team": 2},
            },
        ],
    },
    {
        "question": "Someone asks you to review their PR right now.",
        "choices": [
            {
                "label": "Sure, dropping what I'm doing to look now.",
                "deltas": {"risk": -1, "team": 2},
            },
            {
                "label": "I'll finish my current task first, then review.",
                "deltas": {"order": 1},
            },
            {
                "label": "Skim it fast, leave a couple comments, move on.",
                "deltas": {"order": -1, "team": 1},
            },
        ],
    },
    {
        "question": "Your build just failed in CI. What's your first move?",
        "choices": [
            {
                "label": "Re-run it, probably flaky.",
                "deltas": {"order": -1, "risk": 1},
            },
            {
                "label": "Read the full log before touching anything.",
                "deltas": {"order": 1, "risk": -1},
            },
            {
                "label": "Ping whoever touched that file last.",
                "deltas": {"team": 2},
            },
        ],
    },
    {
        "question": "How do you feel about writing documentation?",
        "choices": [
            {
                "label": "Write it as I go, future me will thank me.",
                "deltas": {"order": 1, "risk": -1},
            },
            {
                "label": "I'll write it eventually. Probably.",
                "deltas": {"order": -2, "risk": 1, "team": -1},
            },
            {
                "label": "Only if someone else is going to read it soon.",
                "deltas": {"team": 1},
            },
        ],
    },
]
