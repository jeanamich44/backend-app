"""Phrase légale verticale, marge gauche."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string_rot90, fill


def draw(c, doc):
    if not doc.visible.middle_legal:
        return
    fill(c, layout.COLOR)
    draw_string_rot90(
        c, layout.LEGAL_X, layout.LEGAL_Y,
        texts.LEGAL, layout.FONT, layout.SIZE_LEGAL,
    )
