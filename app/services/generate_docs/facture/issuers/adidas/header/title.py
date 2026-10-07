"""Titre Facture."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_title:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.TITLE_X, layout.TITLE_Y,
        texts.TITLE, layout.FONT_BOLD, layout.SIZE_TITLE,
    )
