from typing import Awaitable, Callable, Union

from langchain.agents.middleware import ToolCallRequest, wrap_tool_call
from langchain.messages import ToolMessage
from langgraph.types import Command

from m1_final_project.agents.poster_agent.helpers import (
    stage_file_in_composio_storage,
    upload_file_to_x,
)
from m1_final_project.storage.attachment_store import attachment_store

TOOL_OUTPUT = Union[ToolMessage, Command]

X_CREATE_POST = {
    "w_prefix": "x_TWITTER_CREATION_OF_A_POST",
    "raw": "TWITTER_CREATION_OF_A_POST",
}
LINKEDIN_CREATE_POST = {
    "w_prefix": "lkdin_LINKEDIN_CREATE_LINKED_IN_POST",
    "raw": "LINKEDIN_CREATE_LINKED_IN_POST",
}


POST_TOOLS = {
    X_CREATE_POST["w_prefix"],
    LINKEDIN_CREATE_POST["w_prefix"],
}


@wrap_tool_call
async def MediaMiddleware(
    req: ToolCallRequest, handler: Callable[[ToolCallRequest], Awaitable[TOOL_OUTPUT]]
) -> Awaitable[TOOL_OUTPUT]:
    tool_name = req.tool_call["name"]
    # Not a social-post tool → execute normally.
    if tool_name not in POST_TOOLS:
        return await handler(req)

    attachment_id = req.state.get("attachment_id", None)
    # The attachment ID should have been created and stored in the state
    # immediately after generating the AI image. Reaching this point without
    # one indicates an unexpected state inconsistency.
    if not attachment_id:
        raise RuntimeError(
            "No `attachment_id` found in STATE. It's required for post creation."
        )

    file = await attachment_store.get(
        attachment_id=attachment_id
    )  # If nothing found, will raise an error.

    args = req.tool_call["args"]

    # -----------------------------------------------------------------------
    # X / Twitter
    # -----------------------------------------------------------------------
    if tool_name == X_CREATE_POST["w_prefix"]:
        media_id = await upload_file_to_x(
            file_bytes=file["file_bytes"],
            filename=file["filename"],
            mimetype=file["mimetype"],
            toolkit_slug="twitter",
            tool_slug=X_CREATE_POST["raw"],
        )

        updated_args = {**args, "media_media_ids": [media_id]}
    elif tool_name == LINKEDIN_CREATE_POST["w_prefix"]:
        user_urn = req.runtime.context.linkedin_user_urn
        if not user_urn:
            raise RuntimeError(
                "Error: No Linkedin user URN found in agent context. This should be here. Devs, take action!"
            )

        s3_key = await stage_file_in_composio_storage(
            file_bytes=file["file_bytes"],
            filename=file["filename"],
            mimetype=file["mimetype"],
            toolkit_slug="linkedin",
            tool_slug=LINKEDIN_CREATE_POST["raw"],
        )

        updated_args = {
            **args,
            "author": f"urn:li:person:{user_urn}",
            "images": [
                {
                    "name": file["filename"],
                    "s3Key": s3_key,
                    "mimetype": file["mimetype"],
                }
            ],
        }

    req = req.override(tool_call={**req.tool_call, "args": updated_args})

    return await handler(req)
