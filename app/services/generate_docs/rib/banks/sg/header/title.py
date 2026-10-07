"""Titre RELEVÉ D'IDENTITÉ BANCAIRE / IBAN (Helvetica-Bold 12, fill-only)."""

from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.header_title:
        return
    text = doc.header.title
    if not text:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.TITLE_X, layout.TITLE_Y + dy, text,
        layout.FONT_BOLD, layout.SIZE_TITLE,
        max_width=layout.TITLE_W,
    )
