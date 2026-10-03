from dotenv import load_dotenv

load_dotenv()

import asyncio

from langchain.messages import HumanMessage

from m1_final_project.agents.registry import agent_registry
from m1_final_project.mcps.mcp_manager import mcp_manager


async def main():
    dummy_user_id = "dummy_04_lin3"

    # Connect MCP
    await mcp_manager.connect(user_id=dummy_user_id)

    # Build agents
    agent_registry.build()

    # Invoke
    poster = agent_registry.poster_agent

    response = await poster.ainvoke(
        {
            "messages": [
                HumanMessage(
                    content="Make a post in my Linkedin expressing i'm testing Composio 'Linkedin' MCP, and if they're seeing this then probably works fine, hehe."
                )
            ]
        }
    )

    print(response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
