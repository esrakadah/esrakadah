"""Writes the light and dark SVGs in assets/apple/ used by README.md.

Run from the repo root: python3 tools/build_svgs.py
Text and design tokens live here, so a changed number, heading or colour is one edit and one rerun.
Never hand-edit the generated SVGs.

Colour roles follow Material 3: one tonal palette derived from the seed colour (Flutter blue #0553B1,
HCT hue 266), with a primary, an on-surface and an on-surface-variant role per theme. Tones were taken
from material-color-utilities (TonalPalette, chroma 56 for primary, 6 to 8 for the neutrals).
Every text colour passes WCAG AA on the GitHub page colour of its theme (checked in check_contrast()).
"""

from pathlib import Path
from xml.sax.saxutils import escape

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "assets" / "apple"

FONT_STACK = (
    "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', "
    "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
)

# Material 3 roles per theme. "page" is the GitHub page colour the SVG sits on (used only for checks).
THEMES = {
    "light": {
        "page": "#ffffff",
        "primary": "#195bb9",  # primary tone 40
        "on_surface": "#1a1b20",  # neutral tone 10
        "on_surface_variant": "#44474f",  # neutral variant tone 30
        "container": "#edf0ff",  # primary tone 95
        "outline": "#d8e2ff",  # primary tone 90
    },
    "dark": {
        "page": "#0d1117",
        "primary": "#adc6ff",  # primary tone 80
        "on_surface": "#e2e2e9",  # neutral tone 90
        "on_surface_variant": "#c4c6d0",  # neutral variant tone 80
        "container": "#002e69",  # primary tone 20, drawn at CONTAINER_OPACITY_DARK
        "outline": "#004494",  # primary tone 30
    },
}
CONTAINER_OPACITY_DARK = 0.6

# Type scale (SVG units). One size per role, the same in every SVG.
TYPE = {
    "display": {"size": 88, "weight": 700, "tracking": -2.5},
    "hero_name": {"size": 80, "weight": 700, "tracking": -2},
    "headline": {"size": 44, "weight": 700, "tracking": -1},
    "title": {"size": 30, "weight": 500, "tracking": -0.3},
    "label": {"size": 24, "weight": 600, "tracking": 0},
    "body": {"size": 24, "weight": 500, "tracking": -0.1},
}

GRID = 8  # every offset below is a multiple of the 8 pt grid

HERO = {
    "eyebrow": "Google Developer Expert, Flutter & Dart",
    "name": "Esra Kadah",
    "title": "Tech Lead, Senior Flutter & AI Engineer",
}

# Only facts with a written source (see the GBU archive). No number without one.
STAT_TILES = [
    {"eyebrow": "Named by Google", "figure": "GDE", "caption": ["Developer Expert,", "Flutter and Dart"],
     "alt": "GDE: Google Developer Expert for Flutter and Dart."},
    {"eyebrow": "On stage", "figure": "20+", "caption": ["Talks & workshops", "since 2022"],
     "alt": "20+ talks and workshops since 2022."},
    {"eyebrow": "Packt book, 2024", "figure": "Book", "caption": ["Co-author, Flutter", "Design Patterns", "and Best Practices"],
     "alt": "Book: co-author of Flutter Design Patterns and Best Practices, Packt 2024."},
    {"eyebrow": "Since May 2025", "figure": "Live", "caption": ["Co-host, Flutter", "Community AI", "Circle stream"],
     "alt": "Live: co-host of the Flutter Community AI Circle stream since May 2025."},
]

SECTION_HEADINGS = {
    "now": ("Now.", "Where I'll be next."),
    "work": ("Work.", "Flutter and Gemini, shipped."),
    "stage": ("On stage.", "Talks and workshops."),
    "writing": ("Writing.", "Notes from building it."),
    "community": ("Community.", "Where I organize."),
}

HERO_WIDTH = 600
HERO_HEIGHT = 200

# Every wide visual has two layouts. README serves them through <picture> with a width media query:
# "compact" up to COMPACT_BREAKPOINT px of viewport, "wide" above it. Both are shown at width="100%",
# because GitHub gives an <img> inside <picture> no max-width, so a fixed pixel width would overflow a phone.
COMPACT_BREAKPOINT = 767
PHONE_CONTENT_WIDTH = 343  # 375 px viewport minus GitHub's 16 px gutters
SMALL_DESKTOP_CONTENT_WIDTH = 736  # 768 px viewport, the narrowest "wide" layout

TILE_WIDTH = 328
TILE_HEIGHT = 312
TILE_GAP = 16
TILE_RADIUS = 32
TILE_PADDING = 24
LINE_HEIGHT = 32
STATS_COLUMNS = {"wide": 4, "compact": 2}


def stats_width(layout: str) -> int:
    columns = STATS_COLUMNS[layout]
    return columns * TILE_WIDTH + (columns - 1) * TILE_GAP


# Headings: one line on a wide canvas, so every heading shares one scale; two lines on a phone.
HEADING_WIDE_CANVAS = 1800
HEADING_WIDE_HEIGHT = 72
HEADING_COMPACT_CANVAS = 640
HEADING_COMPACT_HEIGHT = 112

# Widest average advance measured in the fallback fonts (Inter Medium, 0.56 of the font size),
# plus 12 percent margin, so a line that passes here fits in every font of FONT_STACK.
WIDTH_FACTOR = 0.56 * 1.12


def text_width(content: str, role: str) -> float:
    return len(content) * TYPE[role]["size"] * WIDTH_FACTOR


def svg_document(width: int, height: int, label: str, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{escape(label)}">\n'
        f"<title>{escape(label)}</title>\n{body}</svg>\n"
    )


def text(x: float, y: float, content: str, role: str, fill: str, anchor: str = "start") -> str:
    style = TYPE[role]
    return (
        f'<text x="{x}" y="{y}" font-family="{FONT_STACK}" font-size="{style["size"]}" '
        f'font-weight="{style["weight"]}" fill="{fill}" text-anchor="{anchor}" '
        f'letter-spacing="{style["tracking"]}">{escape(content)}</text>\n'
    )


def hero_svg(theme: dict) -> str:
    center = HERO_WIDTH / 2
    body = (
        text(center, 4.5 * GRID, HERO["eyebrow"], "label", theme["primary"], "middle")
        + text(center, 15.5 * GRID, HERO["name"], "hero_name", theme["on_surface"], "middle")
        + text(center, 22 * GRID, HERO["title"], "title", theme["on_surface_variant"], "middle")
    )
    label = f'{HERO["name"]}, {HERO["title"]}. {HERO["eyebrow"]}.'
    return svg_document(HERO_WIDTH, HERO_HEIGHT, label, body)


def stats_svg(theme_name: str, theme: dict, layout: str) -> str:
    columns = STATS_COLUMNS[layout]
    rows = (len(STAT_TILES) + columns - 1) // columns
    height = rows * TILE_HEIGHT + (rows - 1) * TILE_GAP
    opacity = CONTAINER_OPACITY_DARK if theme_name == "dark" else 1
    body = ""
    for index, tile in enumerate(STAT_TILES):
        left = (index % columns) * (TILE_WIDTH + TILE_GAP)
        top = (index // columns) * (TILE_HEIGHT + TILE_GAP)
        body += (
            f'<rect x="{left}" y="{top}" width="{TILE_WIDTH}" height="{TILE_HEIGHT}" rx="{TILE_RADIUS}" '
            f'fill="{theme["container"]}" fill-opacity="{opacity}"/>\n'
        )
        x = left + TILE_PADDING
        body += text(x, top + 7 * GRID, tile["eyebrow"], "label", theme["primary"])
        body += text(x, top + 19 * GRID, tile["figure"], "display", theme["on_surface"])
        for line_index, line in enumerate(tile["caption"]):
            body += text(x, top + 25 * GRID + line_index * LINE_HEIGHT, line, "body", theme["on_surface_variant"])
    label = " ".join(tile["alt"] for tile in STAT_TILES)
    return svg_document(stats_width(layout), height, label, body)


def heading_svg(theme: dict, lead: str, rest: str, layout: str) -> str:
    if layout == "wide":
        style = TYPE["headline"]
        body = (
            f'<text x="0" y="54" font-family="{FONT_STACK}" font-size="{style["size"]}" '
            f'font-weight="{style["weight"]}" letter-spacing="{style["tracking"]}">'
            f'<tspan fill="{theme["on_surface"]}">{escape(lead)}</tspan>'
            f'<tspan fill="{theme["on_surface_variant"]}"> {escape(rest)}</tspan></text>\n'
        )
        return svg_document(HEADING_WIDE_CANVAS, HEADING_WIDE_HEIGHT, f"{lead} {rest}", body)
    body = text(0, 6.5 * GRID, lead, "headline", theme["on_surface"]) + text(
        0, 12 * GRID, rest, "title", theme["on_surface_variant"]
    )
    return svg_document(HEADING_COMPACT_CANVAS, HEADING_COMPACT_HEIGHT, f"{lead} {rest}", body)


def luminance(hex_colour: str) -> float:
    channels = [int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def blend(top: str, bottom: str, opacity: float) -> str:
    mixed = [
        round(int(top[i:i + 2], 16) * opacity + int(bottom[i:i + 2], 16) * (1 - opacity)) for i in (1, 3, 5)
    ]
    return "#" + "".join(f"{c:02x}" for c in mixed)


def contrast(a: str, b: str) -> float:
    high, low = sorted((luminance(a), luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def check_contrast() -> None:
    """Fails the build if a text role drops under WCAG AA (4.5:1) on its background."""
    for name, theme in THEMES.items():
        opacity = CONTAINER_OPACITY_DARK if name == "dark" else 1
        tile = blend(theme["container"], theme["page"], opacity)
        for background_name, background in (("page", theme["page"]), ("tile", tile)):
            for role in ("primary", "on_surface", "on_surface_variant"):
                ratio = contrast(theme[role], background)
                assert ratio >= 4.5, f"{name} {role} on {background_name}: {ratio:.2f}"
    # The smallest text must render at 12 px or more at the narrowest width of each layout.
    smallest = min(TYPE["body"]["size"], TYPE["label"]["size"])
    for layout, content_width in (("compact", PHONE_CONTENT_WIDTH), ("wide", SMALL_DESKTOP_CONTENT_WIDTH)):
        rendered = smallest * content_width / stats_width(layout)
        assert rendered >= 12, f"{layout} stat caption renders at {rendered:.1f} px"
    rendered = TYPE["title"]["size"] * PHONE_CONTENT_WIDTH / HEADING_COMPACT_CANVAS
    assert rendered >= 12, f"compact heading subtitle renders at {rendered:.1f} px"
    for tile in STAT_TILES:
        for line in [tile["eyebrow"], *tile["caption"]]:
            assert text_width(line, "body") <= TILE_WIDTH - 2 * TILE_PADDING, f"too wide: {line}"
    for lead, rest in SECTION_HEADINGS.values():
        assert text_width(f"{lead} {rest}", "headline") <= HEADING_WIDE_CANVAS, f"too wide: {lead}"
        assert text_width(lead, "headline") <= HEADING_COMPACT_CANVAS, f"too wide: {lead}"
        assert text_width(rest, "title") <= HEADING_COMPACT_CANVAS, f"too wide: {rest}"


def check_readme() -> None:
    """The README's media queries must use the same breakpoint as the layouts built here."""
    readme = (OUTPUT_DIR.parent.parent / "README.md").read_text(encoding="utf-8")
    assert f"(max-width: {COMPACT_BREAKPOINT}px)" in readme, "README breakpoint differs from COMPACT_BREAKPOINT"
    assert "(max-width: " not in readme.replace(f"(max-width: {COMPACT_BREAKPOINT}px)", ""), "mixed breakpoints"


def main() -> None:
    check_contrast()
    check_readme()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for theme_name, theme in THEMES.items():
        (OUTPUT_DIR / f"hero-{theme_name}.svg").write_text(hero_svg(theme), encoding="utf-8")
        for layout in ("wide", "compact"):
            suffix = "" if layout == "wide" else "-compact"
            (OUTPUT_DIR / f"stats{suffix}-{theme_name}.svg").write_text(
                stats_svg(theme_name, theme, layout), encoding="utf-8"
            )
            for key, (lead, rest) in SECTION_HEADINGS.items():
                (OUTPUT_DIR / f"heading-{key}{suffix}-{theme_name}.svg").write_text(
                    heading_svg(theme, lead, rest, layout), encoding="utf-8"
                )


if __name__ == "__main__":
    main()
