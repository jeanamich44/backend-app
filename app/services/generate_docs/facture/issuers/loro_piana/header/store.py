"""Adresse boutique + tel / mail (chrome gabarit, italique)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_store:
        return
    fill(c, layout.COLOR)
    for x, y, line in zip(layout.STORE_X, layout.STORE_Y, texts.STORE):
        draw_string(c, x, y, line, layout.FONT_ITALIC, layout.SIZE_STORE)
