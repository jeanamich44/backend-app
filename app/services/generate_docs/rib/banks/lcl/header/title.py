"""Titre RELEVE D'IDENTITE BANCAIRE, Verdana-Bold 5.5 navy."""

from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, i=0):
    if not doc.visible.header_title:
        return
    text = doc.header.title
    if not text:
        return
    fill(c, layout.TITLE_COLOR)
    draw_string(
        c, layout.TITLE_X, layout.TITLE_Y + layout.dy(i), text,
        layout.TITLE_FONT, layout.TITLE_SIZE,
        max_width=layout.TITLE_W,
    )
