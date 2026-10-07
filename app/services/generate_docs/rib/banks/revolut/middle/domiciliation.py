"""Domiciliation : label 2 Tr + 3 lignes fill-only."""

from .. import copy as texts
from .. import layout
from ..paint import draw_label, draw_value


def draw(c, doc, dy=0):
    if not doc.visible.middle_domiciliation:
        return
    draw_label(
        c, layout.DOM_LABEL_X, layout.DOM_LABEL_Y + dy,
        texts.LABEL_DOM, layout.FONT, layout.LABEL_SIZE,
    )
    lines = (
        doc.card.domiciliation_nom,
        doc.card.domiciliation_rue,
        doc.card.domiciliation_pays,
    )
    for y, text in zip(layout.DOM_YS, lines):
        if text:
            draw_value(
                c, layout.DOM_X, y + dy, text,
                layout.FONT, layout.FIELD_SIZE,
                max_width=layout.DOM_W,
            )
