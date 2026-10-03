from langchain.messages import HumanMessage

from m1_final_project.agents.fact_agent.build import FactAgentContext
from m1_final_project.agents.registry import agent_registry
from m1_final_project.quiz.prompts import JUDGE_SYSTEM, JUDGE_TASK
from m1_final_project.quiz.questions import AXES


async def generate_verdict(
    persona, dom_trait, langchain_product, norm_scores, verdict_fallback
):
    """Agent looks up the product in the LangChain docs, then writes a verdict.
    persona: entry from PERSONAS; dom_trait: from engine; langchain_product: from PRODUCT_MATCHES;
    norm_scores: {axis_id: 0-100}; verdict_fallback: text used for the verdict if anything fails.
    """

    summary = ", ".join(
        [
            f"{i} category: {l} vs {r} – {norm_scores[i]}/100 toward {r}"
            for i, l, r in AXES
        ]
    )
    user_prompt = JUDGE_TASK.format(
        trait=dom_trait, product=langchain_product, scores=summary
    )

    try:
        response = await agent_registry.fact_agent.ainvoke(
            {"messages": [HumanMessage(content=user_prompt)]},
            context=FactAgentContext(voice=persona["voice"]),
            version="v2",
        )
        return response.value["messages"][-1].content
    except Exception as exc:
        print(
            f"Something went wrong generating verdict.\n\nError: {type(exc).__name__}.\n\nRaw exception: {exc}"
        )
        return verdict_fallback
