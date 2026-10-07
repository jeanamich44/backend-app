"""Titulaire : label + nom, rue, ville (texte live)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_titulaire:
        return
    fill(c, layout.LABEL_COLOR)
    draw_string(
        c, layout.LEFT_X, layout.LABEL_TITULAIRE_Y + dy,
        texts.LABEL_TITULAIRE, layout.LABEL_FONT, layout.LABEL_SIZE,
    )
    fill(c, layout.VALUE_COLOR)
    lines = (
        doc.card.titulaire_nom,
        doc.card.titulaire_rue,
        doc.card.titulaire_ville,
    )
    for y, text in zip(layout.TITULAIRE_YS, lines):
        if text:
            draw_string(
                c, layout.LEFT_X, y + dy, text,
                layout.VALUE_FONT, layout.VALUE_SIZE,
                max_width=layout.LEFT_W,
            )
