# WARNING:
# - This is intended for accessing X tools via Composio MCP server.
# - Does NOT create an OAuth instance.
# - It makes sure we've gave Composio access to our X OAuth app.
# - After consent has been made, it creates a client then used in `mcp_manager`.

import os
import webbrowser

from composio import SESSION_PRESET_DIRECT_TOOLS
from fastmcp.client import Client
from fastmcp.client.transports import StreamableHttpTransport

from m1_final_project.services.composio import composio


# INFO: If you have doubts, check ROOT / NOTES.md / Composio. It contains useful information, also you can ask official Composio
# chatbot: https://docs.composio.dev/reference/changelog?utm_source=chatgpt.com#what-changed
def get_x_client(user_id: str):
    x_auth_config_id = os.environ["COMPOSIO_X_AUTH_CONFIG_ID"]

    # NOTE: We're not including the "tools" param because we're handling this from the auth config object (web)
    session = composio.sessions.create(
        user_id=user_id,
        toolkits=["twitter"],
        auth_configs={"twitter": x_auth_config_id},
        session_preset=SESSION_PRESET_DIRECT_TOOLS,
        mcp=True,
    )

    accounts = composio.connected_accounts.list(
        user_ids=[user_id], auth_config_ids=[x_auth_config_id], statuses=["ACTIVE"]
    )

    if not accounts.items:
        # NOTE: We're not specifying a `callback_url` because we don't have a frontend, so if we don't provide a `callback_url`
        # the user stays in the successfull screen of Composio, which for now is good.
        # callback_url="http://127.0.0.1:8000/composio/x/callback"
        connection_req = session.authorize(
            toolkit="twitter"
        )  # Abstraction layer over `composio.connected_accounts.link()` method.
        webbrowser.open(connection_req.redirect_url)
        connection_req.wait_for_connection()

    transport = StreamableHttpTransport(
        url=session.mcp.url, headers=session.mcp.headers
    )

    return Client(transport=transport)
