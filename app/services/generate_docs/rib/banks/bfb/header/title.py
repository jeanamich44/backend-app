"""Titre Relevé d'Identité Bancaire (chrome outlined)."""

from .. import layout
from ..paint import draw_svg


def draw(c, doc):
    if not doc.visible.header_title:
        return
    draw_svg(
        c, layout.TITLE_SVG,
        layout.TITLE_X, layout.TITLE_Y_TOP,
        layout.TITLE_W, layout.TITLE_H,
    )
