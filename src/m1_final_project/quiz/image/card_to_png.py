# txt → png


from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT_PATH = (
    Path(__file__).resolve().parent.parent.parent / "assets" / "noto_sans_mono.ttf"
)


def card_to_png(card_text, png_path, font_size=28, padding=40):
    """
    Renders the plain-text card as a PNG (green on black) so the image model can see it.
    `card_text`: output of build_card
    `png_path`: where to save
    `padding`: border in px
    """

    font = ImageFont.truetype(str(FONT_PATH), font_size)
    lines = card_text.split("\n")

    char_w = font.getlength("M")  # monospace: every character has the same width
    line_h = font_size + 6  # vertical space per line (raise if box borders show gaps)

    width = int(max(len(l) for l in lines) * char_w) + 2 * padding
    height = len(lines) * line_h + 2 * padding

    img = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(img)

    for i, line in enumerate(lines):  # draw each line lower than the previous one
        draw.text((padding, padding + i * line_h), line, font=font, fill="white")
    img.save(png_path)
    return png_path
