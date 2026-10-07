"""Titulaire(s) : label outlined + nom."""

from .. import layout
from ..paint import draw_label, draw_string, fill


def draw(c, doc):
    if not doc.visible.middle_titulaire:
        return
    draw_label(c, layout.LABEL_TITULAIRE)
    text = doc.card.titulaire_nom
    if text:
        fill(c, layout.COLOR_TEXT)
        draw_string(
            c, layout.TITULAIRE_X, layout.TITULAIRE_Y, text,
            layout.FONT, layout.FONT_SIZE,
            max_width=layout.TITULAIRE_W,
        )
