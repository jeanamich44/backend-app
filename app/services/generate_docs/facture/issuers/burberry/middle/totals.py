"""PRIX TOTAL — montant calculé, pas celui du gabarit."""

from .. import copy as texts
from .. import layout, rules
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.middle_totals:
        return
    fill(c, layout.COLOR)
    total = rules.invoice_total(doc.card.items)
    card_tot = getattr(doc.card, "total", None)
    if card_tot and str(card_tot).strip():
        parsed = rules.parse_money(card_tot)
        if parsed > 0:
            total = parsed
    draw_string(
        c, layout.TOTAL_AMT_X, layout.TOTAL_AMT_Y,
        rules.format_total(total), layout.FONT_BOLD, layout.SIZE_BODY,
    )
    draw_string(
        c, layout.TOTAL_LABEL_X, layout.TOTAL_LABEL_Y,
        texts.TOTAL_LABEL, layout.FONT_BOLD, layout.SIZE_BODY,
    )
