"""N° commande, dates, collect-in-store."""

from .. import copy as texts
from .. import layout, rules
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_order:
        return
    card = doc.card
    fill(c, layout.COLOR)
    font = layout.FONT
    size = layout.SIZE_BODY
    x = layout.LEFT_X
    vx = layout.VALUE_X
    max_w = layout.VALUE_MAX_W
    draw_string(c, x, layout.NUM_LABEL_Y, texts.NUM_LABEL, font, size)
    draw_string(
        c, vx, layout.NUM_LABEL_Y, card.num_commande or "",
        font, size, max_width=max_w,
    )
    draw_string(c, x, layout.DATE_ORDER_Y, texts.DATE_ORDER_LABEL, font, size)
    draw_string(c, x, layout.DATE_ORDER_LINE2_Y, texts.DATE_ORDER_LABEL2, font, size)
    draw_string(
        c, vx, layout.DATE_ORDER_Y, card.date_commande or "",
        font, size, max_width=max_w,
    )
    draw_string(c, x, layout.DATE_SHIP_Y, texts.DATE_SHIP_LABEL, font, size)
    draw_string(
        c, vx, layout.DATE_SHIP_Y, card.date_expedition or "",
        font, size, max_width=max_w,
    )
    if rules.retrait_magasin(card):
        draw_string(c, x, layout.COLLECT_Y, texts.COLLECT, font, size)
