"""Lignes article (1 calée gabarit, jusqu’à 3)."""

from .. import layout, rules
from ..paint import draw_center, draw_right, draw_string, fill


def draw(c, doc):
    if not doc.visible.middle_rows:
        return
    items = list(doc.card.items or ())[: layout.MAX_ROWS]
    fill(c, layout.COLOR_BLACK)
    for i, item in enumerate(items):
        y = layout.row_y(i)
        if item.desc:
            draw_string(
                c, layout.ROW_DESC_X, y,
                item.desc, layout.FONT, layout.SIZE_ROW,
                max_width=layout.ROW_DESC_MAX_W,
            )
        if item.qte:
            draw_center(
                c, layout.QTY_CX, y,
                item.qte, layout.FONT, layout.SIZE_ROW,
            )
        if item.montant:
            draw_right(
                c, layout.MNT_RIGHT, y,
                rules.format_eur(rules.parse_money(item.montant)),
                layout.FONT, layout.SIZE_ROW,
            )
