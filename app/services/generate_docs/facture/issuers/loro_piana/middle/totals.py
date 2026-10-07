"""Total: N + Total final + TVA."""

from .. import copy as texts
from .. import layout, rules
from ..paint import draw_right, draw_string, fill


def draw(c, doc):
    if not doc.visible.middle_totals:
        return
    dy = layout.table_shift(doc.card)
    ttc = rules.items_total(doc.card.items)
    card_tot = getattr(doc.card, "total", None)
    if card_tot and str(card_tot).strip():
        parsed = rules.parse_money(card_tot)
        if parsed > 0:
            ttc = parsed
    rate = rules.parse_money(doc.card.tva_rate)
    vat = rules.vat_amount(ttc, rate)
    fill(c, layout.COLOR)
    count = rules.format_qty(rules.qty_total(doc.card.items))
    draw_string(
        c, layout.COUNT_X, layout.COUNT_Y + dy,
        texts.TOTAL_N + count, layout.FONT_BOLD, layout.SIZE_BODY,
    )
    draw_string(
        c, layout.FINAL_LABEL_X, layout.FINAL_Y + dy,
        texts.TOTAL_FINAL, layout.FONT_BOLD, layout.SIZE_BODY,
    )
    draw_right(
        c, layout.FINAL_RIGHT, layout.FINAL_Y + dy,
        rules.format_money(ttc), layout.FONT_BOLD, layout.SIZE_BODY,
    )
    draw_string(
        c, layout.TVA_LABEL_X, layout.TVA_Y + dy,
        texts.TVA, layout.FONT_BOLD, layout.SIZE_BODY,
    )
    draw_string(
        c, layout.TVA_RATE_X, layout.TVA_Y + dy,
        rules.format_pct(rate), layout.FONT, layout.SIZE_BODY,
    )
    draw_right(
        c, layout.TVA_BASE_RIGHT, layout.TVA_Y + dy,
        rules.format_money(ttc), layout.FONT, layout.SIZE_BODY,
    )
    draw_right(
        c, layout.TVA_AMT_RIGHT, layout.TVA_Y + dy,
        rules.format_money(vat), layout.FONT, layout.SIZE_BODY,
    )
