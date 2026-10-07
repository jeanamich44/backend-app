"""Lignes article : description, note, ASIN, montants."""

from .. import flow, layout, rules
from ..paint import draw_right, draw_string, fill, fill_rect


def _fill_row(c, y0, y1):
    xs = layout.CELL_X
    for i in range(len(xs) - 1):
        fill_rect(c, xs[i], y0, xs[i + 1], y1, layout.COLOR_ROW)


def draw(c, doc, plan):
    y0 = plan.band_y0
    if not plan.items:
        return y0
    if not doc.visible.middle_rows:
        for item in plan.items:
            y0 += flow.item_height(item)
        return y0
    uni = layout.FONT_UNI
    small = layout.SIZE_SMALL
    rate = rules.tva_label(doc.card)
    for item in plan.items:
        lines = flow.item_content(item)
        height = flow.item_height(item)
        y1 = y0 + height
        _fill_row(c, y0, y1)
        first = y0 + layout.ITEM_PAD_TOP
        y = first
        fill(c, layout.COLOR)
        qte, ht, ttc, _line_ht, line_ttc = rules.line_amounts(item)
        draw_string(c, layout.QTE_X, first, rules.format_qty(qte), uni, small)
        draw_right(c, layout.HT_RIGHT, first, rules.format_money_eur(ht), uni, small)
        draw_string(c, layout.TVA_X, first, rate, uni, small)
        draw_right(c, layout.TTC_RIGHT, first, rules.format_money_eur(ttc), uni, small)
        draw_right(c, layout.LINE_RIGHT, first, rules.format_money_eur(line_ttc), uni, small)
        for text, kind in lines:
            color = layout.COLOR_ASIN if kind in ("note", "asin") else layout.COLOR
            fill(c, color)
            draw_string(
                c, layout.DESC_X, y, text, uni, small,
                max_width=layout.DESC_MAX_W, color=color,
            )
            y += layout.DESC_PITCH
        y0 = y1
    return y0
