"""Société (Bold 7.5 gris) + titre Coordonnées bancaires (Bold 15.75)."""

from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_title:
        return
    company = doc.card.titulaire_nom
    if company:
        fill(c, layout.COLOR_GRAY)
        draw_string(
            c, layout.LEFT_X, layout.COMPANY_Y, company,
            layout.FONT_BOLD, layout.SIZE_COMPANY,
            max_width=layout.TITLE_W,
        )
    title = doc.header.title
    if title:
        fill(c, layout.COLOR)
        draw_string(
            c, layout.LEFT_X, layout.TITLE_Y, title,
            layout.FONT_BOLD, layout.SIZE_TITLE,
            max_width=layout.TITLE_W,
            char_space=0.0002,
        )
