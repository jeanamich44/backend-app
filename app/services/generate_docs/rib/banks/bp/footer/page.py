"""Pagination « 1 / 1 » (texte live, Arial 8 pt)."""

from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.footer_page:
        return
    text = doc.footer.page
    if not text:
        return
    fill(c, layout.FOOTER_COLOR)
    draw_string(
        c, layout.FOOTER_PAGE_X, layout.FOOTER_Y, text,
        layout.FOOTER_FONT, layout.FOOTER_SIZE,
        max_width=layout.FOOTER_PAGE_W,
    )
