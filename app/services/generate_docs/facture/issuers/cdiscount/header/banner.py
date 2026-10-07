"""Fonds gris / blanc du bandeau (D0–D15, D28)."""

from .. import layout
from ..paint import fill_rect


def draw(c, doc):
    if not doc.visible.header_banner:
        return
    for x0, y0, x1, y1, color in layout.BAND_FILLS:
        fill_rect(c, x0, y0, x1, y1, color)
