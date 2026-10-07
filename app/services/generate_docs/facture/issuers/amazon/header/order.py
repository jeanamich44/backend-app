"""Bloc Informations de la commande (Y dynamique)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill, fill_rect


def draw(c, doc, plan):
    if not doc.visible.header_order:
        return
    card = doc.card
    header = plan.header
    fill(c, layout.COLOR)
    uni = layout.FONT_UNI
    small = layout.SIZE_SMALL
    draw_string(
        c, layout.ORDER_TITLE_X, header["order_title"],
        texts.ORDER_TITLE, uni, layout.SIZE_UNI_LG,
    )
    draw_string(
        c, layout.ORDER_LABEL_X, header["order_date"],
        texts.ORDER_DATE_LABEL, uni, small,
    )
    draw_string(
        c, layout.ORDER_DATE_X, header["order_date"],
        card.date_commande, uni, small,
    )
    draw_string(
        c, layout.ORDER_LABEL_X, header["order_num"],
        texts.ORDER_NUM_LABEL, uni, small,
    )
    draw_string(
        c, layout.ORDER_NUM_X, header["order_num"],
        card.num_commande, uni, small, max_width=200,
    )
    left, right = layout.RULE_X
    fill_rect(
        c, left, header["order_rule"], right,
        header["order_rule"] + layout.RULE_H, layout.COLOR_LINE,
    )
