"""Writes the light and dark SVGs in assets/apple/ used by README.md.

Run from the repo root: python3 tools/build_svgs.py
Text lives here, so a changed number or heading is one edit and one rerun.
"""

from pathlib import Path
from xml.sax.saxutils import escape

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "assets" / "apple"

FONT_STACK = (
    "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', "
    "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
)

THEMES = {
    "light": {"primary": "#1d1d1f", "secondary": "#6e6e73", "accent": "#0071e3", "tile": "#f5f5f7"},
    "dark": {"primary": "#f5f5f7", "secondary": "#a1a1a6", "accent": "#2997ff", "tile": "#1c1c1e"},
}

HERO = {
    "eyebrow": "Google Developer Expert, Flutter & Dart",
    "name": "Esra Kadah",
    "title": "Tech Lead, Senior Flutter & AI Engineer",
}

STAT_TILES = [
    {"eyebrow": "Google Developer Expert", "figure": "GDE", "caption": ["Recognized by Google", "for Flutter & Dart."]},
    {"eyebrow": "Flutter Community AI Circle", "figure": "29", "caption": ["Livestream episodes,", "co-founded and co-hosted."]},
    {"eyebrow": "Flutter Design Patterns", "figure": "#1", "caption": ["Amazon Best Seller at launch,", "co-authored for Packt."]},
    {"eyebrow": "On stage", "figure": "20+", "caption": ["Talks and workshops", "since 2022."]},
]

SECTION_HEADINGS = {
    "now": ("Now.", "Where I'll be next."),
    "work": ("Work.", "Flutter and Gemini, shipped."),
    "stage": ("On stage.", "Talks and workshops."),
    "writing": ("Writing.", "Notes from building it."),
    "community": ("Community.", "Where I organize."),
}

HERO_WIDTH = 800
HERO_HEIGHT = 200
TILE_WIDTH = 388
TILE_HEIGHT = 260
TILE_GAP = 24
TILE_RADIUS = 28
TILE_PADDING = 36
HEADING_WIDTH = 800
HEADING_HEIGHT = 72


def svg_document(width: int, height: int, label: str, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{escape(label)}">\n'
        f"<title>{escape(label)}</title>\n{body}</svg>\n"
    )


def text(x: float, y: float, content: str, size: int, weight: int, fill: str, anchor: str = "start",
         tracking: float = 0) -> str:
    return (
        f'<text x="{x}" y="{y}" font-family="{FONT_STACK}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}" letter-spacing="{tracking}">{escape(content)}</text>\n'
    )


def hero_svg(theme: dict) -> str:
    center = HERO_WIDTH / 2
    body = (
        text(center, 36, HERO["eyebrow"], 22, 600, theme["accent"], "middle")
        + text(center, 124, HERO["name"], 80, 700, theme["primary"], "middle", -2)
        + text(center, 178, HERO["title"], 30, 500, theme["secondary"], "middle", -0.3)
    )
    label = f'{HERO["name"]}, {HERO["title"]}. {HERO["eyebrow"]}.'
    return svg_document(HERO_WIDTH, HERO_HEIGHT, label, body)


def stats_svg(theme: dict) -> str:
    columns = 2
    rows = (len(STAT_TILES) + columns - 1) // columns
    width = columns * TILE_WIDTH + (columns - 1) * TILE_GAP
    height = rows * TILE_HEIGHT + (rows - 1) * TILE_GAP
    body = ""
    for index, tile in enumerate(STAT_TILES):
        left = (index % columns) * (TILE_WIDTH + TILE_GAP)
        top = (index // columns) * (TILE_HEIGHT + TILE_GAP)
        body += (
            f'<rect x="{left}" y="{top}" width="{TILE_WIDTH}" height="{TILE_HEIGHT}" '
            f'rx="{TILE_RADIUS}" fill="{theme["tile"]}"/>\n'
        )
        x = left + TILE_PADDING
        body += text(x, top + 58, tile["eyebrow"], 20, 600, theme["accent"])
        body += text(x, top + 150, tile["figure"], 84, 700, theme["primary"], tracking=-2.5)
        for line_index, line in enumerate(tile["caption"]):
            body += text(x, top + 196 + line_index * 30, line, 23, 500, theme["secondary"], tracking=-0.2)
    label = " ".join(f'{tile["figure"]}: {" ".join(tile["caption"])}' for tile in STAT_TILES)
    return svg_document(width, height, label, body)


def heading_svg(theme: dict, lead: str, rest: str) -> str:
    size = 44
    body = (
        f'<text x="0" y="54" font-family="{FONT_STACK}" font-size="{size}" font-weight="700" '
        f'letter-spacing="-1">'
        f'<tspan fill="{theme["primary"]}">{escape(lead)}</tspan>'
        f'<tspan fill="{theme["secondary"]}"> {escape(rest)}</tspan></text>\n'
    )
    return svg_document(HEADING_WIDTH, HEADING_HEIGHT, f"{lead} {rest}", body)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for theme_name, theme in THEMES.items():
        (OUTPUT_DIR / f"hero-{theme_name}.svg").write_text(hero_svg(theme), encoding="utf-8")
        (OUTPUT_DIR / f"stats-{theme_name}.svg").write_text(stats_svg(theme), encoding="utf-8")
        for key, (lead, rest) in SECTION_HEADINGS.items():
            (OUTPUT_DIR / f"heading-{key}-{theme_name}.svg").write_text(
                heading_svg(theme, lead, rest), encoding="utf-8"
            )


if __name__ == "__main__":
    main()
