"""Wordmark noelse : fills vectoriels du gabarit, 3 coupons."""

from .. import layout
from ..paint import fill_fills
from .paths import LOGO_FILLS


def draw(c, doc, dy=0):
    if not doc.visible.header_logo:
        return
    fill_fills(c, LOGO_FILLS, layout.LOGO_COLOR, dy=dy)
