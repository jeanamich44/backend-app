"""Wordmark Engie — chemins D19 du flux original."""

from .. import layout
from ..chrome.header_paths import LOGO_EVEN_ODD, LOGO_OPS
from ..paint import fill_ops


def draw(c, doc):
    if not doc.visible.header_logo:
        return
    fill_ops(c, LOGO_OPS, layout.BLUE, even_odd=LOGO_EVEN_ODD)
