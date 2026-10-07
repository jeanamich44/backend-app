"""Frais d'expédition, remise, Facture Total."""

from .. import copy as texts
from .. import flow, layout, rules
from ..paint import draw_right, draw_string, fill, fill_rect


def _fill_row(c, y0, y1):
    xs = layout.CELL_X
    for i in range(len(xs) - 1):
        fill_rect(c, xs[i], y0, xs[i + 1], y1, layout.COLOR_ROW)


def _rules_after(c, y1):
    left, right = layout.RULE_X
    xs = layout.CELL_X
    fill_rect(c, left, y1, right, y1 + layout.RULE_H, layout.COLOR_RULE_LIGHT)
    for i in range(len(xs) - 1):
        fill_rect(
            c, xs[i], y1 - layout.RULE_H, xs[i + 1], y1,
            layout.COLOR_RULE_LIGHT,
        )


def _extra_line(c, y, label, ht, ttc):
    uni = layout.FONT_UNI
    small = layout.SIZE_SMALL
    fill(c, layout.COLOR)
    draw_string(c, layout.DESC_X, y, label, uni, small)
    draw_right(c, layout.HT_RIGHT, y, rules.format_money_eur(ht), uni, small)
    draw_right(c, layout.TTC_RIGHT, y, rules.format_money_eur(ttc), uni, small)
    draw_right(c, layout.LINE_RIGHT, y, rules.format_money_eur(ttc), uni, small)


def draw(c, doc, plan, bottom):
    if not plan.extras or not doc.visible.middle_totals:
        return bottom
    card = doc.card
    keys = flow.extra_keys(card)
    y = bottom + layout.EXTRA_GAP
    last_y = y
    rows = []
    for key in keys:
        if key == "expedition":
            rows.append((
                y, texts.LIVRAISON_LABEL,
                rules.parse_money(card.expedition_ht),
                rules.parse_money(card.expedition_ttc),
            ))
        else:
            rows.append((
                y, texts.REMISE_LABEL,
                rules.parse_money(card.remise_ht),
                rules.parse_money(card.remise_ttc),
            ))
        last_y = y
        y += layout.EXTRA_PITCH
    band0 = last_y - layout.ITEM_PAD_TOP
    band1 = band0 + layout.EXTRA_BAND_H
    _fill_row(c, band0, band1)
    _rules_after(c, band1)
    for origin, label, ht, ttc in rows:
        _extra_line(c, origin, label, ht, ttc)
    if not plan.grand:
        return last_y
    grand_y = last_y + layout.GRAND_DY
    fill(c, layout.COLOR)
    draw_string(
        c, layout.GRAND_LABEL_X, grand_y,
        texts.GRAND_LABEL, layout.FONT_UNI, layout.SIZE_GRAND,
    )
    draw_right(
        c, layout.GRAND_RIGHT, grand_y,
        (card.total or "").strip() or rules.format_money_eur(rules.grand_total(card)),
        layout.FONT_UNI, layout.SIZE_GRAND,
    )
    return grand_y
