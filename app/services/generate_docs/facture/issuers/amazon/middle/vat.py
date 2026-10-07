"""Récapitulatif Taux TVA / Total HT / TVA (page 1 ou page 2)."""

from .. import copy as texts
from .. import layout, rules
from ..paint import draw_right, draw_string, fill, fill_rect


def _fill_vat_row(c, y0, y1):
    xs = layout.VAT_COL_X
    for i in range(len(xs) - 1):
        fill_rect(c, xs[i], y0, xs[i + 1], y1, layout.COLOR_ROW)
        fill_rect(
            c, xs[i], y1 - layout.RULE_H, xs[i + 1], y1,
            layout.COLOR_RULE_LIGHT,
        )


def _head_rules(c, y):
    xs = layout.VAT_COL_X
    for i in range(len(xs) - 1):
        fill_rect(
            c, xs[i], y, xs[i + 1], y + layout.RULE_H,
            layout.COLOR_RULE_LIGHT,
        )


def draw(c, doc, plan, after):
    if not plan.vat or not doc.visible.middle_vat:
        return after
    if plan.kind == "full" or plan.items or plan.extras or plan.grand:
        header_y = after + layout.VAT_AFTER_GRAND
    else:
        header_y = layout.VAT_P2_Y
    rate_y = header_y + layout.VAT_RATE_DY
    total_y = rate_y + layout.VAT_TOTAL_DY
    _head_rules(c, header_y - layout.VAT_HEAD_RULE_DY)
    gray0 = rate_y - layout.ITEM_PAD_TOP
    gray1 = gray0 + layout.EXTRA_BAND_H
    _fill_vat_row(c, gray0, gray1)
    uni = layout.FONT_UNI
    small = layout.SIZE_SMALL
    fill(c, layout.COLOR)
    draw_string(c, layout.VAT_LABEL_TAUX_X, header_y, texts.VAT_TAUX, uni, small)
    draw_string(c, layout.VAT_LABEL_HT_X, header_y, texts.VAT_TOTAL_HT, uni, small)
    draw_string(c, layout.VAT_LABEL_TVA_X, header_y, texts.VAT_TVA, uni, small)
    ht = rules.recap_ht(doc.card)
    tva = rules.recap_tva(doc.card)
    draw_string(c, layout.VAT_RATE_X, rate_y, rules.tva_label(doc.card), uni, small)
    draw_right(c, layout.VAT_HT_RIGHT, rate_y, rules.format_money_eur(ht), uni, small)
    draw_right(c, layout.VAT_TVA_RIGHT, rate_y, rules.format_money_eur(tva), uni, small)
    draw_string(c, layout.VAT_TOTAL_X, total_y, texts.VAT_TOTAL, uni, small)
    draw_right(c, layout.VAT_HT_RIGHT, total_y, rules.format_money_eur(ht), uni, small)
    draw_right(c, layout.VAT_TVA_RIGHT, total_y, rules.format_money_eur(tva), uni, small)
    return total_y
