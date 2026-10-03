from fastmcp.client.transports import StreamableHttpTransport

from m1_final_project.mcps.providers.linkedin_composio import get_linkedin_client

# from m1_final_project.mcps.providers.x import x_auth
from m1_final_project.mcps.providers.x_composio import get_x_client

server_configs = {
    "docs_langchain": {
        "transport": lambda url: StreamableHttpTransport(url=url),
        "url": "https://docs.langchain.com/mcp",
        "auth": None,
    },
    "dev": {
        "transport": lambda url: StreamableHttpTransport(url=url),
        "url": "http://127.0.0.1:8000/mcp",
        "auth": None,
    },
    "x": {"composio": get_x_client},
    "lkdin": {"composio": get_linkedin_client},
    # INFO: X official MCP does NOT expose a tool to create tweets!
    # "x": {
    #     "transport": lambda url: StreamableHttpTransport(url=url),
    #     "url": "https://api.x.com/mcp",
    #     "auth": x_auth
    # }
}
