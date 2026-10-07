"""Page 1 / 1."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.footer_page:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.PAGE_X, layout.PAGE_Y,
        texts.PAGE, layout.FONT, layout.SIZE_PAGE,
    )
