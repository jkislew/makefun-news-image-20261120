#!/usr/bin/env python3
"""Draw the front page for Friday 20 November 2026.

A single 1024x1024 newspaper page that sums up the day's world news
for the make.fun bounty news-image-20261120.  Everything on the page
is typeset from the story data below with Pillow; the drawing uses no
randomness, no clock and no network, so two runs write the same file.

Run it directly to (re)create entry.png next to this script:

    python3 make_image.py
"""

from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
EDGE = 36                      # outer margin on every side
SPAN = PAGE - 2 * EDGE         # printable width

INK = (26, 24, 20)
PAPER = (247, 243, 233)
FAINT = (104, 98, 88)
CRIMSON = (158, 27, 27)
NAVY = (31, 58, 95)
PINE = (27, 94, 32)
PLUM = (84, 26, 110)
TEAL = (0, 84, 72)

FONT_DIR = Path("/usr/share/fonts/truetype/liberation")
SERIF_FILES = {
    "bold": FONT_DIR / "LiberationSerif-Bold.ttf",
    "plain": FONT_DIR / "LiberationSerif-Regular.ttf",
    "italic": FONT_DIR / "LiberationSerif-Italic.ttf",
}
SANS_FILES = {
    "bold": FONT_DIR / "LiberationSans-Bold.ttf",
    "plain": FONT_DIR / "LiberationSans-Regular.ttf",
}


def load_font(kind, style, size):
    book = SERIF_FILES if kind == "serif" else SANS_FILES
    return ImageFont.truetype(str(book[style]), size)


def text_width(draw, s, font):
    box = draw.textbbox((0, 0), s, font=font)
    return box[2] - box[0]


def fit_font(draw, s, kind, style, start, floor, target):
    """Largest size <= start whose rendering of s is <= target wide."""
    size = start
    while size > floor:
        f = load_font(kind, style, size)
        if text_width(draw, s, f) <= target:
            return f
        size -= 2
    return load_font(kind, style, floor)


def wrap_to_width(draw, s, font, limit):
    """Greedy word wrap driven by real pixel widths, not characters."""
    lines, current = [], ""
    for word in s.split():
        trial = word if not current else current + " " + word
        if text_width(draw, trial, font) <= limit:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, lines, x, y, font, leading, fill=INK, align="left"):
    for line in lines:
        lx = x
        if align == "center":
            lx = x + (SPAN - text_width(draw, line, font)) // 2
        draw.text((lx, y), line, font=font, fill=fill)
        y += leading
    return y


def rule(draw, y, weight=2, fill=INK, x0=EDGE, x1=PAGE - EDGE):
    draw.rectangle([x0, y, x1, y + weight - 1], fill=fill)
    return y + weight


# ---------------------------------------------------------------- stories
# Every fact below was checked against at least two outlets on the
# morning of 20 November 2026 (WIB) before it was set in type.

LEAD = {
    "kicker": "THE SHENZHEN SUMMIT — THE FIRST TRILATERAL MEETING OF THE THREE LEADERS",
    "headline": [
        "TRUMP, XI AND PUTIN SIGN A",
        "\u201cDECLARATION TOWARD PEACE\u201d",
    ],
    "body": (
        "The leaders of the United States, China and Russia met for 90 minutes on the "
        "sidelines of the APEC summit in Shenzhen and issued a four-point declaration: reform "
        "the United Nations, raise the world's supply of refined fuel, shield state leaders "
        "from international courts, and open a dialogue on nuclear risk. It never mentions "
        "Ukraine, Iran or North Korea — and Europe's leaders dismissed it as a photo opportunity."
    ),
}

SECOND = {
    "kicker": "THE HAGUE — A FIRST IN THE COURT'S 80 YEARS",
    "headline": [
        "WORLD COURT FINDS MYANMAR GUILTY OF",
        "GENOCIDE AGAINST THE ROHINGYA",
    ],
    "body": (
        "The International Court of Justice ruled that Myanmar committed genocide in its 2017 "
        "clearance operations in Rakhine State — the first time the court has ever held a state "
        "responsible for genocide. The Gambia brought the case. The judges ordered reparations, "
        "the safe return of the displaced, and a progress report within two years."
    ),
}

PANELS = [
    {
        "tag": "DEEP SPACE",
        "colour": NAVY,
        "headline": "VOYAGER 1 IS ONE LIGHT-DAY FROM EARTH",
        "body": (
            "16.1 billion miles (25.9 billion km) from Earth. Its radio "
            "signal now takes a full 24 hours to reach home."
        ),
    },
    {
        "tag": "MARKETS",
        "colour": PINE,
        "headline": "ANTHROPIC IPO JUMPS 17% ON DEBUT",
        "body": (
            "$81.3 billion raised — the largest IPO ever. It closed at "
            "$97.17, up 17%, as the Nasdaq fell 2%."
        ),
    },
    {
        "tag": "GAMES",
        "colour": PLUM,
        "headline": "GTA 6 EARNS $1.84 BILLION IN A DAY",
        "body": (
            "An estimated 19 million copies on day one, 75% on "
            "PlayStation 5 (Sensor Tower)."
        ),
    },
    {
        "tag": "THE STORM",
        "colour": TEAL,
        "headline": "CYCLONE AKVAN SLAMS INTO ODISHA",
        "body": (
            "Landfall near Gopalpur at Friday noon, gusts to 110 km/h. "
            "Some 300,000 people evacuated."
        ),
    },
]

TICKER_ITEMS = [
    "TRUMP: IRAN DECISION WAITS UNTIL 2027",
    "KYIV HIT BY FOUR BALLISTIC MISSILES",
    "TANKER AFIRE AFTER MINE STRIKE NEAR HORMUZ",
    "EUROPE READY FOR TALKS WITH RUSSIA",
    "HAYABUSA2 ABANDONS ITS ASTEROID LANDING",
]


# ---------------------------------------------------------------- drawing

def masthead(draw, y):
    small = load_font("sans", "bold", 19)
    draw.text((EDGE, y), "FRIDAY, 20 NOVEMBER 2026", font=small, fill=INK)
    right = "ONE PAGE \u00b7 THE WHOLE WORLD"
    draw.text((PAGE - EDGE - text_width(draw, right, small), y), right, font=small, fill=INK)
    y = rule(draw, y + 30, weight=2)
    title = fit_font(draw, "THE WORLD TODAY", "serif", "bold", 118, 60, SPAN)
    y = draw_lines(draw, ["THE WORLD TODAY"], EDGE, y + 8, title, 94, align="center")
    strap = load_font("sans", "plain", 19)
    places = "SHENZHEN \u00b7 THE HAGUE \u00b7 ODISHA \u00b7 WALL STREET \u00b7 DEEP SPACE"
    draw.text((EDGE + (SPAN - text_width(draw, places, strap)) // 2, y + 2),
              places, font=strap, fill=FAINT)
    y += 26
    y = rule(draw, y, weight=5)
    return rule(draw, y + 3, weight=1)


def story_block(draw, y, story, head_size, body_size, body_leading, head_leading):
    kick = load_font("sans", "bold", 20)
    draw.text((EDGE, y), story["kicker"], font=kick, fill=CRIMSON)
    y += 27
    head = load_font("serif", "bold", head_size)
    y = draw_lines(draw, story["headline"], EDGE, y, head, head_leading)
    y += 4
    body = load_font("serif", "plain", body_size)
    lines = wrap_to_width(draw, story["body"], body, SPAN)
    return draw_lines(draw, lines, EDGE, y, body, body_leading)


def panel(draw, x, y, width, item):
    tag = load_font("sans", "bold", 17)
    draw.text((x, y), item["tag"], font=tag, fill=item["colour"])
    y += 24
    head = load_font("sans", "bold", 22)
    lines = wrap_to_width(draw, item["headline"], head, width)
    y = draw_lines(draw, lines, x, y, head, 25)
    y += 4
    body = load_font("sans", "plain", 17)
    lines = wrap_to_width(draw, item["body"], body, width)
    return draw_lines(draw, lines, x, y, body, 21)


def ticker(draw, top):
    draw.rectangle([0, top, PAGE, PAGE], fill=INK)
    head = load_font("sans", "bold", 19)
    draw.text((EDGE, top + 10), "ALSO TODAY", font=head, fill=(255, 213, 128))
    body = load_font("sans", "bold", 17)
    joined = "  \u2022  ".join(TICKER_ITEMS)
    lines = wrap_to_width(draw, joined, body, SPAN)
    y = top + 37
    for line in lines:
        draw.text((EDGE, y), line, font=body, fill=PAPER)
        y += 22
    return y


def compose():
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(img)
    y = masthead(draw, 24)
    y += 10
    y = story_block(draw, y, LEAD, head_size=54, body_size=20,
                    body_leading=26, head_leading=61)
    y += 6
    y = rule(draw, y, weight=2)
    y += 10
    y = story_block(draw, y, SECOND, head_size=39, body_size=20,
                    body_leading=25, head_leading=46)
    y += 6
    y = rule(draw, y, weight=2)
    y += 10
    label = load_font("sans", "bold", 18)
    draw.text((EDGE, y), "IN BRIEF — FOUR MORE STORIES", font=label, fill=INK)
    y += 25
    gap = 22
    col = (SPAN - 3 * gap) // 4
    ends = []
    for i, item in enumerate(PANELS):
        x = EDGE + i * (col + gap)
        if i:
            draw.line([x - gap // 2, y, x - gap // 2, y + 178], fill=FAINT, width=1)
        ends.append(panel(draw, x, y, col, item))
    y = max(ends)
    ticker(draw, max(y + 14, PAGE - 116))
    return img


def main():
    out = Path(__file__).resolve().parent / "entry.png"
    compose().save(out, format="PNG", optimize=False)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
