"""Séparateurs : ligne de tirets entre coupons + filets segmentés en bas de page."""

from .. import layout
from ..paint import draw_string, fill, stroke_line


def draw(c, doc, dy=0):
    if not doc.visible.middle_separator:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.SEP_X, layout.SEP_Y + dy, layout.SEP_TEXT,
        layout.FONT, layout.SEP_SIZE,
    )


def draw_dashes(c, doc):
    if not doc.visible.middle_separator:
        return
    for x0, x1 in layout.SEP_DASH_SEGS:
        stroke_line(
            c, x0, layout.SEP_DASH_Y, x1, layout.SEP_DASH_Y,
            layout.SEP_DASH_W, layout.COLOR, cap=layout.TABLE_CAP,
        )
