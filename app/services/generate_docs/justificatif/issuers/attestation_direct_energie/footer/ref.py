"""Réf. courrier CS197 — chrome."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.footer_ref:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.REF_X, layout.REF_Y,
        texts.REF, layout.FONT, layout.REF_SIZE,
        max_width=layout.REF_MAX_W,
    )
