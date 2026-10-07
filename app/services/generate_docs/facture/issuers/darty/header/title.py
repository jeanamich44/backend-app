"""JUSTIFICATIF DE VENTE + date."""

from .. import copy as texts
from .. import layout
from ..chrome import vectors
from ..paint import draw_string, fill, fill_rect


def draw(c, doc):
    if not doc.visible.header_title:
        return
    for x0, y0, x1, y1, color in vectors.TITLE_FILLS:
        fill_rect(c, x0, y0, x1, y1, color)
    fill(c, layout.COLOR_GRAY)
    draw_string(
        c, layout.UNDER_X, layout.UNDER_Y,
        texts.UNDER, layout.FONT_BOLD, layout.SIZE_UNDER,
    )
    fill(c, layout.COLOR)
    draw_string(
        c, layout.TITLE_X, layout.TITLE_Y,
        texts.TITLE, layout.FONT_BOLD, layout.SIZE_TITLE,
        max_width=layout.TITLE_MAX_W,
    )
    draw_string(
        c, layout.DATE_X, layout.DATE_Y,
        texts.DATE_PREFIX + (doc.card.date_facture or ""),
        layout.FONT_BOLD, layout.SIZE_DATE,
        max_width=layout.DATE_MAX_W,
    )
