"""Filet sous PRIX TOTAL (LW page ~0,75, pas 1,0)."""

from .. import layout
from ..paint import stroke_line


def draw(c, doc):
    if not doc.visible.footer_line:
        return
    x0, y0, x1, y1 = layout.LINE_FOOT
    stroke_line(c, x0, y0, x1, y1, layout.TABLE_RULE_W, layout.COLOR)
