"""Domiciliation / Paying Bank : 2 lignes sous le label."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_domiciliation:
        return
    fill(c, layout.LABEL_COLOR)
    draw_string(
        c, layout.DOM_X, layout.TABLE_LABEL_Y + dy,
        texts.LABEL_DOM, layout.LABEL_FONT, layout.LABEL_SIZE,
        max_width=layout.DOM_W,
    )
    fill(c, layout.VALUE_COLOR)
    rows = (doc.card.domiciliation_rue, doc.card.domiciliation_ville)
    for i, value in enumerate(rows):
        if not value:
            continue
        draw_string(
            c, layout.DOM_X,
            layout.DOM_Y + i * layout.DOM_LEADING + dy,
            value, layout.VALUE_FONT, layout.VALUE_SIZE,
            max_width=layout.DOM_W,
        )
