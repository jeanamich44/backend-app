"""Lien CGU + filet."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill, stroke_line


def draw(c, doc):
    if not doc.visible.footer_cgu:
        return
    fill(c, layout.COLOR_LINK)
    draw_string(
        c, layout.CGU_X, layout.CGU_Y,
        texts.CGU, layout.FONT, layout.SIZE_FOOT,
    )
    x0, y, x1, w = layout.CGU_RULE
    stroke_line(c, x0, y, x1, y, w, layout.COLOR_LINK)
