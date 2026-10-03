import mimetypes
from io import BytesIO
from pathlib import Path

import httpx
from google import genai
from google.genai.errors import ClientError, ServerError
from google.genai.types import GenerateContentConfig, Modality
from PIL import Image
from tenacity import retry_if_exception

from m1_final_project.my_tenacity import standard_retry
from m1_final_project.quiz.prompts import IMAGE_PROMPT

client = genai.Client()


def _is_transient_error(exc: BaseException) -> bool:
    """True solo para errores de red o de servidor/rate-limit, nunca para
    errores de request malformado o de autenticación."""
    if isinstance(exc, ServerError):
        return True  # 5xx: siempre transitorio

    elif isinstance(exc, ClientError):
        return exc.code == 429  # de los 4xx, solo el rate limit es transitorio

    # NOTE: Why are we checking these httpx exceptions for Gemini but not for OpenAI? Go to ROOT / "NOTES.md" -> "Why are we catching *httpx* exceptions when using `google-genai` but not when using `openai`?"
    return isinstance(
        exc, (httpx.ConnectError, httpx.TimeoutException)
    )  # falla de red antes de llegar al servidor


@standard_retry(retry=retry_if_exception(_is_transient_error))
def generate_card_image_gemini(png_path, out_path):
    """
    Sends the card PNG + prompt to Gemini and saves the edited image.

    `png_path`: card rendered by card_to_png
    `out_path`: where to save the AI image
    """

    # If not using PIL:
    # with open(png_path, "rb") as f:
    #     image_bytes = f.read()

    # source_image = {"mime_type": "image/png", "data": image_bytes}

    source_image = Image.open(png_path)

    prompt = IMAGE_PROMPT.format()

    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[source_image, prompt],  # imagen + texto, en ese orden
        config=GenerateContentConfig(
            response_modalities=[Modality.TEXT, Modality.IMAGE]
        ),
    )

    img_bytes = None

    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            # If not using PIL:
            # with open(out_path, "wb") as f:
            #     f.write(part.inline_data.data)

            # In here, we're using PIL to write the bytes, but we could also use Path.
            # Pro of PIL: It acts as a safety validation layer. If Gemini returns invalid image data, Image.open() will throw an error immediately, preventing you from saving a broken file. You can also change formats easily (e.g., saving a PNG source as a JPEG).
            img_bytes = part.inline_data.data

            result_image = Image.open(BytesIO(img_bytes))
            result_image.save(out_path)

            path_obj = Path(out_path)
            mimetype, _ = mimetypes.guess_type(out_path)
            mimetype = mimetype or "image/png"

            return {
                "out_path": str(path_obj),
                "filename": path_obj.name,
                "mimetype": mimetype,
                "bytes": img_bytes,
            }
    raise RuntimeError(
        "Model didn't return any image."
    )  # por si solo devuelve texto (ej. rechazo de contenido)
