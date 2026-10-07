"""Bloc service client (chrome émetteur)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_service:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.SERVICE_TITLE_X, layout.SERVICE_TITLE_Y,
        texts.SERVICE_TITLE, layout.FONT_BOLD, layout.SIZE_SERVICE,
    )
    for y, (label, value) in zip(layout.SERVICE_Y, texts.SERVICE_ROWS):
        draw_string(
            c, layout.SERVICE_LABEL_X, y,
            label, layout.FONT, layout.SIZE_BODY,
        )
        draw_string(
            c, layout.SERVICE_VALUE_X, y,
            value, layout.FONT, layout.SIZE_BODY,
        )
