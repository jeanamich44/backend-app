"""Fond de la carte : filet arrondi gris outlined."""

from .. import layout
from ..paint import draw_svg


def draw(c, doc):
    if not doc.visible.middle_card:
        return
    draw_svg(
        c, layout.CARD_SVG,
        layout.CARD_X, layout.CARD_Y_TOP,
        layout.CARD_W, layout.CARD_H,
    )
