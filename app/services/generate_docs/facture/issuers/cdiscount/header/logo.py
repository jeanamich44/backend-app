"""Wordmark Cdiscount - Marketplace (Helvetica-Bold 25 pt)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_logo:
        return
    fill(c, layout.COLOR_LOGO)
    logo_text = "Cdiscount" if getattr(doc.card, "sold_by_cdiscount", True) else texts.LOGO
    draw_string(
        c, layout.LOGO_X, layout.LOGO_Y,
        logo_text, layout.FONT_BOLD, layout.SIZE_LOGO,
        max_width=layout.LOGO_MAX_W,
    )
