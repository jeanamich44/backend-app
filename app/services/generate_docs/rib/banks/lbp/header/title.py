"""Titre centré haut de page."""

from .. import layout
from ..paint import fill, y_up


def draw(c, doc):
    if not doc.visible.header_title:
        return
    text = doc.header.title
    if not text:
        return
    c.setFont(layout.TITLE_FONT, layout.TITLE_SIZE)
    fill(c, layout.TITLE_COLOR)
    c.drawCentredString(layout.PAGE_W / 2.0, y_up(layout.TITLE_Y), text)
