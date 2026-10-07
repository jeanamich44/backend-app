"""Titre Reçu + filet Canva sous le titre."""

from .. import copy as texts
from .. import layout
from ..chrome import vectors
from ..paint import draw_string, fill, stroke_line


def draw(c, doc):
    if not doc.visible.header_title:
        return
    x0, y0, x1, y1 = vectors.HEADER_LINE
    stroke_line(c, x0, y0, x1, y1, layout.RULE_W, layout.COLOR)
    fill(c, layout.COLOR)
    draw_string(
        c, layout.TITLE_X, layout.TITLE_Y,
        texts.TITLE, layout.FONT_BOLD, layout.SIZE_TITLE,
    )
