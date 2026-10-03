import base64
import mimetypes
from pathlib import Path

from openai import APIConnectionError, APITimeoutError, OpenAI, RateLimitError
from tenacity import retry_if_exception_type

from m1_final_project.my_tenacity import standard_retry
from m1_final_project.quiz.prompts import IMAGE_PROMPT

client = OpenAI()


@standard_retry(
    retry=retry_if_exception_type((RateLimitError, APIConnectionError, APITimeoutError))
)
def generate_card_image_openai(png_path, out_path):
    """
    Sends the card PNG + prompt to Gemini and saves the edited image.

    `png_path`: card rendered by card_to_png
    `out_path`: where to save the AI image
    """
    prompt = IMAGE_PROMPT.format()

    with open(png_path, "rb") as f:
        response = client.images.edit(
            model="gpt-image-2", image=f, prompt=prompt, size="1024x1024"
        )

    img_b64 = response.data[0].b64_json
    img_bytes = base64.b64decode(img_b64)

    path_obj = Path(out_path)
    path_obj.write_bytes(img_bytes)

    mimetype, _ = mimetypes.guess_type(out_path)
    mimetype = mimetype or "image/png"

    return {
        "out_path": str(path_obj),
        "filename": path_obj.name,
        "mimetype": mimetype,
        "bytes": img_bytes,
    }
