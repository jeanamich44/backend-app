"""Marque Nike.com (orange)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_brand:
        return
    fill(c, layout.COLOR_BRAND)
    draw_string(
        c, layout.BRAND_X, layout.BRAND_Y,
        texts.BRAND, layout.FONT_BOLD, layout.SIZE_BRAND,
    )
