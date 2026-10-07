"""Bloc vendeur."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill, fill_rect, stroke_line


def draw(c, doc):
    if not doc.visible.middle_vendor:
        return
    card = doc.card
    dy = layout.table_shift(card)
    for x0, y0, x1, y1, color in layout.shifted_fills(layout.VENDOR_FILLS, dy):
        fill_rect(c, x0, y0, x1, y1, color)
    fill(c, layout.COLOR)
    draw_string(
        c, layout.VENDOR_X, layout.VENDOR_TITLE_Y + dy,
        texts.VENDOR, layout.FONT_BOLD, layout.SIZE_VENDOR,
        max_width=layout.VENDOR_MAX_W,
    )
    if not getattr(card, "sold_by_cdiscount", True):
        fill(c, layout.COLOR_LINK)
        draw_string(
            c, layout.VENDOR_LINK_X, layout.VENDOR_LINK_Y + dy,
            texts.VENDOR_LINK, layout.FONT, layout.SIZE_LINK,
            max_width=layout.VENDOR_LINK_MAX_W,
        )
        x0, y, x1, w = layout.shifted_rule(layout.VENDOR_LINK_RULE, dy)
        stroke_line(c, x0, y, x1, y, w, layout.COLOR_LINK)
    fill(c, layout.COLOR_MUTED)
    if card.vendeur:
        draw_string(
            c, layout.VENDOR_X, layout.VENDOR_BY_Y + dy,
            texts.VENDOR_BY + card.vendeur,
            layout.FONT, layout.SIZE_VENDOR_BODY,
            max_width=layout.VENDOR_MAX_W,
        )
    if card.immat:
        draw_string(
            c, layout.VENDOR_X, layout.VENDOR_IMMAT_Y + dy,
            texts.VENDOR_IMMAT + card.immat,
            layout.FONT, layout.SIZE_VENDOR_BODY,
            max_width=layout.VENDOR_MAX_W,
        )
