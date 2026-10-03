from dotenv import load_dotenv

load_dotenv()

from pathlib import Path

from m1_final_project.quiz.image.card_to_png import card_to_png
from m1_final_project.quiz.image.dummy_gen import generate_card_image_dummy

txt = next(Path("output").glob("*.txt"))
png = card_to_png(txt.read_text(encoding="utf-8"), txt.with_suffix(".png"))
ai_img_path = generate_card_image_dummy()
