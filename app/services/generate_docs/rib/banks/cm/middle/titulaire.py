"""Titulaire : label + 3 lignes (trou si une ligne est vide)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_titulaire:
        return
    card = doc.card
    fill(c, layout.COLOR)
    draw_string(
        c, layout.TITULAIRE_X, layout.TITULAIRE_LABEL_Y + dy,
        texts.LABEL_TITULAIRE, layout.VALUE_FONT, layout.SIZE_VALUE,
        max_width=layout.TITULAIRE_W,
    )
    rows = (card.titulaire_nom, card.titulaire_rue, card.titulaire_ville)
    for i, value in enumerate(rows):
        if not value:
            continue
        draw_string(
            c, layout.TITULAIRE_X,
            layout.TITULAIRE_Y + i * layout.TITULAIRE_LEADING + dy,
            value, layout.ADDR_FONT, layout.SIZE_LABEL,
            max_width=layout.TITULAIRE_W,
        )
