"""Mentions légales émetteur (EU vendu par Amazon / OSS marketplace)."""

from .. import layout
from ..paint import draw_string


def draw(c, doc, ys, lines):
    if not doc.visible.footer_legal:
        return
    for y, text in zip(ys, lines):
        draw_string(
            c, layout.FOOTER_X, y,
            text, layout.FONT_UNI, layout.SIZE_FOOTER,
            color=layout.COLOR_MUTED, max_width=540,
        )
