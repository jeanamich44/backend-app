"""Ligne Votre commande."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.middle_order:
        return
    card = doc.card
    fill(c, layout.COLOR)
    draw_string(
        c, layout.ORDER_X, layout.ORDER_Y,
        texts.ORDER_L + (card.num_commande or "") + texts.ORDER_MID
        + (card.date_commande or ""),
        layout.FONT_BOLD, layout.SIZE_ORDER,
        max_width=layout.ORDER_MAX_W,
    )
