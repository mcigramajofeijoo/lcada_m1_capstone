# Trait (as returned by dominant_trait) -> LangChain product.
# Copied from the reference; double-check names against docs.langchain.com,
# since product names change (the reference itself mentions a rename).
PRODUCT_MATCHES = {
    "Chaotic": "Fleet",
    "Organized": "Evaluation",
    "Cautious": "Observability",
    "Bold": "Engine",
    "Solo": "Sandboxes",
    "Collaborative": "Deployment",
}

# This is used in the card rendered (`title` ALWAYS, `verdict` only if the agent in charge of generating it fails for some reason)
RESULTS = {
    "Solo": {
        "title": "The Lone Builder",
        "verdict": "You ship best alone: headphones on, decisions fast. You thrive in deep work states where you can hold the entire architecture in your head without interruption. Constant pings and endless meetings only disrupt your flow state and raw productivity.",
    },
    "Bold": {
        "title": "The Shipper",
        "verdict": "You ship first and fix forward. Momentum is your superpower. You believe that getting code into the hands of users is infinitely more valuable than achieving theoretical perfection, trusting your ability to patch things on the fly rather than getting bogged down in endless pre-launch testing.",
    },
    "Chaotic": {
        "title": "The Improviser",
        "verdict": "You thrive in the unknown and see sudden shifts as exciting challenges rather than setbacks. Strict roadmaps bore you, and you prefer to tackle problems head-on as they spontaneously arise. Your adaptable nature means you find highly creative workarounds when the original plan falls apart.",
    },
    "Organized": {
        "title": "The Architect",
        "verdict": "You believe that an ounce of prevention is worth a pound of cure. You build robust systems, write comprehensive documentation, and rely on well-structured plans to guide your engineering efforts. Chaos is the enemy of progress for you, and you prefer to measure twice so you only ever have to cut once.",
    },
    "Cautious": {
        "title": "The Guardian",
        "verdict": "You prioritize stability, reliability, and thorough validation above all else. You would rather delay a release than push code that might introduce subtle bugs or regressions. Your meticulous attention to detail ensures that when your work finally ships, the resulting product is virtually bulletproof.",
    },
    "Collaborative": {
        "title": "The Co-Pilot",
        "verdict": "You do your absolute best work when you are bouncing ideas off others and solving complex problems as a cohesive unit. Whether through pair programming, dynamic whiteboarding sessions, or rigorous code reviews, you value shared ownership and recognize that a unified team builds vastly superior software.",
    },
}
