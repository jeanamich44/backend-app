"""Titre RELEVE D'IDENTITE BANCAIRE, centré dans le cadre."""

from .. import layout
from ..paint import draw_centered, fill


def draw(c, doc, dy=0):
    if not doc.visible.header_title:
        return
    text = doc.header.title
    if not text:
        return
    fill(c, layout.TITLE_COLOR)
    draw_centered(
        c, layout.TITLE_CX0, layout.TITLE_CX1, layout.TITLE_Y + dy, text,
        layout.TITLE_FONT, layout.TITLE_SIZE,
        max_width=layout.TITLE_CX1 - layout.TITLE_CX0,
    )
