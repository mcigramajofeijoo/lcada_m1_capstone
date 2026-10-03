import mimetypes
from pathlib import Path

DUMMY_IMAGE_PATH = Path(__file__).parent.parent.parent / "assets" / "dummy_card.png"


def generate_card_image_dummy():
    """
    Drop-in replacement for generate_card_image_*. No genera nada: solo
    devuelve la ruta de una imagen ya creada a mano.
    """
    print(
        f"[DUMMY] using pre-generated card image instead of calling OpenAI/Gemini API: {DUMMY_IMAGE_PATH}"
    )

    path_obj = Path(DUMMY_IMAGE_PATH)
    img_bytes = path_obj.read_bytes()

    path_obj.write_bytes(img_bytes)

    mimetype, _ = mimetypes.guess_type(DUMMY_IMAGE_PATH)
    mimetype = mimetype or "image/png"

    return {
        "out_path": str(path_obj),
        "filename": path_obj.name,
        "mimetype": mimetype,
        "bytes": img_bytes,
    }
