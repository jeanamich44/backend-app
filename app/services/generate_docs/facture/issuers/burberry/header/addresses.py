"""Adresses d'expédition et de facturation."""

from .. import copy as texts
from .. import layout, rules
from ..paint import draw_string, fill


def _column(c, title_y, title, ys, lines):
    fill(c, layout.COLOR)
    x = layout.RIGHT_X
    max_w = layout.ADDR_MAX_W
    draw_string(c, x, title_y, title, layout.FONT, layout.SIZE_BODY)
    for y, line in zip(ys, lines):
        draw_string(c, x, y, line, layout.FONT, layout.SIZE_BODY, max_width=max_w)


def draw(c, doc):
    if not doc.visible.header_addresses:
        return
    lines = rules.address_lines(doc.card)
    _column(c, layout.SHIP_TITLE_Y, texts.SHIP_TITLE, layout.SHIP_Y, lines)
    _column(c, layout.BILL_TITLE_Y, texts.BILL_TITLE, layout.BILL_Y, lines)
