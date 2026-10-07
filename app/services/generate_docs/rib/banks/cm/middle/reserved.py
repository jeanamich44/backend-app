"""Mention PARTIE RESERVEE, origin à gauche (gabarit iText)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_reserved:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.RESERVED_X, layout.RESERVED_Y + dy, texts.RESERVED,
        layout.LABEL_FONT, layout.SIZE_LABEL,
        max_width=layout.BOX_X1 - layout.RESERVED_X,
    )
