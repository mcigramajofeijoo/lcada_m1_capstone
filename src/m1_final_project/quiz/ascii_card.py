import re
import textwrap
from pathlib import Path

from m1_final_project.quiz.questions import AXES
from uuid import uuid4

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

INDENT = "  "
BAR_WIDTH = 14  # Total blocks in each meter
RESET, BOLD, GREEN = "\033[0m", "\033[1m", "\033[92m"  # ANSI codes: Terminal only

DEFAULT_MASCOT = "\n".join(
    [
        " ___",
        "[o_o]",
        "/|_|\\",
        " | |",
    ]
)


def build_meter(left, right, score, left_w, right_w):
    """
    One line like: Chaotic  [██████░░░░░░░░] Organized      Chaotic 60%

    score: 0-100 toward the right label.
    left_w/right_w: pad labels so columns align
    """
    filled = round(BAR_WIDTH * score / 100)
    bar = "█" * filled + "░" * (BAR_WIDTH - filled)

    # which side wins and by how much (score 40 -> Chaotic 60%)
    lean, pct = (right, score) if score >= 50 else (left, 100 - score)

    # NOTE:
    # - `<` forces the text to be left-aligned.
    # - `{left_w}` is a nested variable that dynamically sets the total width (number of characters) allocated for that column.
    return f"{INDENT}{left:<{left_w}} {bar} {right:<{right_w}}   {lean} {pct}%"


def build_card(
    title, trait, product, scores, verdict, judge_name, mascot=DEFAULT_MASCOT
):
    # INFO: Refer to ROOT / NOTES.md -> `ASCII Card – Build Card` section for some information it may be useful.
    lines = []  # the card, top to bottom, one string per line

    width = max(len(title) + 4, 24)  # inner width of the title box
    box_width = width + 2  # + the two border characters ┌ ┐

    # 1. Mascot, centered over the box
    art_lines = mascot.split("\n")  # one string per row of the drawing
    art_width = max(len(row) for row in art_lines)  # widest row of the drawing
    pad = INDENT + " " * (
        (box_width - art_width) // 2
    )  # left margin, same for EVERY row (this centers the art in the title box, see an output example to understand better)
    lines.append("")
    for row in art_lines:
        lines.append(pad + row)

    # 2. Title box
    lines.append("")
    lines.append(INDENT + "┌" + "─" * width + "┐")
    lines.append(INDENT + "│" + title.upper().center(width) + "│")
    lines.append(INDENT + "└" + "─" * width + "┘")

    # 3. Dominant trait and product
    lines.append("")
    lines.append(f"{INDENT}Dominant trait : {trait}")
    lines.append(f"{INDENT}Best match     : LangChain {product}")

    # 4. One meter per axis
    lines.append("")
    left_w = max(len(left) for _, left, _ in AXES)  # longest left label
    right_w = max(len(right) for _, _, right in AXES)  # longest right label
    for axis_id, left, right in AXES:
        lines.append(build_meter(left, right, scores[axis_id], left_w, right_w))

    # 5. Verdict, wrapped in quotes
    lines.append("")
    wrapped = textwrap.wrap(verdict, width=44) or [
        ""
    ]  # list of lines, each <= 44 chars
    wrapped[0] = f'"{wrapped[0]}'  # opening quote on the first line
    wrapped[-1] = f'{wrapped[-1]}"'  # closing quote on the last line
    for row in wrapped:
        lines.append(INDENT + row)

    # 6. Footer
    lines.append("")
    lines.append(f"{INDENT}Judged by {judge_name}")
    lines.append("")

    return "\n".join(lines)  # glue all lines with line breaks


def save_card(card_text, judge_name, title):
    """Saves the plain-text card to output/ and returns the file path."""

    # INFO: Refer to ROOT / NOTES.md -> `ASCII Card – Save Card` section for useful information about this code.
    random_id = uuid4().hex
    slug = re.sub(r"[^a-z0-9]+", "_", f"{judge_name}_{title}.txt".lower()).strip("_")
    path = OUTPUT_DIR / f"{slug}_{random_id}.txt"
    path.write_text(card_text, encoding="utf-8")
    return path


def print_card(card_text, color=GREEN):
    print(f"{color}{BOLD}{card_text}{RESET}")
