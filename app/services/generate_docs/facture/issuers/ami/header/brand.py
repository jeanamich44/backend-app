"""Filet haut + AMI PARIS - ALEXANDRE MATTIUSSI."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill, stroke_line


def draw(c, doc):
    if not doc.visible.header_brand:
        return
    stroke_line(
        c, layout.RULE_X0, layout.RULE_Y, layout.RULE_X1, layout.RULE_Y,
        layout.RULE_W, layout.COLOR,
    )
    fill(c, layout.COLOR)
    draw_string(
        c, layout.BRAND_X, layout.BRAND_Y,
        texts.BRAND, layout.FONT_BOLD, layout.SIZE_BRAND,
    )
