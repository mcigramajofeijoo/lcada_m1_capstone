from langchain_core.prompts import PromptTemplate

# System prompt: quién es el judge y las reglas.
# Solo depende de la persona, así que su única variable es {voice}.
JUDGE_SYSTEM = PromptTemplate.from_template(
    "You are {voice}. This is a single-shot task: never ask questions. "
    "Use the docs tool to look up the LangChain product you are given (max 2 searches). "
    "Then write ONE sentence (max 30 words) that names the product exactly as given, "
    "states one concrete fact from the docs, and connects it to the developer's trait. "
    "Output only that sentence. Never use em dashes."
)

# Mensaje del usuario: los datos de esta ejecución.
JUDGE_TASK = PromptTemplate.from_template(
    "Dominant trait: {trait}. Product: {product}. Scores: {scores}."
)

IMAGE_PROMPT = PromptTemplate.from_template(
    "This image is a rasterized text-based developer personality quiz card. "
    "Use the input image as the authoritative source for all content, text, "
    "numbers, percentages, hierarchy, and mascot identity. "
    "Transform it into a premium 2D editorial graphic with a playful, "
    "experimental Awwwards-style and contemporary digital-design aesthetic. "
    "STYLE: "
    "Maximalist but carefully art-directed, playful, expressive, modern, "
    "slightly chaotic, editorial, neo-brutalist, and creative-tech inspired. "
    "Keep the composition square, spacious, and breathable with strong visual rhythm. "
    "TYPOGRAPHY: "
    "Use Saans or a similar modern grotesk. Create strong hierarchy with "
    "oversized expressive headlines, refined spacing, and scale contrast. "
    "Preserve all source text exactly as written. "
    "COLOR: "
    "Use a consistent palette of warm ivory/off-white, near-black, emerald green, "
    "cobalt blue, orange, yellow, and subtle purple accents. "
    "TEXTURE: "
    "Apply a warm crumpled-paper texture across the entire image, with subtle "
    "multiply-style paper grain, fine print imperfections, and restrained "
    "halftone texture. Keep the texture tactile and realistic without reducing legibility. "
    "GRAPHIC LANGUAGE: "
    "Use hand-drawn scribbles, stars, arrows, underlines, geometric shapes, "
    "halftone patterns, grid fragments, abstract blobs, and imperfect marker strokes. "
    "Keep decorative elements intentional and balanced rather than random. "
    "MASCOT: "
    "Transform the source mascot into a charming expressive 2D illustrated character. "
    "Preserve its recognizable silhouette, proportions, pose, and identity. "
    "Use bold shapes, clean outlines, flat colors, subtle shading, and tactile texture. "
    "Do not make it photorealistic, 3D, anime, or generic clip-art. "
    "SCORES: "
    "Preserve all score values exactly and turn meters into polished colored graphical bars. "
    "Maintain clear spacing between labels, bars, and percentages. "
    "BRANDING: "
    "Keep a small LangChain Academy logo in the top-right corner, secondary to the main content. "
    "FIDELITY: "
    "Do not rewrite, add, remove, summarize, or invent content. "
    "Preserve the meaning and information hierarchy of the source. "
    "Improve only the visual presentation. "
    "AVOID: "
    "Photorealism, 3D rendering, glossy UI, generic SaaS dashboards, "
    "corporate infographic styling, excessive gradients, excessive shadows, "
    "neon-heavy palettes, visual clutter, illegible typography, or invented text."
)


POSTER_SYSTEM = PromptTemplate.from_template(
    "You are a social-posting assistant for a developer personality quiz. "
    "The quiz scores a developer's answers, derives a dominant trait, and "
    "matches them to a real LangChain product. You'll receive a short "
    "summary of one quiz result as context, plus tools to post it.\n\n"
    "You can only post to X and LinkedIn, no other platform exists for this. "
    "Whenever you need information from the user for any reason, including "
    "confirming where to post, you MUST use the dev_ask_user tool. Never ask "
    "a question in your own reply text, the user cannot respond to that.\n\n"
    "Before posting anywhere, use dev_ask_user to confirm whether the user "
    "wants to post to X, LinkedIn, both, or neither (do NOT allow a custom answer).\n\n"
    "If posting to LinkedIn, the author/URN field and the image are filled "
    "in for you automatically before the call reaches LinkedIn. Never ask "
    "the user for a URN, an ID, or any image data, call the LinkedIn tool "
    "with whatever placeholder or empty value it requires for those fields, "
    "you don't need the real ones.\n\n"
    "For each platform the user approves, write the post in the voice of "
    "whoever just took the quiz, reacting to their own result, like "
    "'Just took a dev personality quiz and apparently I'm Chaotic...'. "
    "NEVER write it in the voice of the person who built the quiz, never "
    "say things like 'I built this' or 'I just finished Module 1', the "
    "poster is not the builder.\n\n"
    "Make a small, light joke about the dominant trait.\n\n"
    "Keep it brief, the image carries the result, don't restate the scores or verdict text. "
)

POSTER_TASK = PromptTemplate.from_template(
    "Quiz result to announce:\n"
    "- Scores: {scores}\n"
    "- Dominant trait: {trait}\n"
    "- Matched LangChain product: {product}\n"
    '- Judge\'s verdict: "{verdict}"'
)

# Dos detalles que suelen morder
# - **Llaves literales:** si el texto del prompt necesita { o } (por ejemplo, un ejemplo en JSON), duplicalas: {{ }}. Si no, el template las interpreta como variables.
# - **Variables faltantes:** JUDGE_SYSTEM.format() sin voice lanza KeyError. Es una ventaja: el error aparece antes de gastar una llamada al modelo.
