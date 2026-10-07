"""FACTURE + date + n° facture, alignés à droite."""

from .. import layout
from ..paint import draw_right, fill


def draw(c, doc):
    if not doc.visible.header_title:
        return
    card = doc.card
    fill(c, layout.COLOR_TITLE)
    draw_right(
        c, layout.TITLE_RIGHT, layout.TITLE_Y,
        "FACTURE", layout.FONT_BOLD, layout.SIZE_TITLE,
        max_width=layout.TITLE_MAX_W,
    )
    fill(c, layout.COLOR_MUTED)
    draw_right(
        c, layout.TITLE_RIGHT, layout.DATE_Y,
        card.date_facture or "", layout.FONT, layout.SIZE_TITLE,
        max_width=layout.TITLE_MAX_W,
    )
    draw_right(
        c, layout.TITLE_RIGHT, layout.NUM_Y,
        card.num_facture or "", layout.FONT, layout.SIZE_TITLE,
        max_width=layout.TITLE_MAX_W,
    )
