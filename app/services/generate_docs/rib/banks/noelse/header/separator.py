"""Filets pointillés entre coupons (50 % d’opacité)."""

from .. import layout
from ..paint import stroke_line


def draw(c, doc):
    for y in layout.SEP_YS:
        stroke_line(
            c, layout.SEP_X0, layout.SEP_X1, y, layout.SEP_W,
            layout.COLOR_SEP, cap=0, dash=layout.SEP_DASH,
            alpha=layout.SEP_ALPHA,
        )
