"""Date d’édition, à gauche."""

from .. import layout
from ..paint import draw_string, fill_rgb


def draw(c, doc):
    if not doc.visible.header_date or not doc.header.date:
        return
    fill_rgb(c, layout.COLOR)
    draw_string(
        c, layout.DATE_X, layout.DATE_Y, doc.header.date,
        layout.FONT, layout.SIZE_BODY,
    )
