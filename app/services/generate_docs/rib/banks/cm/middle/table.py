"""Codes banque / guichet / compte / clé / devise, centrés dans les colonnes."""

from .. import copy as texts
from .. import layout
from ..paint import draw_centered, draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_table:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.RIB_HEAD_X, layout.RIB_HEAD_Y + dy, texts.LABEL_RIB,
        layout.LABEL_FONT, layout.SIZE_LABEL, max_width=layout.RIB_HEAD_W,
    )
    heads = (
        texts.COL_BANQUE, texts.COL_GUICHET, texts.COL_COMPTE,
        texts.COL_CLE, texts.COL_DEVISE,
    )
    vals = (
        doc.card.banque, doc.card.guichet, doc.card.compte,
        doc.card.cle, doc.card.devise,
    )
    for (x0, x1), label, value in zip(layout.TABLE_COLS, heads, vals):
        draw_centered(
            c, x0, x1, layout.TABLE_LABEL_Y + dy, label,
            layout.LABEL_FONT, layout.SIZE_LABEL,
        )
        if value:
            draw_centered(
                c, x0, x1, layout.TABLE_Y + dy, value,
                layout.VALUE_FONT, layout.SIZE_VALUE,
            )
