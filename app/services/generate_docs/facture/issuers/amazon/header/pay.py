"""Encadré Payé : référence, vendeur, TVA, date, n° facture, total."""

from .. import copy as texts
from .. import layout, rules
from ..paint import draw_string, fill, width


def draw(c, doc):
    if not doc.visible.header_pay:
        return
    card = doc.card
    uni = layout.FONT_UNI
    small = layout.SIZE_SMALL
    fill(c, layout.COLOR)
    draw_string(
        c, layout.PAY_TITLE_X, layout.PAY_TITLE_Y,
        texts.PAYE, uni, layout.SIZE_PAY,
    )
    y_ref, y_sold, y_tva = layout.PAY_Y
    draw_string(
        c, layout.PAY_X, y_ref,
        texts.PAY_REF_PREFIX + (card.payment_ref or ""),
        uni, small, max_width=210,
    )
    draw_string(
        c, layout.PAY_X, y_sold,
        texts.PAY_SOLD_PREFIX + (card.seller_nom or ""),
        uni, small, max_width=210,
    )
    tva = (card.seller_tva or "").strip()
    if tva:
        draw_string(
            c, layout.PAY_X, y_tva,
            texts.PAY_TVA_PREFIX + tva,
            uni, small, max_width=210,
        )
    draw_string(
        c, layout.PAY_LABEL_X, layout.PAY_DATE_Y,
        texts.PAY_DATE, uni, small,
    )
    draw_string(
        c, layout.PAY_VALUE_X, layout.PAY_DATE_Y,
        card.date_facture, uni, small,
    )
    draw_string(
        c, layout.PAY_LABEL_X, layout.PAY_INV_Y,
        texts.PAY_INV, uni, small,
    )
    inv_num = card.num_facture or ""
    inv_w = width(inv_num, uni, small)
    inv_x = min(layout.PAY_VALUE_X, layout.PAY_RULE[1] - inv_w)
    draw_string(
        c, inv_x, layout.PAY_INV_Y,
        inv_num, uni, small, max_width=140,
    )
    draw_string(
        c, layout.PAY_LABEL_X, layout.PAY_TOTAL_Y,
        texts.PAY_TOTAL, uni, small,
    )
    draw_string(
        c, layout.PAY_VALUE_X, layout.PAY_TOTAL_Y,
        rules.format_money_eur(rules.grand_total(card)),
        uni, small,
    )
