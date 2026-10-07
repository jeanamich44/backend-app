"""Séparateur entre coupons : PNG du gabarit (pas de vecteur)."""

from .. import layout
from ..paint import draw_chrome


def draw(c, doc, dy=0):
    if not doc.visible.middle_separator:
        return
    draw_chrome(
        c, layout.SEP_FILE,
        layout.SEP_X, layout.SEP_Y_TOP + dy,
        layout.SEP_W, layout.SEP_H,
    )
