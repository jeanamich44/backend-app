"""Filet au-dessus des mentions."""

from .. import layout
from ..paint import fill_rect


def draw(c, doc, rule_y):
    if not doc.visible.footer_line:
        return
    x0, x1 = layout.FOOTER_RULE_X
    fill_rect(c, x0, rule_y, x1, rule_y + layout.RULE_H, layout.COLOR_LINE)
