from deepagents import create_deep_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import MemorySaver

from m1_final_project.agents.poster_agent.context import PosterAgentContext
from m1_final_project.agents.poster_agent.middleware import MediaMiddleware
from m1_final_project.agents.poster_agent.state import PosterAgentState
from m1_final_project.mcps.mcp_manager import mcp_manager
from m1_final_project.quiz.prompts import POSTER_SYSTEM


def build_poster_agent():
    # When creating the MCP session we're already restricting the tools the server exposes to only this one, but just in
    # case we'd like to expose all Twitter (X) tools, we can create this `ALLOWED_TOOLS` list.
    ALLOWED_X_TOOLS = [
        "x_TWITTER_CREATION_OF_A_POST"
    ]  # List of composio twitter tools: https://docs.composio.dev/toolkits/twitter
    ALLOWED_LINKEDIN_TOOLS = [
        "lkdin_LINKEDIN_CREATE_LINKED_IN_POST"
    ]  # List of composio linkedin tools: https://docs.composio.dev/toolkits/linkedin

    x_tools = [t for t in mcp_manager.tools if t.name in ALLOWED_X_TOOLS]
    lkdin_tools = [t for t in mcp_manager.tools if t.name in ALLOWED_LINKEDIN_TOOLS]
    dev_tools = [t for t in mcp_manager.tools if t.name.startswith("dev_")]

    tools = x_tools + lkdin_tools + dev_tools

    agent = create_deep_agent(
        "openrouter:nvidia/nemotron-3.5-lightning:free",
        system_prompt=POSTER_SYSTEM.format(),
        tools=tools,
        state_schema=PosterAgentState,
        # Finally we didn't use this (context), because we don't need to call the tool LINKEDIN_REGISTER_IMAGE_UPLOAD, the LINKEDIN_CREATE_LINKED_IN_POST tool already do this
        # for us behind the scenes it seems. So we don't need to store the URN, we're leaving it for pedagogical purposes.
        context_schema=PosterAgentContext,
        name="M1_FP_Poster_Agent_Testing",
        checkpointer=MemorySaver(),
        # WARNING::
        # Agent
        #   ↓
        # HITL
        #   ↓ approve/edit
        # Media middleware
        #   ↓
        # Composio tool
        #
        # Do NOT pass interrupt_on=... to create_deep_agent() here. We need the HITL to happen before we get the `media_id` and `asset_urn` since they expire in secs after generation.
        middleware=[
            HumanInTheLoopMiddleware(
                interrupt_on={
                    "x_TWITTER_CREATION_OF_A_POST": {
                        "allowed_decisions": ["approve", "reject", "edit"]
                    },
                    "lkdin_LINKEDIN_CREATE_LINKED_IN_POST": {
                        "allowed_decisions": ["approve", "reject", "edit"]
                    },
                    "dev_ask_user": {"allowed_decisions": ["respond"]},
                }
            ),
            MediaMiddleware,
        ],
    )

    return agent
