"""Méthode de paiement + Payé avec / Merci."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.footer_payment:
        return
    fill(c, layout.COLOR)
    font = layout.FONT
    size = layout.SIZE_BODY
    draw_string(
        c, layout.PAY_LABEL_X, layout.PAY_LABEL_Y,
        texts.PAY_LABEL, font, size,
    )
    draw_string(
        c, layout.PAY_VALUE_X, layout.PAY_WITH_Y,
        texts.PAY_WITH, font, size,
    )
    draw_string(
        c, layout.PAY_VALUE_X, layout.PAY_CARD_Y,
        doc.card.payment_mode or "", font, size,
        max_width=layout.PAY_MAX_W,
    )
    draw_string(
        c, layout.PAY_VALUE_X, layout.PAY_THANKS_Y,
        texts.PAY_THANKS, font, size,
    )
