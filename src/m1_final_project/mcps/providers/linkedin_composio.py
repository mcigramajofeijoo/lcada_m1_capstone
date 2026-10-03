import os
import webbrowser

from composio import SESSION_PRESET_DIRECT_TOOLS
from fastmcp.client import Client, StreamableHttpTransport


# NOTE: We intentionally don't call `get_or_create_linkedin_urn()` here.
# This function is used by `server_configs`, which is used by `MCPManager`.
# `get_or_create_linkedin_urn()`, however, depends on the `MCPManager` instance,
# which would create a circular import.
# It is also unnecessary here (we were adding it as a safety net): the LinkedIn URN is resolved in
# `main.py` and passed to the Poster Agent through runtime context, where the
# media middleware reads it when creating the post.
# from m1_final_project.agents.poster_agent.helpers import \
#     get_or_create_linkedin_urn
from m1_final_project.services.composio import composio


def get_linkedin_client(user_id: str):
    linkedin_auth_config_id = os.environ["COMPOSIO_LINKEDIN_AUTH_CONFIG_ID"]

    # Create Session
    session = composio.sessions.create(
        user_id=user_id,
        toolkits=["linkedin"],
        # tools={"linkedin": {"enable": ["LINKEDIN_CREATE_LINKED_IN_POST", "LINKEDIN_GET_MY_INFO"]}}, # `LINKEDIN_GET_MY_INFO` is a tool that gives the agent our Linkedin URN, which it needs to make a post.
        auth_configs={"linkedin": linkedin_auth_config_id},
        session_preset=SESSION_PRESET_DIRECT_TOOLS,
        mcp=True,
    )

    # Check for Duplicates
    accounts = composio.connected_accounts.list(
        user_ids=[user_id],
        auth_config_ids=[linkedin_auth_config_id],
        statuses=["ACTIVE"],
    )

    # If no active account, request connection
    if not accounts.items:
        # NOTE: We're not specifying a `callback_url` because we don't have a frontend, so if we don't provide a `callback_url`
        # the user stays in the successfull screen of Composio, which for now is good.
        connection_req = session.authorize("linkedin")
        webbrowser.open(connection_req.redirect_url)
        connection_req.wait_for_connection()
        # linkedin_urn = await get_or_create_linkedin_urn(user_id=user_id)

    # Return fastmcp client
    transport = StreamableHttpTransport(
        url=session.mcp.url, headers=session.mcp.headers
    )

    return Client(transport=transport)
