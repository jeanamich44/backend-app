"""Adresse de livraison / facturation + titulaire dummy."""

from .. import copy as texts
from .. import layout, rules
from ..paint import draw_string, fill


def _block(c, x, y0, lines, max_w):
    for i, line in enumerate(lines):
        draw_string(
            c, x, y0 + i * layout.ADDR_PITCH,
            line, layout.FONT, layout.SIZE_ADDR,
            max_width=max_w,
        )


def draw(c, doc):
    if not doc.visible.header_addresses:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.SHIP_X, layout.ADDR_TITLE_Y,
        texts.SHIP_TITLE, layout.FONT_BOLD, layout.SIZE_ADDR_TITLE,
        max_width=layout.SHIP_MAX_W,
    )
    draw_string(
        c, layout.BILL_X, layout.ADDR_TITLE_Y,
        texts.BILL_TITLE, layout.FONT_BOLD, layout.SIZE_ADDR_TITLE,
        max_width=layout.BILL_MAX_W,
    )
    _block(c, layout.SHIP_X, layout.ADDR_Y0, rules.ship_lines(doc.card), layout.SHIP_MAX_W)
    _block(c, layout.BILL_X, layout.ADDR_Y0, rules.bill_lines(doc.card), layout.BILL_MAX_W)
