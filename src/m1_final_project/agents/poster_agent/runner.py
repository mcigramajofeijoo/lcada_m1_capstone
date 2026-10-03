from langgraph.types import Command

from m1_final_project.agents.poster_agent.context import PosterAgentContext
from m1_final_project.agents.poster_agent.helpers import get_or_create_linkedin_urn
from m1_final_project.agents.registry import agent_registry
from m1_final_project.hitl.handlers import default_handler
from m1_final_project.hitl.registry import REGISTRY
from m1_final_project.storage.linkedin_store import linkedin_store


async def run_poster_agent(input: dict, config: dict):
    """
    Invoca al agent y resuelve interrupts hasta que termina.

    Args:
    - initial_state: dict pasado como state inicial (ej. messages + attachment_id).
    - config: el config object de LangGraph (thread_id, etc.).
    """
    poster_agent = agent_registry.poster_agent

    linkedin_user_urn = await get_or_create_linkedin_urn(
        user_id=config["configurable"]["thread_id"]
    )

    # Context, not state: linkedin_user_urn is static per run (unlike attachment_id,
    # which changes every invoke, so that one belongs in state).
    # Context isn't persisted by the checkpointer, so it must be passed on every
    # invoke. In production this would likely come from a DB; for now, Redis.
    context = PosterAgentContext(linkedin_user_urn=linkedin_user_urn)

    response = await poster_agent.ainvoke(
        input, version="v2", config=config, context=context
    )

    while response.interrupts:
        decisions = []

        pending = response.interrupts[0].value

        for req in pending["action_requests"]:
            handler = REGISTRY.get(req["name"], default_handler)
            decisions.append(await handler(req))

        response = await poster_agent.ainvoke(
            Command(resume={"decisions": decisions}),
            version="v2",
            config=config,
            context=context,
        )

    return response
