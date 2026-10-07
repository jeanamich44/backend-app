"""Libellé complémentaire, sous chaque coupon."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, i=0):
    if not doc.visible.middle_libelle:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.LIBELLE_X, layout.LIBELLE_Y + layout.dy_nat(i), texts.LIBELLE,
        layout.FONT, layout.LIBELLE_SIZE,
    )
