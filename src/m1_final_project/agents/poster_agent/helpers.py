from dotenv import load_dotenv

load_dotenv()

import hashlib
import os

import httpx2
from composio import Composio

from m1_final_project.mcps.mcp_manager import mcp_manager
from m1_final_project.storage.linkedin_store import linkedin_store
import json
import asyncio


async def get_s3_presigned_url_and_key(
    file_bytes: bytes, toolkit_slug: str, tool_slug: str, filename: str, mimetype: str
) -> str:
    md5 = hashlib.md5(file_bytes).hexdigest()

    async with httpx2.AsyncClient() as client:
        # Get presigned URL
        response = await client.post(
            url="https://backend.composio.dev/api/v3/files/upload/request",
            json={
                "toolkit_slug": toolkit_slug,
                "tool_slug": tool_slug,
                "filename": filename,
                "mimetype": mimetype,
                "md5": md5,
            },
            headers={
                "Content-Type": "application/json",
                "x-api-key": os.environ["COMPOSIO_API_KEY"],
            },
        )

        response.raise_for_status()
        data = response.json()

    return (data["new_presigned_url"], data["key"])


async def stage_file_in_composio_storage(
    file_bytes: bytes, toolkit_slug: str, tool_slug: str, filename: str, mimetype: str
) -> str:
    new_presigned_url, key = await get_s3_presigned_url_and_key(
        file_bytes=file_bytes,
        toolkit_slug=toolkit_slug,
        tool_slug=tool_slug,
        filename=filename,
        mimetype=mimetype,
    )

    async with httpx2.AsyncClient() as client:
        await client.put(
            url=new_presigned_url,
            content=file_bytes,
            headers={"Content-Type": mimetype},
        )

    return key


# TODO: Check we're parsing the returned value correctly!
async def get_x_media_id(
    s3_key: str, filename: str, mimetype: str, media_category: str = "tweet_image"
):
    # - In order to see the input schema of this tool, you can go here: https://docs.composio.dev/toolkits/twitter
    # - To see the input and output schema in detail, you need to call the meta tool "COMPOSIO_GET_TOOL_SCHEMAS" (you can use the `get_tool_schemas` tool defined in this file): https://docs.composio.dev/toolkits/meta-tools/get_tool_schemas
    # - You can see the JSON with both schemas in ROOT / NOTES.md / "Input & Output Schema of TWITTER_UPLOAD_MEDIA" (26 Sep, 2026)
    upload_media = mcp_manager.tools_map.get("x_TWITTER_UPLOAD_MEDIA", None)
    if not upload_media:
        raise ValueError("The x_TWITTER_UPLOAD_MEDIA tool was not found.")

    raw_res = await upload_media.ainvoke(
        input={
            "media": {"name": filename, "s3Key": s3_key, "mimetype": mimetype},
            "media_category": media_category,
        }
    )

    inner_text_str = raw_res[0]["text"]
    res = json.loads(inner_text_str)

    if not res.get("successful"):
        raise RuntimeError(f"Failed to upload media to X: {raw_res}")

    return res["data"]["data"]["id"]


async def upload_file_to_x(
    file_bytes: bytes, toolkit_slug: str, tool_slug: str, filename: str, mimetype: str
):
    """
    Deterministically upload a file to X through Composio.

    Returns:
        media_id
    """
    try:
        s3_key = await stage_file_in_composio_storage(
            file_bytes=file_bytes,
            toolkit_slug=toolkit_slug,
            tool_slug=tool_slug,
            filename=filename,
            mimetype=mimetype,
        )

        media_id = await get_x_media_id(
            s3_key=s3_key, filename=filename, mimetype=mimetype
        )

        return media_id
    except Exception as exc:
        print(
            f'Something went wrong uploading the file "{filename}" ({mimetype}) to X.'
            f"\nError: {type(exc).__name__}"
            f"\nTraceback: {exc}"
        )
        raise exc


# NOTE: Currently not being used.
# TODO: Check we're parsing the returned value correctly!
async def get_linkedin_asset_urn(owner_urn: str, file_bytes: bytes) -> str:
    """
    Register an image upload through Composio's LinkedIn toolkit, upload the
    image bytes to LinkedIn's presigned URL, and return the resulting asset URN.

    Args:
        file_bytes: Raw bytes of the image to upload.
        owner_urn: LinkedIn URN of the user or organization that will own the image.

    Returns:
        The LinkedIn asset URN (later used in `LINKEDIN_CREATE_LINKED_IN_POST`).
    """
    register_img_up = mcp_manager.tools_map.get(
        "lkdin_LINKEDIN_REGISTER_IMAGE_UPLOAD", None
    )
    if not register_img_up:
        raise ValueError(
            'The "lkdin_LINKEDIN_REGISTER_IMAGE_UPLOAD" tool was not found.'
        )

    raw_res = await register_img_up.ainvoke({"owner_urn": owner_urn})
    inner_text_str = raw_res[0]["text"]
    res = json.loads(inner_text_str)

    if not res.get("successful", False):
        raise RuntimeError(f"Failed to register LinkedIn image upload: {res}")

    data = res["data"]

    async with httpx2.AsyncClient() as client:
        response = await client.put(
            url=data["upload_url"],
            content=file_bytes,
            headers=data.get("upload_headers", {}),
        )

        response.raise_for_status()

    return data["asset_urn"]


# Utility
def get_tool_schemas(
    tool_slugs: list[str],  # Toolkit tool(s)
    schemas: list[str],  # ['input_schema', 'output_schema']
):
    composio = Composio(api_key=os.environ["COMPOSIO_API_KEY"])
    session = composio.sessions.create(user_id="temp_system_user")

    response = session.execute(
        tool_slug="COMPOSIO_GET_TOOL_SCHEMAS",
        arguments={"tool_slugs": tool_slugs, "include": schemas},
    )

    session.delete()

    return response


async def get_or_create_linkedin_urn(user_id: str):
    record = await linkedin_store.get(user_id)
    if record:
        return record["urn"]

    # Get info, set it in Redis, return URN.
    get_my_info = mcp_manager.tools_map.get("lkdin_LINKEDIN_GET_MY_INFO", None)
    if not get_my_info:
        raise RuntimeError(
            "The LinkedIn GET_MY_INFO tool was not found (lkdin_LINKEDIN_GET_MY_INFO)."
        )

    raw_res = await get_my_info.ainvoke(
        {}
    )  # To see what this is returning, go to ROOT / NOTES.md / "get_or_create_linkedin_urn Invoke Response"
    inner_text_str = raw_res[0]["text"]
    res = json.loads(inner_text_str)

    if not res.get("successful", None):
        raise RuntimeError(f"Failed to retrieve LinkedIn user info: {raw_res}")

    data = res["data"]
    urn = data["id"]

    await linkedin_store.set(user_id=user_id, urn=urn)
    return urn


if __name__ == "__main__":
    # NOTE: If executing directly we need to call `load_dotenv` at the top of the file.
    # WARNING: Also, we need to comment the line inside `/mcps/providers/linkedin_composio.py/get_linkedin_client (fn)` where we call "get_or_create_linkedin_urn", otherwise we get a circular import exception.
    # response = get_tool_schemas(
    #     tool_slugs=["LINKEDIN_GET_MY_INFO"],
    #     schemas=["output_schema"],
    # )
    # print(response)
    async def run():
        await mcp_manager.connect(user_id="007")
        asset_urn = await get_linkedin_asset_urn(
            owner_urn="vZ9VsVYm9G", file_bytes=b"1234567"
        )
        print(asset_urn)

    asyncio.run(run())
