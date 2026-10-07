"""Mentions légales Gotham Rounded Book 6 pt."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.footer_legal:
        return
    fill(c, layout.COLOR)
    for y, line in zip(layout.LEGAL_Y, texts.LEGAL):
        draw_string(
            c, layout.LEGAL_X, y, line,
            layout.FONT_GOTHAM, layout.LEGAL_SIZE,
            max_width=layout.LEGAL_MAX_W,
        )
