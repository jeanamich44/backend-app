"""Mentions légales Darty (chrome Times-Roman)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.footer_legal:
        return
    fill(c, layout.COLOR)
    for x, y, line in zip(layout.LEGAL_X, layout.LEGAL_Y, texts.LEGAL):
        draw_string(c, x, y, line, layout.FONT_TIMES, layout.SIZE_LEGAL)
