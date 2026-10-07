"""Césure entre coupons : ciseaux + trait pointillé."""

from .. import layout
from ..paint import draw_image, stroke_line


def draw(c, doc, dy=0):
    if not doc.visible.middle_separator:
        return
    draw_image(
        c, layout.CUT_FILE,
        layout.CUT_X, layout.CUT_Y_TOP + dy,
        layout.CUT_W, layout.CUT_H,
    )
    stroke_line(
        c, layout.SEP_X0, layout.SEP_Y + dy, layout.SEP_X1, layout.SEP_Y + dy,
        layout.SEP_STROKE,
        dash=layout.SEP_DASH,
        phase=layout.SEP_DASH_PHASE,
    )
