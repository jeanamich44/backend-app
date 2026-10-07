"""Titre RIB · Relevé d'Identité Bancaire (2 Tr)."""

from .. import layout
from ..paint import draw_label


def draw(c, doc, dy=0):
    if not doc.visible.header_title:
        return
    text = doc.header.title
    if not text:
        return
    draw_label(
        c, layout.TITLE_X, layout.TITLE_Y + dy, text,
        layout.FONT, layout.TITLE_SIZE,
        max_width=layout.TITLE_W,
    )
