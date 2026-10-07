"""Filets remplis sous le tableau RIB et sous IBAN/BIC."""

from .. import layout
from ..paint import fill_rect


def draw(c, doc, dy=0):
    if not doc.visible.middle_lines:
        return
    for x0, y0, x1, y1 in layout.RIB_RULES + layout.INTL_RULES:
        fill_rect(c, x0, y0 + dy, x1, y1 + dy, layout.COLOR)
