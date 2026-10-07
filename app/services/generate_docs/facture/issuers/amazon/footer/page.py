"""Pagination Page N de M."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string


def draw(c, doc, page_y, current, total):
    if not doc.visible.footer_page:
        return
    x_page, x_cur, x_of, x_max = layout.PAGE_X
    muted = layout.COLOR_MUTED
    uni = layout.FONT_UNI
    size = layout.SIZE_PAGE
    draw_string(c, x_page, page_y, texts.PAGE_LABEL, uni, size, color=muted)
    draw_string(c, x_cur, page_y, str(current), uni, size, color=layout.COLOR)
    draw_string(c, x_of, page_y, texts.PAGE_OF, uni, size, color=muted)
    draw_string(c, x_max, page_y, str(total), uni, size, color=layout.COLOR)
