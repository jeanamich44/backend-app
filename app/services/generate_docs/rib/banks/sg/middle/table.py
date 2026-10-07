"""Codes Banque / Guichet / Compte / Clé RIB + label RIB."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_table:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.LABEL_X, layout.RIB_LABEL_Y + dy, texts.LABEL_RIB,
        layout.FONT_BOLD, layout.SIZE_LABEL,
    )
    heads = (texts.COL_BANQUE, texts.COL_GUICHET, texts.COL_COMPTE, texts.COL_CLE)
    vals = (doc.card.banque, doc.card.guichet, doc.card.compte, doc.card.cle)
    for x, label, value in zip(layout.TABLE_XS, heads, vals):
        draw_string(
            c, x, layout.TABLE_LABEL_Y + dy, label,
            layout.FONT_BOLD, layout.SIZE_VALUE,
            max_width=layout.TABLE_COL_W,
        )
        if value:
            draw_string(
                c, x, layout.TABLE_VALUE_Y + dy, value,
                layout.FONT, layout.SIZE_VALUE,
                max_width=layout.TABLE_COL_W,
            )
