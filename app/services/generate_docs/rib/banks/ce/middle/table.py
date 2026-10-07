"""Codes banque / guichet / compte / clé."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_table:
        return
    fill(c, layout.LABEL_COLOR)
    heads = (texts.COL_BANQUE, texts.COL_GUICHET, texts.COL_COMPTE, texts.COL_CLE)
    for x, label, max_w in zip(layout.TABLE_X, heads, layout.TABLE_W):
        draw_string(
            c, x, layout.TABLE_LABEL_Y + dy, label,
            layout.LABEL_FONT, layout.LABEL_SIZE, max_width=max_w,
        )
    fill(c, layout.VALUE_COLOR)
    vals = (doc.card.banque, doc.card.guichet, doc.card.compte, doc.card.cle)
    for x, value, max_w in zip(layout.TABLE_X, vals, layout.TABLE_W):
        if not value:
            continue
        draw_string(
            c, x, layout.TABLE_Y + dy, value,
            layout.VALUE_FONT, layout.VALUE_SIZE, max_width=max_w,
        )
