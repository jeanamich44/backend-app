"""Coupe sous chaque coupon : filet [1.8 0.9] clippé à 0.75 pt."""

from .. import layout
from ..paint import stroke_dash


def draw(c, doc, dy=0):
    if not doc.visible.middle_separator:
        return
    stroke_dash(
        c,
        layout.SEP_X0,
        layout.SEP_X1,
        layout.SEP_Y + dy,
        layout.SEP_W,
        layout.SEP_DASH,
        layout.COLOR,
        clip_y0=layout.SEP_CLIP_Y0 + dy,
        clip_y1=layout.SEP_CLIP_Y1 + dy,
    )
