"""Bloc Thank you / next order."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.footer_thanks:
        return
    fill(c, layout.COLOR)
    for y, line in zip(layout.THANKS_Y, texts.THANKS):
        draw_string(
            c, layout.THANKS_X, y, line,
            layout.FONT_FOOTER, layout.SIZE_FOOTER,
            max_width=layout.THANKS_MAX_W,
        )
