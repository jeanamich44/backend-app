"""Tableau bénéficiaire / IBAN / devise / institution / BIC."""

from .. import copy as texts
from .. import layout
from .. import rib
from ..paint import draw_right, draw_string, fill_rgb, stroke_line


def draw(c, doc):
    if not doc.visible.middle_table:
        return
    card = doc.card
    x = layout.LEFT_X
    fill_rgb(c, layout.COLOR)
    labels = (
        texts.LABEL_BENEF,
        texts.LABEL_IBAN,
        texts.LABEL_DEVISE,
        texts.LABEL_INSTITUTION,
        texts.LABEL_BIC,
    )
    values = (
        card.nom_societe,
        rib.compact(card.iban),
        card.devise,
        texts.INSTITUTION,
        rib.compact(card.bic),
    )
    for y, label, value in zip(layout.ROW_YS, labels, values):
        draw_string(c, x, y, label, layout.FONT, layout.SIZE_BODY)
        if value:
            draw_right(
                c, layout.RIGHT_X, y, value,
                layout.FONT_BOLD, layout.SIZE_BODY,
            )
    x0, x1 = layout.ROW_LINE_LEFT
    x2, x3 = layout.ROW_LINE_RIGHT
    for y in layout.ROW_LINE_YS:
        stroke_line(
            c, x0, x1, y, layout.ROW_LINE_W, layout.COLOR_LINE_TABLE, cap=2, join=2,
        )
        stroke_line(
            c, x2, x3, y, layout.ROW_LINE_W, layout.COLOR_LINE_TABLE, cap=2, join=2,
        )
