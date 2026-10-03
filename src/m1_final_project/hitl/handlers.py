import questionary

from m1_final_project.hitl.registry import register_handler


@register_handler("dev_ask_user")
async def handler_dev_ask_user(req: dict) -> dict:
    args = req["args"]

    question = args["question"]
    choices = args.get("choices", [])
    allow_custom = args.get("allow_custom", False)

    if choices:
        q_choices = list(choices)

        if allow_custom:
            q_choices.append("Other")

        selected = await questionary.select(
            question,
            choices=q_choices,
        ).ask_async()

        if selected is not None and selected == "Other":
            selected = await questionary.text(
                "Specify:", instruction="You selected 'Other'."
            ).ask_async()
    else:
        selected = await questionary.text(question).ask_async()

    return {"type": "respond", "message": selected}


@register_handler("x_TWITTER_CREATION_OF_A_POST")
async def handler_publish_on_x(req: dict):
    # NOTE: When you use version="v2" with human-in-the-loop middleware, the Interrupt.value payload wraps action requests
    # in a standard dictionary format where tool parameters are keyed under "arguments" rather than "args".
    # Docs: https://docs.langchain.com/oss/python/langchain/human-in-the-loop
    args = req["args"]
    text = args["text"]  # Post content: TWITTER_CREATION_OF_A_POST.text

    print("\n" + "=" * 60)
    print("X POST — REVIEW REQUIRED")
    print("=" * 60)
    print(text)
    print("=" * 60 + "\n")

    q_choices = ["Approve", "Reject", "Edit"]

    selected = await questionary.select(
        message="Review the X post:",
        choices=q_choices,
    ).ask_async()

    if selected == "Approve":
        return {"type": "approve"}

    elif selected == "Reject":
        reason = await questionary.text(
            message="Why are you rejecting this post?",
            instruction="Enter a reason:",
        ).ask_async()

        return {
            "type": "reject",
            "message": reason,
        }

    elif selected == "Edit":
        new_text = await questionary.text(
            message="Edit the X post:",
            instruction="Enter the new post content:",
            default=text,
        ).ask_async()

        return {
            "type": "edit",
            "edited_action": {
                "name": req["name"],
                "args": {
                    **args,
                    "text": new_text,
                },
            },
        }


@register_handler("lkdin_LINKEDIN_CREATE_LINKED_IN_POST")
async def handler_publish_on_linkedin(req: dict):
    args = req["args"]
    text = args[
        "commentary"
    ]  # Post content: LINKEDIN_CREATE_LINKED_IN_POST.commentary (https://docs.composio.dev/toolkits/linkedin)

    print("\n" + "=" * 60)
    print("LINKEDIN POST — REVIEW REQUIRED")
    print("=" * 60)
    print(text)
    print("=" * 60 + "\n")

    q_choices = ["Approve", "Reject", "Edit"]

    selected = await questionary.select(
        message="Review the Linkedin post:",
        choices=q_choices,
    ).ask_async()

    if selected == "Approve":
        return {"type": "approve"}

    elif selected == "Reject":
        reason = await questionary.text(
            message="Why are you rejecting this post?",
            instruction="Enter a reason:",
        ).ask_async()

        return {
            "type": "reject",
            "message": reason,
        }

    elif selected == "Edit":
        new_text = await questionary.text(
            message="Edit the Linkedin post:",
            instruction="Enter the new post content:",
            default=text,
        ).ask_async()

        return {
            "type": "edit",
            "edited_action": {
                "name": req["name"],
                "args": {
                    **args,
                    "text": new_text,
                },
            },
        }


def default_handler(req: dict) -> dict:
    print(f"No handler for tool '{req['name']}'. Rejecting for security")
    return {
        "type": "reject",
        "message": f"There is no handler configured for tool '{req['name']}'.",
    }
