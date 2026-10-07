"""Titulaire : label Bold 10.5 + 3 lignes Regular 10.5."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_titulaire:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.LABEL_X, layout.TITULAIRE_LABEL_Y + dy, texts.LABEL_TITULAIRE,
        layout.FONT_BOLD, layout.SIZE_LABEL,
    )
    lines = (
        doc.card.titulaire_nom,
        doc.card.titulaire_rue,
        doc.card.titulaire_ville,
    )
    for y, text in zip(layout.TITULAIRE_YS, lines):
        if text:
            draw_string(
                c, layout.TITULAIRE_X, y + dy, text,
                layout.FONT, layout.SIZE_ADDR,
                max_width=layout.TITULAIRE_W,
            )
