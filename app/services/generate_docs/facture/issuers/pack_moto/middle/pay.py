"""Moyen de paiement + transporteur, décalés si extra articles."""

from .. import copy as texts
from .. import layout, rules
from ..paint import draw_string, fill, fill_rect, stroke_rect
from . import vectors


def draw(c, doc):
    if not doc.visible.middle_pay:
        return
    extra = layout.extra_y(doc.card)
    _p, _s, _h, _v, ttc = rules.invoice_totals(doc.card)
    stroke_rect(
        c, *vectors.shifted(vectors.PAY_OUTER, extra),
        layout.STROKE_W, layout.COLOR, cap=layout.STROKE_CAP,
    )
    fill_rect(c, *vectors.shifted(vectors.PAY_VAL, extra), (1, 1, 1))
    fill_rect(c, *vectors.shifted(vectors.PAY_HEAD, extra), layout.COLOR_CELL)
    stroke_rect(
        c, *vectors.shifted(vectors.CARRIER_OUTER, extra),
        layout.STROKE_W, layout.COLOR, cap=layout.STROKE_CAP,
    )
    fill_rect(c, *vectors.shifted(vectors.CARRIER_VAL, extra), (1, 1, 1))
    fill_rect(c, *vectors.shifted(vectors.CARRIER_HEAD, extra), layout.COLOR_CELL)
    fill(c, layout.COLOR)
    draw_string(
        c, layout.PAY_LABEL_X, layout.PAY_LABEL_Y + extra,
        texts.PAY_LABEL, layout.FONT_BOLD, layout.SIZE_PAY,
        max_width=layout.PAY_MAX_W,
    )
    draw_string(
        c, layout.PAY_VAL_X, layout.PAY_VAL_Y + extra,
        doc.card.payment or "", layout.FONT, layout.SIZE_PAY,
        max_width=layout.PAY_MAX_W,
    )
    draw_string(
        c, layout.PAY_AMT_X, layout.PAY_VAL_Y + extra,
        rules.format_eur(ttc), layout.FONT, layout.SIZE_PAY,
        max_width=layout.PAY_MAX_W,
    )
    draw_string(
        c, layout.CARRIER_LABEL_X, layout.CARRIER_LABEL_Y + extra,
        texts.CARRIER_LABEL, layout.FONT_BOLD, layout.SIZE_PAY,
        max_width=layout.PAY_MAX_W,
    )
    draw_string(
        c, layout.CARRIER_VAL_X, layout.CARRIER_VAL_Y + extra,
        doc.card.transporteur or "", layout.FONT, layout.SIZE_PAY,
        max_width=layout.CARRIER_MAX_W,
    )
