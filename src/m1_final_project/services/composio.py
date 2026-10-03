from composio import Composio
from composio_langchain import LangchainProvider

# INFO: Passing a framework provider like LangchainProvider to the Composio SDK pre-formats tools into framework-ready objects with
# Pydantic argument models internally [/docs/providers/langchain#python-argument-validation]. This eliminates manual client-side
# conversion, provides built-in schema validation, and ensures direct integration without extra runtime round-trips
# [/docs/sessions-via-mcp]. You can read the full documentation at # https://docs.composio.dev/docs/providers/langchain.
composio = Composio(provider=LangchainProvider())
