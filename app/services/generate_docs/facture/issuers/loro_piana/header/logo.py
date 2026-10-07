"""Wordmark Loro Piana (XObject 447×94)."""

from .. import layout
from ..paint import draw_image


def draw(c, doc):
    if not doc.visible.header_logo:
        return
    draw_image(
        c, layout.LOGO_FILE,
        layout.LOGO_X, layout.LOGO_Y,
        layout.LOGO_W, layout.LOGO_H,
    )
