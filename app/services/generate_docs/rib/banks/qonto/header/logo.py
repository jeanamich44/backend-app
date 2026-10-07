"""Wordmark qonto : fills vectoriels du gabarit."""

from .. import layout
from ..paint import fill_fills
from .paths import LOGO_FILLS


def draw(c, doc):
    if not doc.visible.header_logo:
        return
    fill_fills(c, LOGO_FILLS, layout.COLOR)
