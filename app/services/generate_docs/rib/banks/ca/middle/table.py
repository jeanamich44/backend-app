"""Codes banque / guichet / compte / clé : labels gras, valeurs SemiBold, à gauche."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_table:
        return
    fill(c, layout.COLOR)
    heads = (texts.COL_BANQUE, texts.COL_GUICHET, texts.COL_COMPTE, texts.COL_CLE)
    for x, label, max_w in zip(layout.TABLE_X, heads, layout.TABLE_W):
        draw_string(
            c, x, layout.TABLE_HEAD_Y + dy, label,
            layout.FONT_BOLD, layout.SIZE, max_width=max_w,
        )
    card = doc.card
    vals = (card.banque, card.guichet, card.compte, card.cle)
    for x, value, max_w in zip(layout.TABLE_X, vals, layout.TABLE_W):
        if not value:
            continue
        draw_string(
            c, x, layout.TABLE_VAL_Y + dy, value,
            layout.FONT, layout.SIZE, max_width=max_w,
        )
