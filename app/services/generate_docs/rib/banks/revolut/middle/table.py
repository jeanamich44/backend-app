"""Tableau RIB : 4 colonnes, labels 2 Tr, valeurs fill-only."""

from .. import copy as texts
from .. import layout
from ..paint import draw_label, draw_value


def draw(c, doc, dy=0):
    if not doc.visible.middle_table:
        return
    heads = (
        texts.COL_BANQUE,
        texts.COL_AGENCE,
        texts.COL_COMPTE,
        texts.COL_CLE,
    )
    for x, label in zip(layout.TABLE_HEAD_XS, heads):
        draw_label(
            c, x, layout.TABLE_HEAD_Y + dy, label,
            layout.FONT, layout.FIELD_SIZE,
        )
    vals = (
        doc.card.banque,
        doc.card.guichet,
        doc.card.compte,
        doc.card.cle,
    )
    for x, value, max_w in zip(layout.TABLE_VAL_XS, vals, layout.TABLE_W):
        if value:
            draw_value(
                c, x, layout.TABLE_VAL_Y + dy, value,
                layout.FONT, layout.FIELD_SIZE,
                max_width=max_w,
            )
