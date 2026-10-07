"""Adresse siège myPOS Ltd, alignée à droite (chrome)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_right, fill_rgb


def draw(c, doc):
    if not doc.visible.header_address:
        return
    x = layout.RIGHT_X
    fill_rgb(c, layout.COLOR_BRAND)
    draw_right(c, x, layout.BRAND_Y, texts.BRAND, layout.FONT_BOLD, layout.SIZE_BRAND)
    fill_rgb(c, layout.COLOR)
    for y, line in zip(layout.ADDR_YS, (texts.ADDR_1, texts.ADDR_2, texts.ADDR_3)):
        draw_right(c, x, y, line, layout.FONT, layout.SIZE_BODY)
