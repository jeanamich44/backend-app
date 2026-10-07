"""Coupe entre coupons : filet pointillé stroke + ciseaux PNG."""

from .. import layout
from ..paint import draw_chrome, stroke_dash


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
        layout.SEP_COLOR,
        clip_y0=layout.SEP_CLIP_Y0 + dy,
        clip_y1=layout.SEP_CLIP_Y1 + dy,
    )
    draw_chrome(
        c, layout.SCISSORS_FILE,
        layout.SCISSORS_X, layout.SCISSORS_Y_TOP + dy,
        layout.SCISSORS_W, layout.SCISSORS_H,
    )
