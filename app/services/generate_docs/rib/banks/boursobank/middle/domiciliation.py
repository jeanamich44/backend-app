"""Domiciliation banque : label + 3 lignes (texte live, casse mixte)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_domiciliation:
        return
    fill(c, layout.LABEL_COLOR)
    draw_string(
        c, layout.LEFT_X, layout.LABEL_DOM_Y + dy,
        texts.LABEL_DOM, layout.LABEL_FONT, layout.LABEL_SIZE,
    )
    fill(c, layout.VALUE_COLOR)
    lines = (
        doc.card.domiciliation_nom,
        doc.card.domiciliation_rue,
        doc.card.domiciliation_ville,
    )
    for y, text in zip(layout.DOM_YS, lines):
        if text:
            draw_string(
                c, layout.LEFT_X, y + dy, text,
                layout.VALUE_FONT, layout.VALUE_SIZE,
                max_width=layout.LEFT_W,
            )
