"""Filet bleu entre les deux cartes."""

from .. import layout
from ..paint import stroke_line


def draw(c, doc):
    if not doc.visible.middle_separator:
        return
    stroke_line(
        c, layout.SEP_X0, layout.SEP_Y, layout.MARGIN_RIGHT, layout.SEP_Y,
        layout.SEP_W, layout.BRAND_TITLE_COLOR,
        dash=layout.SEP_DASH, cap=1,
    )
