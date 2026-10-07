"""Lieu de consommation + détail p.2."""

from .. import copy as texts
from .. import layout, rules
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_lieu:
        return
    fill(c, layout.COLOR_BLUE)
    draw_string(
        c, layout.REF_X, layout.LIEU_LABEL_Y,
        texts.LIEU_LABEL, layout.FONT_BOLD, layout.SIZE_REF,
        max_width=layout.LIEU_MAX_W,
    )
    fill(c, layout.COLOR)
    for y, line in zip(layout.LIEU_Y, rules.lieu_lines(doc.card)):
        draw_string(
            c, layout.REF_X, y, line,
            layout.FONT, layout.SIZE_LIEU,
            max_width=layout.LIEU_MAX_W,
        )
    draw_string(
        c, layout.REF_X, layout.DETAIL_Y,
        texts.DETAIL, layout.FONT, layout.SIZE_LIEU,
        max_width=layout.LIEU_MAX_W,
    )
