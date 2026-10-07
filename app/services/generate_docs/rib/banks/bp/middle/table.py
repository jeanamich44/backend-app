"""Tableau RIB : fonds gris + filets segmentés, en-têtes et valeurs centrés."""

from .. import copy as texts
from .. import layout
from ..paint import draw_centred, fill, fill_rect, stroke_line


def draw(c, doc, dy=0):
    if not doc.visible.middle_table:
        return
    for x0, y0, x1, y1 in layout.TABLE_FILLS:
        fill_rect(c, x0, y0 + dy, x1, y1 + dy, layout.TABLE_FILL)
    for x0, y0, x1, y1, width in layout.TABLE_LINES:
        stroke_line(
            c, x0, y0 + dy, x1, y1 + dy, width,
            layout.TABLE_STROKE, cap=layout.TABLE_CAP,
        )

    fill(c, layout.COLOR)
    heads = (texts.COL_BANQUE, texts.COL_GUICHET, texts.COL_COMPTE, texts.COL_CLE)
    for cx, label, max_w in zip(layout.TABLE_CX, heads, layout.TABLE_W):
        draw_centred(
            c, cx, layout.TABLE_HEAD_Y + dy, label,
            layout.FONT, layout.SIZE, max_width=max_w,
        )
    card = doc.card
    vals = (card.banque, card.guichet, card.compte, card.cle)
    for cx, value, max_w in zip(layout.TABLE_CX, vals, layout.TABLE_W):
        if value:
            draw_centred(
                c, cx, layout.TABLE_VAL_Y + dy, value,
                layout.FONT, layout.SIZE, max_width=max_w,
            )
