"""Trait D12 sous les mentions."""

from .. import layout
from ..paint import stroke_line


def draw(c, doc):
    if not doc.visible.footer_line:
        return
    x0, y0 = layout.RULE_FROM
    x1, y1 = layout.RULE_TO
    stroke_line(c, x0, y0, x1, y1, layout.RULE_W, layout.COLOR_RULE, cap=0)
