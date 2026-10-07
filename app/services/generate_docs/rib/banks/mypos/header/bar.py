"""Bande bleue haute + filet gris sous l’en-tête."""

from .. import layout
from ..paint import fill_rect, stroke_line


def draw(c, doc):
    fill_rect(
        c, layout.BAR_X, layout.BAR_Y, layout.BAR_W, layout.BAR_H,
        layout.COLOR_BAR,
    )
    stroke_line(
        c, layout.LEFT_X, layout.RIGHT_X, layout.HEAD_LINE_Y,
        layout.HEAD_LINE_W, layout.COLOR_LINE_HEAD, cap=0,
    )
