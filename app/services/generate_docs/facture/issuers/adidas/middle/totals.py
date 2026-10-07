"""Bandes D10–D11 + sous-total / montant / TVA / mention débit."""

from .. import copy as texts
from .. import layout, rules
from ..paint import draw_right, draw_string, fill, fill_rect


def draw(c, doc):
    if not doc.visible.middle_totals:
        return
    fill_rect(c, *layout.TOTAL_BAR_LEFT, layout.COLOR_GRAY)
    fill_rect(c, *layout.TOTAL_BAR_RIGHT, layout.COLOR_GRAY)

    sous, montant, tva = rules.invoice_totals(doc.card.items)
    card_tot = getattr(doc.card, "total", None)
    if card_tot and str(card_tot).strip():
        parsed = rules.parse_money(card_tot)
        if parsed > 0:
            sous = parsed
            montant = sous / (1.0 + layout.TVA_RATE / 100.0)
            tva = sous - montant

    fill(c, layout.COLOR)
    bold = layout.FONT_BOLD
    roman = layout.FONT
    sz = layout.SIZE_TOTAL
    x = layout.TOTAL_LABEL_X
    right = layout.TOTAL_VALUE_RIGHT

    draw_string(c, x, layout.TOTAL_SUB_Y, texts.SUBTOTAL, bold, sz)
    draw_right(c, right, layout.TOTAL_SUB_Y, rules.format_money(sous), roman, sz)

    draw_string(c, x, layout.TOTAL_AMOUNT_Y, texts.MONTANT, bold, sz)
    draw_right(c, right, layout.TOTAL_AMOUNT_VALUE_Y, rules.format_money(montant), roman, sz)

    tva_label = texts.TVA_PREFIX + rules.format_money(montant) + ")"
    draw_string(c, x, layout.TOTAL_TVA_Y, tva_label, roman, sz)
    draw_right(c, right, layout.TOTAL_TVA_Y, rules.format_money(tva), roman, sz)

    for y, line in zip(layout.NOTE_Y, texts.NOTE):
        draw_string(c, x, y, line, bold, sz)
