"""Titre Facture rouge + cadre PDF4NET."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string_html, fill, html_frame, stroke_html_border


def draw(c, doc):
    if not doc.visible.header_title:
        return
    c.saveState()
    html_frame(c, layout.TITLE_FRAME_X, layout.TITLE_FRAME_Y)
    stroke_html_border(c, layout.TITLE_SIDES, layout.TITLE_BOX_W, layout.COLOR)
    fill(c, layout.COLOR_TITLE)
    draw_string_html(
        c, layout.TITLE_TM[0], layout.TITLE_TM[1],
        texts.TITLE, layout.FONT, layout.SIZE_TITLE,
    )
    c.restoreState()
