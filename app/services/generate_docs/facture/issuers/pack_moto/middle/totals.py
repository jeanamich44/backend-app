"""Recap montants à droite, décalé si extra articles."""

from .. import copy as texts
from .. import layout, rules
from ..paint import draw_string, fill, fill_rect, stroke_rect
from . import vectors


def draw(c, doc):
    if not doc.visible.middle_totals:
        return
    extra = layout.extra_y(doc.card)
    products, ship, ht, vat, ttc = rules.invoice_totals(doc.card)
    card_tot = getattr(doc.card, "total", None)
    if card_tot and str(card_tot).strip():
        parsed = rules.parse_money(card_tot)
        if parsed > 0:
            ttc = parsed
            ht = round(ttc / 1.20, 2)
            vat = round(ttc - ht, 2)
            products = round(ht - ship, 2)
    stroke_rect(
        c, *vectors.shifted(vectors.TOTAL_OUTER, extra),
        layout.STROKE_W, layout.COLOR, cap=layout.STROKE_CAP,
    )
    for rect in vectors.shifted_pair(vectors.TOTAL_VALUE_FILLS, extra):
        fill_rect(c, *rect, (1, 1, 1))
    for rect in vectors.shifted_pair(vectors.TOTAL_LABEL_FILLS, extra):
        fill_rect(c, *rect, layout.COLOR_CELL)
    labels = (
        texts.TOTAL_PRODUCTS,
        texts.TOTAL_SHIP,
        texts.TOTAL_HT,
        texts.TOTAL_TAX,
        texts.TOTAL,
    )
    ship_txt = texts.SHIP_FREE if ship == 0 else rules.format_eur(ship)
    amounts = (
        rules.format_eur(products),
        ship_txt,
        rules.format_eur(ht),
        rules.format_eur(vat),
        rules.format_eur(ttc),
    )
    fonts = (
        layout.FONT, layout.FONT, layout.FONT_BOLD,
        layout.FONT_BOLD, layout.FONT_BOLD,
    )
    sizes = (
        layout.SIZE_BODY, layout.SIZE_BODY, layout.SIZE_BODY,
        layout.SIZE_BODY, layout.SIZE_TOTAL,
    )
    fill(c, layout.COLOR)
    for i, label in enumerate(labels):
        draw_string(
            c, layout.TOTAL_LABEL_X[i], layout.TOTAL_LABEL_Y[i] + extra,
            rules.cell(label), fonts[i], sizes[i],
        )
        ax = layout.SHIP_FREE_X if i == 1 and ship == 0 else layout.TOTAL_VAL_X[i]
        draw_string(
            c, ax, layout.TOTAL_LABEL_Y[i] + extra,
            rules.cell(amounts[i]), fonts[i], sizes[i],
        )
