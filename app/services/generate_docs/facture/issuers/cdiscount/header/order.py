"""Bloc commande dans le cartouche blanc."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_order:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.ORDER_X, layout.ORDER_Y[0],
        texts.ORDER_L1, layout.FONT, layout.SIZE_ORDER,
        max_width=layout.ORDER_MAX_W,
    )
    draw_string(
        c, layout.ORDER_X, layout.ORDER_Y[1],
        texts.ORDER_L2 + (doc.card.num_commande or ""),
        layout.FONT, layout.SIZE_ORDER,
        max_width=layout.ORDER_MAX_W,
    )
    fill(c, layout.COLOR_MUTED)
    draw_string(
        c, layout.DATE_X, layout.DATE_Y,
        texts.DATE_PREFIX + (doc.card.date_commande or ""),
        layout.FONT, layout.SIZE_DATE,
        max_width=layout.DATE_MAX_W,
    )
