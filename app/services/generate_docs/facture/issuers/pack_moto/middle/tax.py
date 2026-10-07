"""Détail des taxes — une ligne agrégée, décalée si extra articles."""

from .. import copy as texts
from .. import layout, rules
from ..paint import draw_string, fill, fill_rect, stroke_rect
from . import vectors


def draw(c, doc):
    if not doc.visible.middle_tax:
        return
    extra = layout.extra_y(doc.card)
    stroke_rect(
        c, *vectors.shifted(vectors.TAX_OUTER, extra),
        layout.STROKE_W, layout.COLOR, cap=layout.STROKE_CAP,
    )
    for rect in vectors.shifted_pair(vectors.TAX_VAL_FILLS, extra):
        fill_rect(c, *rect, (1, 1, 1))
    for rect in vectors.shifted_pair(vectors.TAX_HEAD_FILLS, extra):
        fill_rect(c, *rect, layout.COLOR_CELL)
    fill(c, layout.COLOR)
    for x, y, label in layout.TAX_TITLE:
        draw_string(
            c, x, y + extra, label,
            layout.FONT_BOLD, layout.SIZE_BODY,
        )
    _products, _ship, _ht, vat, _ttc = rules.invoice_totals(doc.card)
    rate = 0.0
    for item in doc.card.items or ():
        rate = rules.parse_money(item.tva)
        if rate:
            break
    values = (
        texts.TAX_KIND,
        rules.format_pct_tax(rate or 20.0),
        rules.format_eur(vat),
    )
    for x, value in zip(layout.TAX_VAL_X, values):
        draw_string(
            c, x, layout.TAX_VAL_Y + extra,
            rules.cell(value), layout.FONT, layout.SIZE_BODY,
        )
