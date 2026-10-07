"""Filets gris continus (rectangles 0.8 pt, pas des tirets)."""

from .. import layout
from ..paint import fill_rect


def draw(c, doc, dy=0):
    if not doc.visible.middle_lines:
        return
    for y in layout.LINE_Y:
        fill_rect(
            c,
            layout.LINE_X0,
            y + dy,
            layout.LINE_X1,
            y + dy + layout.LINE_H,
            layout.LINE_COLOR,
        )
