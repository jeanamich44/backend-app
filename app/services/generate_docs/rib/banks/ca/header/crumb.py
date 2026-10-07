"""Fil d'Ariane du bandeau web (une fois en haut de page, pas par coupon)."""

from .. import layout
from ..paint import clip, draw_string, fill, width

_SPACE = " "
_CHEVRON = ">"


def draw(c, doc, dy=0):
    if not doc.visible.header_crumb:
        return
    left = doc.header.crumb or ""
    link = doc.header.crumb_link or ""
    if not left and not link:
        return
    x = layout.CRUMB_X
    y = layout.CRUMB_Y + dy
    font = layout.FONT
    size = layout.CRUMB_SIZE
    pad = size * layout.CRUMB_CHEVRON_EM
    fill(c, layout.CRUMB_COLOR)
    if left:
        shown = clip(left, font, size, layout.CRUMB_W)
        draw_string(c, x, y, shown, font, size)
        x += width(shown, font, size)
        draw_string(c, x, y, _SPACE, font, size)
        x += width(_SPACE, font, size) + pad
        draw_string(c, x, y, _CHEVRON, font, size)
        x += width(_CHEVRON, font, size) + pad
        draw_string(c, x, y, _SPACE, font, size)
        x += width(_SPACE, font, size)
    if link:
        fill(c, layout.CRUMB_LINK_COLOR)
        draw_string(c, x, y, link, font, size, max_width=80.0)
