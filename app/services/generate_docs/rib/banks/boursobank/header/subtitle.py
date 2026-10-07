"""Sous-titre Compte bancaire (texte live, aligné à droite)."""

from .. import layout
from ..paint import draw_right, fill


def draw(c, doc, dy=0):
    if not doc.visible.header_subtitle:
        return
    text = doc.header.subtitle
    if not text:
        return
    fill(c, layout.SUBTITLE_COLOR)
    draw_right(
        c, layout.SUBTITLE_RIGHT_X, layout.SUBTITLE_Y + dy, text,
        layout.SUBTITLE_FONT, layout.SUBTITLE_SIZE,
        max_width=layout.SUBTITLE_W,
    )
