"""Lignes article (1 calée gabarit, extra = même pitch que le filet)."""

from .. import layout, rules
from ..paint import draw_right, draw_string, fill


def draw(c, doc):
    if not doc.visible.middle_rows:
        return
    items = list(doc.card.items or ())[: layout.MAX_ROWS]
    fill(c, layout.COLOR)
    for i, item in enumerate(items):
        y = layout.row_at(layout.ROW_Y, i)
        if item.sku:
            draw_string(
                c, layout.ROW_SKU_X, y, item.sku,
                layout.FONT, layout.SIZE_BODY, max_width=layout.SKU_MAX_W,
            )
        if item.desc:
            draw_string(
                c, layout.ROW_DESC_X, y, item.desc,
                layout.FONT, layout.SIZE_BODY, max_width=layout.DESC_MAX_W,
            )
        if item.qte:
            draw_right(
                c, layout.QTY_RIGHT, y, item.qte,
                layout.FONT_BOLD, layout.SIZE_BODY,
            )
        if item.prix:
            unit = rules.parse_money(item.prix)
            draw_right(
                c, layout.PRIX_RIGHT, y, rules.format_euro(unit),
                layout.FONT_BOLD, layout.SIZE_BODY,
            )
            draw_right(
                c, layout.ROW_TOTAL_RIGHT, y,
                rules.format_euro(rules.line_total(item)),
                layout.FONT_BOLD, layout.SIZE_BODY,
            )
