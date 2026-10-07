"""Barre Total + frais de port."""

from .. import copy as texts
from .. import layout, rules
from ..paint import draw_right, draw_string, fill, fill_rect


def draw(c, doc):
    if not doc.visible.middle_totals:
        return
    card = doc.card
    dy = layout.table_shift(card)
    for x0, y0, x1, y1, color in layout.shifted_fills(layout.TOTAL_FILLS, dy):
        fill_rect(c, x0, y0, x1, y1, color)
    fill(c, layout.COLOR_WHITE)
    draw_string(
        c, layout.TOTAL_LABEL_X, layout.TOTAL_LABEL_Y + dy,
        texts.TOTAL, layout.FONT_BOLD, layout.SIZE_TOTAL,
    )
    tot_val = rules.items_total(card.items)
    card_tot = getattr(card, "total", None)
    if card_tot and str(card_tot).strip():
        parsed = rules.parse_money(card_tot)
        if parsed > 0:
            tot_val = parsed
    draw_right(
        c, layout.TOTAL_AMT_RIGHT, layout.TOTAL_AMT_Y + dy,
        rules.format_eur(tot_val),
        layout.FONT_BOLD, layout.SIZE_TOTAL_AMT,
    )
    fill(c, layout.COLOR_COL)
    draw_string(
        c, layout.PORT_LABEL_X, layout.PORT_LABEL_Y + dy,
        texts.PORT, layout.FONT, layout.SIZE_PORT,
    )
    fill(c, layout.COLOR_BLACK)
    draw_right(
        c, layout.PORT_RIGHT, layout.PORT_AMT_Y + dy,
        rules.format_eur(rules.parse_money(card.port)),
        layout.FONT, layout.SIZE_ROW,
    )
