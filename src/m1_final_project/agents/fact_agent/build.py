from dataclasses import dataclass

from deepagents import create_deep_agent

from m1_final_project.agents.fact_agent.middleware import set_fact_agent_system_prompt
from m1_final_project.mcps.mcp_manager import mcp_manager


@dataclass
class FactAgentContext:
    voice: str


def build_fact_agent():
    ALLOWED_TOOLS = {"docs_langchain_search_docs_by_lang_chain"}
    tools = [t for t in mcp_manager.tools if t.name in ALLOWED_TOOLS]

    agent = create_deep_agent(
        "openrouter:inclusionai/ling-3.0-flash-vl:free",
        tools=tools,
        name="M1_FP_Fact_Agent",
        context_schema=FactAgentContext,
        middleware=[set_fact_agent_system_prompt],
    )

    return agent
