"""Nom et adresse du titulaire (5 lignes max, optionnelles compactées)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_titulaire:
        return
    fill(c, layout.BRAND_TITLE_COLOR)
    draw_string(
        c, layout.TITULAIRE_TITLE_X, layout.TITULAIRE_TITLE_Y + dy,
        texts.TITULAIRE_TITLE, layout.TABLE_VAL_FONT, layout.TITULAIRE_TITLE_SIZE,
    )
    fill(c, layout.LINE_BLACK)
    for i, line in enumerate(doc.card.titulaire_lines()):
        draw_string(
            c, layout.TITULAIRE_X, layout.TITULAIRE_YS[i] + dy,
            line, layout.TABLE_VAL_FONT, layout.TITULAIRE_SIZE,
            max_width=layout.TITULAIRE_W,
        )
