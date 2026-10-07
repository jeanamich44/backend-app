"""Bloc émetteur (chrome gabarit)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_issuer:
        return
    fill(c, layout.COLOR)
    for i, line in enumerate(texts.ISSUER):
        font = layout.FONT_BOLD if i == len(texts.ISSUER) - 1 else layout.FONT
        draw_string(
            c, layout.ISSUER_X, layout.ISSUER_Y[i],
            line, font, layout.SIZE_ISSUER,
            max_width=layout.ISSUER_MAX_W,
        )
