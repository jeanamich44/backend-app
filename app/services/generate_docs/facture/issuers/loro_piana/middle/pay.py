"""Paiement + monnaie rendue (€ à gauche, montant à droite)."""

from .. import copy as texts
from .. import layout, rules
from ..paint import draw_right, draw_string, fill


def _euro_amount(c, y, amount, font, size):
    draw_string(c, layout.PAY_EURO_X, y, "€", font, size)
    draw_right(c, layout.PAY_AMT_RIGHT, y, rules.format_money(amount), font, size)


def draw(c, doc):
    if not doc.visible.middle_pay:
        return
    dy = layout.table_shift(doc.card)
    ttc = rules.items_total(doc.card.items)
    monnaie = rules.parse_money(doc.card.monnaie)
    fill(c, layout.COLOR)
    draw_string(
        c, layout.PAY_LABEL_X, layout.PAY_LABEL_Y + dy,
        texts.PAIEMENT, layout.FONT_BOLD, layout.SIZE_BODY,
    )
    if doc.card.payment:
        draw_string(
            c, layout.PAY_VAL_X, layout.PAY_VAL_Y + dy,
            doc.card.payment, layout.FONT_BOLD, layout.SIZE_BODY,
            max_width=layout.PAY_MAX_W,
        )
    _euro_amount(
        c, layout.PAY_VAL_Y + dy, ttc,
        layout.FONT_BOLD, layout.SIZE_BODY,
    )
    draw_string(
        c, layout.PAY_LABEL_X, layout.MONNAIE_Y + dy,
        texts.MONNAIE, layout.FONT_BOLD, layout.SIZE_BODY,
    )
    _euro_amount(
        c, layout.MONNAIE_Y + dy, monnaie,
        layout.FONT_BOLD, layout.SIZE_BODY,
    )
