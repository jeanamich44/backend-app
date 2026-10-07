"""Domiciliation Okali, une ligne."""

from .. import copy as texts
from .. import layout
from ..paint import draw_label, draw_value, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_domiciliation:
        return
    fill(c, layout.LABEL_COLOR)
    draw_label(
        c, layout.FIELD_X, layout.DOM_Y + dy, texts.LABEL_DOM,
        layout.FONT, layout.SIZE_FIELD,
    )
    if not doc.card.domiciliation:
        return
    draw_value(
        c, layout.DOM_VALUE_X, layout.DOM_Y + dy, doc.card.domiciliation,
        layout.FONT, layout.SIZE_FIELD, max_width=layout.DOM_W,
    )
