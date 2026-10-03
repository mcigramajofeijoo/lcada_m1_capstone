from contextlib import AsyncExitStack

from fastmcp.client import Client
from fastmcp.client.group import ClientGroup
from langchain.mcp import MCPAdapter

from m1_final_project.mcps.server_configs import server_configs


class MCPManager:
    def __init__(self):
        self.exit_stack = AsyncExitStack()
        self.adapter = None
        self.tools = list()
        self.tools_map = dict()
        self._connected = False

    async def connect(self, user_id: str):
        if self._connected:
            return

        clients = {}
        for name, config in server_configs.items():
            if "composio" in config:
                clients[name] = config.get("composio")(user_id)
                continue

            transport = config.get("transport", None)
            url = config.get("url", None)
            auth = config.get("auth", None)

            auth_for_this_user = auth(user_id) if auth else None

            clients[name] = Client(transport(url), auth=auth_for_this_user)

        group = ClientGroup(clients)
        self.adapter = await self.exit_stack.enter_async_context(MCPAdapter(group))
        self.tools = await self.adapter.list_tools()

        # NOTE: This is useful when we need to call a specific tool, so we don't have to iterate over the entire tools of the *mcp_manager* (preventing the O(N) problem)
        # We wouldn't really need "self.tools" anymore, since we were using it when creating an agent: <>tls = [for t in mm.tools if t.name.startswith(...)]</>
        # But with the map we could do: <>tls = [t for name, t in mm.tools_map.items() if name.startswith(...)]</>
        self.tools_map = {t.name: t for t in self.tools}

        # print(self.tools)
        self._connected = True

    async def close(self):
        await self.exit_stack.aclose()


mcp_manager = MCPManager()


if __name__ == "__main__":
    mcp_manager.connect()
