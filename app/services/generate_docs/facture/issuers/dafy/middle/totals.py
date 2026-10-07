from .. import copy as texts
from .. import layout, rules
from ..paint import draw_right, draw_string, fill, fill_ops
from . import vectors


def draw(c, doc):
    if not doc.visible.middle_totals:
        return
    extra = layout.middle_shift(doc.card)
    ht, ttc, remise, port, due, dont = rules.invoice_totals(doc.card)
    card_tot = getattr(doc.card, "total", None)
    if card_tot and str(card_tot).strip():
        parsed = rules.parse_money(card_tot)
        if parsed > 0 and abs(parsed - due) > 0.01:
            due = parsed
            ttc = round(due + remise - port, 2)
            ht = round(ttc / 1.20, 2)
            dont = round(ttc - ht, 2)
    for ops in vectors.TOTAL_OPS:
        fill_ops(c, ops, layout.COLOR_GRAY, dy=extra)
    fill(c, layout.COLOR)
    size = layout.SIZE_BODY
    y_ht, y_ttc, y_rem, y_port, y_due, y_tva = (
        y + extra for y in layout.TOTAL_Y
    )
    draw_string(
        c, layout.TOTAL_LABEL_X, y_ht, texts.TOTAL_HT,
        layout.FONT_BOLD, size,
    )
    draw_right(
        c, layout.TOTAL_RIGHT, y_ht,
        rules.format_total_amount(ht, bold=True),
        layout.FONT_BOLD, size,
    )
    draw_string(
        c, layout.TOTAL_LABEL_X, y_ttc, texts.TOTAL_TTC,
        layout.FONT, size,
    )
    draw_right(
        c, layout.TOTAL_RIGHT, y_ttc,
        rules.format_total_amount(ttc),
        layout.FONT, size,
    )
    draw_string(
        c, layout.TOTAL_LABEL_X, y_rem, texts.TOTAL_REMISE,
        layout.FONT, size,
    )
    draw_right(
        c, layout.TOTAL_RIGHT, y_rem,
        rules.format_total_amount(remise),
        layout.FONT, size,
    )
    draw_string(
        c, layout.TOTAL_LABEL_X, y_port, texts.TOTAL_PORT,
        layout.FONT, size,
    )
    draw_right(
        c, layout.TOTAL_RIGHT, y_port,
        rules.format_total_amount(port),
        layout.FONT, size,
    )
    draw_string(
        c, layout.TOTAL_PAY_X, y_due, texts.TOTAL_DUE,
        layout.FONT_BOLD, size,
    )
    draw_right(
        c, layout.TOTAL_PAY_RIGHT, y_due,
        rules.format_total_amount(due, bold=True),
        layout.FONT_BOLD, size,
    )
    draw_string(
        c, layout.TOTAL_PAY_X, y_tva, texts.TOTAL_TVA,
        layout.FONT_BOLD, size,
    )
    draw_right(
        c, layout.TOTAL_PAY_RIGHT, y_tva,
        rules.format_total_amount(dont, bold=True),
        layout.FONT_BOLD, size,
    )
