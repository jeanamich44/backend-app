"""Lignes article : description, quantité, prix, coût + D10."""

from .. import layout, rules
from ..paint import draw_right, draw_string, fill, stroke_line
from . import vectors


def draw(c, doc):
    if not doc.visible.middle_rows:
        return
    items = list(doc.card.items or ())[: layout.MAX_ROWS]
    fill(c, layout.COLOR)
    font = layout.FONT
    size = layout.SIZE_ROW
    for i, item in enumerate(items):
        y = layout.ITEM_Y + i * layout.ROW_H
        qte, pu, cost = rules.line_cost(item)
        draw_string(
            c, layout.COL_TEXT_X[0], y, item.desc or "",
            font, size, max_width=layout.DESC_MAX_W,
        )
        if item.qte:
            draw_right(c, layout.QTY_RIGHT, y, rules.format_qty(qte), font, size)
        if item.pu:
            draw_right(c, layout.PRICE_RIGHT, y, rules.format_euro(pu), font, size)
        if item.qte or item.pu:
            draw_right(c, layout.COST_RIGHT, y, rules.format_euro(cost), font, size)
    n = max(1, len(items))
    shift = (n - 1) * layout.ROW_H
    (x0, y0), (x1, y1) = vectors.ITEM_LINE
    stroke_line(c, x0, y0 + shift, x1, y1 + shift, layout.TABLE_RULE_W, layout.COLOR, cap=0)
