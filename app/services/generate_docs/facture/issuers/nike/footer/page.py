"""Pagination « Page 1 of 1 »."""

from .. import copy as texts
from .. import layout
from ..paint import draw_center_kerned, fill


def draw(c, doc):
    if not doc.visible.footer_page:
        return
    fill(c, layout.COLOR)
    draw_center_kerned(
        c, layout.PAGE_X, layout.PAGE_Y,
        texts.PAGE, layout.FONT, layout.SIZE_PAGE,
    )
