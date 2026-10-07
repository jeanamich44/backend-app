"""Ligne Powered by TCPDF — chrome 1 pt."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.footer_tcpdf:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.TCPDF_X, layout.TCPDF_Y,
        texts.TCPDF, layout.FONT, layout.SIZE_TCPDF,
        max_width=layout.TCPDF_MAX_W,
    )
