"""Bloc PACKMOTO Bagnolet + téléphone — chrome."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.footer_issuer:
        return
    fill(c, layout.COLOR_TITLE)
    for (x, y), line in zip(layout.LEGAL, texts.LEGAL):
        draw_string(
            c, x, y, line,
            layout.FONT, layout.SIZE_LEGAL,
            max_width=layout.LEGAL_MAX_W,
        )
