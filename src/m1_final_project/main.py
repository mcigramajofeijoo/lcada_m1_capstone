from dotenv import load_dotenv

load_dotenv()

import asyncio

import questionary
from langchain.messages import HumanMessage

from m1_final_project.mcps.mcp_manager import mcp_manager
from m1_final_project.agents.registry import agent_registry
from m1_final_project.storage.attachment_store import attachment_store
from m1_final_project.agents.poster_agent.runner import run_poster_agent
from m1_final_project.quiz.ascii_card import build_card, print_card, save_card
from m1_final_project.quiz.engine import dominant_trait, run_quiz, score_answers
from m1_final_project.quiz.image.card_to_png import card_to_png
from m1_final_project.quiz.image.dummy_gen import generate_card_image_dummy
from m1_final_project.quiz.image.openai_gen import generate_card_image_openai
from m1_final_project.quiz.judge import generate_verdict
from m1_final_project.quiz.personas import PERSONAS
from m1_final_project.quiz.prompts import POSTER_TASK
from m1_final_project.quiz.results import PRODUCT_MATCHES, RESULTS
from m1_final_project.utils import get_img_path_hyperlink

async def main():

    # 0. Setup
    dummy_user_id = "007"
    await mcp_manager.connect(dummy_user_id)
    agent_registry.build()

    # 1. User picks the judge
    persona_name = await questionary.select(
        "Pick your judge:", choices=list(PERSONAS)
    ).ask_async()
    persona = PERSONAS[persona_name]

    # 2. Deterministic part: scores -> trait -> product
    quiz = await run_quiz()
    scores = score_answers(quiz)
    trait = dominant_trait(scores)
    product = PRODUCT_MATCHES[trait]
    result = RESULTS[trait]

    # 3. Agent part: docs lookup + verdict
    verdict = await generate_verdict(persona, trait, product, scores, result["verdict"])
    card = build_card(
        result["title"],
        trait,
        product,
        scores,
        verdict,
        persona_name,
        persona["mascot"],
    )

    print_card(card, color=persona["color"])

    card_path = pil_png_path = ai_img_path = None

    try:
        card_path = save_card(card, persona_name, result["title"])

        # NOTE: We can make these functions return the bytes if necessary
        pil_png_path = card_to_png(
            card, card_path.with_name(card_path.stem + "_pil.png")
        )

        # TODO: Create a explicit type/dataclass for the return value of image creation functions:
        # - Expected fields: out_path, filename, mimetype, bytes
        img_info = (
            generate_card_image_dummy()
        )  # WARNING: Using dummy since we don't have API credits!

        # ai_img_path = generate_card_image_openai(
        #     pil_png_path,
        #     card_path.with_name(card_path.stem + "_ai.png")
        # )

        # Store img information in Redis (TTL 1 Hour)
        attachment_id = await attachment_store.set(
            file_bytes=img_info["bytes"],
            filename=img_info["filename"],
            mimetype=img_info["mimetype"],
        )

        config = {"configurable": {"thread_id": dummy_user_id}}

        user_prompt = POSTER_TASK.format(
            scores=scores, trait=trait, product=product, verdict=verdict
        )

        response = await run_poster_agent(
            input={
                "messages": [HumanMessage(content=user_prompt)],
                "attachment_id": attachment_id,
            },
            config=config,
        )

        print(f"Agent: {response.value['messages'][-1].content}")

    finally:
        print("\nGenerated files:")
        for label, path in [
            ("ASCII Card", card_path),
            ("PIL Image", pil_png_path),
            ("AI Image", ai_img_path),
        ]:
            print(get_img_path_hyperlink(label=label, path=path))


if __name__ == "__main__":
    asyncio.run(main())
