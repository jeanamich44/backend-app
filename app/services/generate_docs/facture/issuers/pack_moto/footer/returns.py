"""Conditions de retour — chrome."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.footer_returns:
        return
    extra = layout.extra_y(doc.card) if doc.visible.middle else 0.0
    fill(c, layout.COLOR)
    for y, line in zip(layout.RETURN_Y, texts.RETURNS):
        draw_string(
            c, layout.RETURN_X, y + extra, line,
            layout.FONT, layout.SIZE_RETURN,
            max_width=layout.RETURN_MAX_W,
        )
