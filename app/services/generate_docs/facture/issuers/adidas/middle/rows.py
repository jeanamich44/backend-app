"""Lignes article (SKU / taille centrés, nom à gauche, prix à droite)."""

from .. import layout, rules
from ..paint import draw_center, draw_right, draw_string, fill


def draw(c, doc):
    if not doc.visible.middle_rows:
        return
    fill(c, layout.COLOR)
    sku_cx = (layout.CELL_ARTICLE[0] + layout.CELL_ARTICLE[1]) / 2
    size_cx = (layout.CELL_TAILLE[0] + layout.CELL_TAILLE[1]) / 2
    qty_cx = (layout.CELL_QTE[0] + layout.CELL_QTE[1]) / 2
    font = layout.FONT
    size = layout.SIZE_BODY
    for i, item in enumerate(doc.card.items[: layout.MAX_ROWS]):
        y = layout.ROW_Y0 + i * layout.ROW_PITCH
        qte, ht, ttc, _line_ht, line_ttc = rules.line_amounts(item)
        draw_center(c, sku_cx, y, item.sku, font, size, max_width=layout.CELL_ARTICLE[1] - layout.CELL_ARTICLE[0] - 4)
        draw_center(c, size_cx, y, item.taille, font, size, max_width=layout.CELL_TAILLE[1] - layout.CELL_TAILLE[0] - 4)
        draw_string(
            c, layout.ROW_NOM_X, y, item.nom, font, size,
            max_width=layout.ROW_NOM_MAX_W,
        )
        draw_center(c, qty_cx, y, rules.format_qty(qte), font, size)
        draw_right(c, layout.ROW_HT_RIGHT, y, rules.format_money(ht), font, size)
        draw_right(c, layout.ROW_TTC_RIGHT, y, rules.format_money(ttc), font, size)
        draw_right(c, layout.ROW_TOTAL_RIGHT, y, rules.format_money(line_ttc), font, size)
