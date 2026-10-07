"""Cadre or arrondi, trou sous le titre IBAN."""

from .. import layout
from ..paint import stroke_items
from .chrome_paths import FRAME_GAP, FRAME_STROKE


def draw(c, doc, dy=0):
    stroke_items(
        c, FRAME_STROKE, layout.COLOR_GOLD, layout.FRAME_W,
        dy=dy, cap=1, join=0, miter=4,
    )
    stroke_items(
        c, FRAME_GAP, layout.COLOR_GOLD, layout.FRAME_W,
        dy=dy, cap=1, join=0, miter=4,
    )
