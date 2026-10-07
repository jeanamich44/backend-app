"""Mention PARTIE RESERVEE, alignée à droite."""

from .. import copy as texts
from .. import layout
from ..paint import draw_right, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_reserved:
        return
    fill(c, layout.COLOR)
    draw_right(
        c, layout.RESERVED_RIGHT_X, layout.RESERVED_Y + dy, texts.RESERVED,
        layout.LABEL_FONT, layout.SIZE_LABEL, max_width=layout.RIGHT_X1 - layout.NOTICE_X,
    )
