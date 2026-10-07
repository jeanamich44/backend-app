"""Titre Account details statement + date du document."""

from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, dy=0):
    fill(c, layout.COLOR)
    if doc.visible.header_title and doc.header.title:
        draw_string(
            c, layout.TITLE_X, layout.TITLE_Y + dy, doc.header.title,
            layout.FONT_BOLD, layout.SIZE_TITLE,
            max_width=layout.COL_W + 280,
            char_space=layout.TITLE_TRACK,
        )
    if doc.visible.header_date and doc.header.date:
        draw_string(
            c, layout.TITLE_X, layout.DATE_Y + dy, doc.header.date,
            layout.FONT, layout.SIZE_VALUE,
            max_width=layout.COL_W + 80,
        )
