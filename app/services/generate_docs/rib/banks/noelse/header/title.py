"""Titre IBAN 15 pt Light, dans la découpe du cadre."""

from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, i=0):
    if not doc.visible.header_title:
        return
    text = doc.header.title
    if not text:
        return
    x, y = layout.TITLE_POS[i]
    fill(c, layout.COLOR)
    draw_string(
        c, x, y, text, layout.FONT, layout.SIZE_TITLE,
        max_width=layout.TITLE_W,
    )
