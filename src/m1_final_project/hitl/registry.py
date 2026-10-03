from collections import defaultdict
from typing import Awaitable, Callable

HandlerFn = Callable[[dict], Awaitable[dict]]
REGISTRY: dict[str, HandlerFn] = defaultdict(dict)


def register_handler(tool_name: str):
    def decorator(fn: HandlerFn) -> HandlerFn:
        if REGISTRY.get(tool_name) is not None:
            raise ValueError(
                f'There is a handler already in the registry for tool "{tool_name}"!'
            )
        REGISTRY[tool_name] = fn
        return fn

    return decorator
