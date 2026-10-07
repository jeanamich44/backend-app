"""Titulaire : label 2 Tr + nom, rue, CP, ville, département fill-only."""

from .. import copy as texts
from .. import layout
from ..paint import draw_label, draw_value


def draw(c, doc, dy=0):
    if not doc.visible.middle_titulaire:
        return
    draw_label(
        c, layout.TITULAIRE_LABEL_X, layout.TITULAIRE_LABEL_Y + dy,
        texts.LABEL_TITULAIRE, layout.FONT, layout.LABEL_SIZE,
    )
    card = doc.card
    lines = (
        card.titulaire_nom,
        card.titulaire_rue,
        card.titulaire_cp,
        card.titulaire_ville,
    )
    for y, text in zip(layout.TITULAIRE_YS, lines):
        if text:
            draw_value(
                c, layout.TITULAIRE_X, y + dy, text,
                layout.FONT, layout.FIELD_SIZE,
                max_width=layout.TITULAIRE_W,
            )
    if card.titulaire_dept:
        draw_value(
            c, layout.TITULAIRE_DEPT_X, layout.TITULAIRE_DEPT_Y + dy,
            card.titulaire_dept, layout.FONT, layout.FIELD_SIZE,
            max_width=layout.TITULAIRE_W,
        )
