"""Nom d'agence dans la case Domiciliation (centré)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_centered, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_agence:
        return
    fill(c, layout.COLOR)
    draw_centered(
        c, layout.RIGHT_X0, layout.RIGHT_X1, layout.AGENCE_LABEL_Y + dy,
        texts.LABEL_AGENCE, layout.LABEL_FONT, layout.SIZE_LABEL,
    )
    if not doc.card.agence:
        return
    draw_centered(
        c, layout.RIGHT_X0, layout.RIGHT_X1, layout.AGENCE_Y + dy,
        doc.card.agence, layout.VALUE_FONT, layout.SIZE_VALUE,
        max_width=layout.RIGHT_X1 - layout.RIGHT_X0,
    )
