"""Texte d'usage FR/EN sous le titre (Ubuntu Light 7 pt, gris)."""

from .. import layout
from ..paint import draw_string, fill, wrap_lines


def draw(c, doc, dy=0):
    if not doc.visible.header_text:
        return
    text = doc.header.text
    if not text:
        return
    fill(c, layout.TEXT_COLOR)
    y = layout.TEXT_Y + dy
    for paragraph in text.split("\n"):
        paragraph = paragraph.strip()
        if not paragraph:
            y += layout.TEXT_LEADING
            continue
        lines = wrap_lines(
            paragraph, layout.TEXT_FONT, layout.TEXT_SIZE, layout.TEXT_W,
        )
        last = len(lines) - 1
        for i, line in enumerate(lines):
            draw_string(
                c, layout.TEXT_X, y, line,
                layout.TEXT_FONT, layout.TEXT_SIZE,
                max_width=layout.TEXT_W,
                justify_to=layout.TEXT_W if i < last else None,
            )
            y += layout.TEXT_LEADING
