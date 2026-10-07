"""Wordmark myPOS : Form FO1 rejoué, fills du gabarit."""

from .. import layout
from ..paint import fill_groups, fill_rect
from .paths import FILLS


def draw(c, doc):
    if not doc.visible.header_logo:
        return
    x, y, w, h = layout.LOGO_MASK
    fill_rect(c, x, y, w, h)
    fill_groups(c, FILLS)
