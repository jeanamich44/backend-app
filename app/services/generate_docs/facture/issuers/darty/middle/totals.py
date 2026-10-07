"""Total facturé / réglé / solde."""

from .. import copy as texts
from .. import layout, rules
from ..chrome import vectors
from ..paint import draw_right, draw_strokes, draw_string, fill, shift_strokes


def draw(c, doc):
    if not doc.visible.middle_totals:
        return
    dy = layout.table_shift(doc.card)
    draw_strokes(c, shift_strokes(vectors.TOTAL_STROKES, dy))
    ht, vat, ttc = rules.invoice_totals(doc.card.items)
    card_tot = getattr(doc.card, "total", None)
    if card_tot and str(card_tot).strip():
        parsed = rules.parse_money(card_tot)
        if parsed > 0:
            ttc = parsed
            ht = round(ttc / 1.20, 2)
            vat = round(ttc - ht, 2)
    fill(c, layout.COLOR)
    draw_string(
        c, layout.TRUST_X, layout.TRUST_Y + dy,
        texts.TRUST, layout.FONT, layout.SIZE_TRUST,
    )
    draw_string(
        c, layout.TOTAL_LABEL_X, layout.TOTAL_Y + dy,
        texts.TOTAL, layout.FONT_BOLD, layout.SIZE_TOTAL,
    )
    draw_right(
        c, layout.MONEY_HT_RIGHT, layout.TOTAL_Y + dy,
        rules.format_eur(ht), layout.FONT, layout.SIZE_TOTAL,
    )
    draw_right(
        c, layout.MONEY_TVA_RIGHT, layout.TOTAL_Y + dy,
        rules.format_eur(vat), layout.FONT, layout.SIZE_TOTAL,
    )
    draw_right(
        c, layout.MONEY_TTC_RIGHT, layout.TOTAL_Y + dy,
        rules.format_eur(ttc), layout.FONT, layout.SIZE_TOTAL,
    )
    draw_string(
        c, layout.PAY_LABEL_X, layout.PAY_Y + dy,
        texts.PAY, layout.FONT_BOLD, layout.SIZE_TOTAL,
    )
    draw_string(
        c, layout.PAY_VAL_X, layout.PAY_Y + dy,
        "    " + (doc.card.payment or ""),
        layout.FONT, layout.SIZE_TOTAL,
    )
    draw_right(
        c, layout.MONEY_TTC_RIGHT, layout.PAY_Y + dy,
        rules.format_eur(ttc), layout.FONT, layout.SIZE_TOTAL,
    )
    draw_string(
        c, layout.SOLDE_LABEL_X, layout.SOLDE_Y + dy,
        texts.SOLDE, layout.FONT_BOLD, layout.SIZE_TOTAL,
    )
    draw_right(
        c, layout.MONEY_TTC_RIGHT, layout.SOLDE_Y + dy,
        rules.format_eur(0, zero_plain=True),
        layout.FONT, layout.SIZE_TOTAL,
    )
