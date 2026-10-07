"""Agence de domiciliation : label + 3 lignes, alignés à droite."""

from .. import copy as texts
from .. import layout
from ..paint import draw_right, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_agence:
        return
    fill(c, layout.COLOR)
    draw_right(
        c, layout.AGENCE_RIGHT, layout.AGENCE_LABEL_Y + dy, texts.LABEL_AGENCE,
        layout.FONT_BOLD, layout.SIZE_LABEL,
        max_width=layout.AGENCE_W,
    )
    lines = (
        doc.card.agence,
        doc.card.agence_rue,
        doc.card.agence_ville,
    )
    for y, text in zip(layout.AGENCE_YS, lines):
        if text:
            draw_right(
                c, layout.AGENCE_RIGHT, y + dy, text,
                layout.FONT, layout.SIZE_ADDR,
                max_width=layout.AGENCE_W,
            )
