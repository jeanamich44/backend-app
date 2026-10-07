"""Sous-total, taxe, total + D11 / D12 / D9."""

from .. import copy as texts
from .. import layout, rules
from ..paint import draw_right, draw_string, fill, fill_subpaths, stroke_line
from . import vectors


def draw(c, doc):
    if not doc.visible.middle_totals:
        return
    extra = layout.table_shift(len(doc.card.items or ()))
    sous, rate, tax, total = rules.invoice_totals(doc.card.items, doc.card.tva)
    card_tot = getattr(doc.card, "total", None)
    if card_tot and str(card_tot).strip():
        parsed = rules.parse_money(card_tot)
        if parsed > 0:
            total = parsed
            sous = round(total / (1.0 + rate / 100.0), 2)
            tax = round(total - sous, 2)
    fill(c, layout.COLOR)
    font = layout.FONT
    size = layout.SIZE_ROW
    draw_string(
        c, layout.COL_TEXT_X[2], layout.SUB_Y + extra, texts.SUBTOTAL,
        font, size,
    )
    draw_right(
        c, layout.COST_RIGHT, layout.SUB_AMT_Y + extra, rules.format_euro(sous),
        font, size,
    )
    fill_subpaths(c, vectors.THICK, vectors.COLOR_THICK, dy=extra)
    draw_string(
        c, layout.COL_TEXT_X[1], layout.TAX_LABEL_Y + extra, texts.TAX,
        font, size,
    )
    draw_right(
        c, layout.TAX_PCT_RIGHT, layout.TAX_VAL_Y + extra, rules.format_pct(rate),
        font, size,
    )
    draw_right(
        c, layout.COST_RIGHT, layout.TAX_VAL_Y + extra, rules.format_euro(tax),
        font, size,
    )
    (x0, y0), (x1, y1) = vectors.TAX_LINE
    stroke_line(c, x0, y0 + extra, x1, y1 + extra, layout.TABLE_RULE_W, layout.COLOR, cap=0)
    draw_string(
        c, layout.COL_TEXT_X[2], layout.TOTAL_LABEL_Y + extra, texts.TOTAL,
        font, size,
    )
    draw_right(
        c, layout.COST_RIGHT, layout.TOTAL_AMT_Y + extra, rules.format_euro(total),
        font, size,
    )
    (x0, y0), (x1, y1) = vectors.BOT_LINE
    stroke_line(c, x0, y0 + extra, x1, y1 + extra, layout.TABLE_RULE_W, layout.COLOR, cap=0)
