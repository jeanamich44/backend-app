"""Lignes article + COLLECT AT STORE si retrait magasin."""

from .. import copy as texts
from .. import layout, rules
from ..paint import draw_right, draw_string, fill


def draw(c, doc):
    if not doc.visible.middle_rows:
        return
    items = list(doc.card.items or ())[: layout.MAX_ROWS]
    fill(c, layout.COLOR)
    font = layout.FONT
    size = layout.SIZE_BODY
    last_y = layout.ITEM_Y0
    for i, item in enumerate(items):
        y = layout.ITEM_Y0 + i * layout.ROW_PITCH
        last_y = y
        qte, pu, _line = rules.line_cost(item)
        draw_string(c, layout.ITEM_NUM_X, y, str(i + 1), font, size)
        draw_string(
            c, layout.SKU_X, y, item.sku, font, size,
            max_width=layout.SKU_MAX_W,
        )
        draw_string(
            c, layout.BARCODE_X, y, item.barcode, font, size,
            max_width=layout.BARCODE_MAX_W,
        )
        draw_string(
            c, layout.DESC_X, y, item.desc, font, size,
            max_width=layout.DESC_MAX_W,
        )
        draw_string(
            c, layout.DESC_X, y + layout.LINE_PITCH, item.desc2, font, size,
            max_width=layout.DESC_MAX_W,
        )
        draw_string(
            c, layout.SIZE_X, y, item.taille, font, size,
            max_width=layout.SIZE_MAX_W,
        )
        draw_string(
            c, layout.COLOR_X, y, item.couleur, font, size,
            max_width=layout.COLOR_MAX_W,
        )
        draw_string(c, layout.QTY_X, y, rules.format_qty(qte), font, size)
        draw_right(c, layout.PRICE_RIGHT, y, rules.format_money(pu), font, size)
    if rules.retrait_magasin(doc.card):
        ty = last_y + layout.COLLECT_TEXT_DY
        vy = last_y + layout.COLLECT_VAL_DY
        draw_string(c, layout.DESC_X, ty, texts.COLLECT_ROW, font, size)
        draw_string(c, layout.QTY_X, vy, "1", font, size)
        draw_right(c, layout.PRICE_RIGHT, vy, "0.00", font, size)
