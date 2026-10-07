"""Titre produit + mode de règlement."""

from .. import copy as texts
from .. import layout
from ..paint import draw_right, draw_string, fill, fill_rect


def draw(c, doc):
    if not doc.visible.middle_heading:
        return
    for x0, y0, x1, y1, color in layout.PAY_FILLS:
        fill_rect(c, x0, y0, x1, y1, color)
    fill(c, layout.COLOR)
    draw_string(
        c, layout.PRODUCT_X, layout.PRODUCT_Y,
        texts.PRODUCT, layout.FONT_BOLD, layout.SIZE_PRODUCT,
        max_width=layout.PRODUCT_MAX_W,
    )
    draw_string(
        c, layout.PAY_LABEL_X, layout.PAY_Y,
        texts.PAY_LABEL, layout.FONT_BOLD, layout.SIZE_PAY,
        max_width=layout.PAY_MAX_W,
    )
    fill(c, layout.COLOR_MUTED)
    draw_right(
        c, layout.PAY_RIGHT, layout.PAY_Y,
        doc.card.payment or "", layout.FONT_BOLD, layout.SIZE_PAY,
        max_width=layout.PAY_MAX_W,
    )
