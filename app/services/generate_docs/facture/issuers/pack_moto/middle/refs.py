"""Table refs : n° facture, dates, commande."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill, fill_rect, stroke_rect
from . import vectors


def draw(c, doc):
    if not doc.visible.middle_refs:
        return
    stroke_rect(c, *vectors.REF_OUTER, layout.STROKE_W, layout.COLOR, cap=layout.STROKE_CAP)
    for rect in vectors.REF_VAL_FILLS:
        fill_rect(c, *rect, (1, 1, 1))
    for rect in vectors.REF_HEAD_FILLS:
        fill_rect(c, *rect, layout.COLOR_CELL)
    fill(c, layout.COLOR)
    for x, label in zip(layout.REF_LABEL_X, texts.REF_LABELS):
        draw_string(
            c, x, layout.REF_LABEL_Y, label,
            layout.FONT_BOLD, layout.SIZE_BODY,
            max_width=layout.REF_MAX_W,
        )
    card = doc.card
    values = (
        card.num_facture or "",
        card.date_facture or "",
        card.num_commande or "",
        card.date_commande or "",
    )
    for x, value in zip(layout.REF_VALUE_X, values):
        draw_string(
            c, x, layout.REF_VALUE_Y, value,
            layout.FONT, layout.SIZE_REF_VAL,
            max_width=layout.REF_MAX_W,
        )
