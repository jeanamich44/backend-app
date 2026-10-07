"""Bloc service client (chrome émetteur)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_service:
        return
    fill(c, layout.COLOR)
    for y, line in zip(layout.SERVICE_Y, texts.SERVICE_LINES):
        draw_string(c, layout.SERVICE_X, y, line, layout.FONT, layout.SIZE_BODY)
