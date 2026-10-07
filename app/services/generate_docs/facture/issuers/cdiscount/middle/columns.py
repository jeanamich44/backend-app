"""Colonnes Produit / Qté / Montant + filets."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill, stroke_line


def draw(c, doc):
    if not doc.visible.middle_columns:
        return
    fill(c, layout.COLOR_COL)
    draw_string(
        c, layout.COL_PRODUIT_X, layout.COL_Y,
        texts.COL_PRODUIT, layout.FONT_BOLD, layout.SIZE_COL,
        max_width=layout.COL_MAX_W,
    )
    draw_string(
        c, layout.COL_QTE_X, layout.COL_Y,
        texts.COL_QTE, layout.FONT_BOLD, layout.SIZE_COL,
    )
    draw_string(
        c, layout.COL_MNT_X, layout.COL_Y,
        texts.COL_MNT, layout.FONT_BOLD, layout.SIZE_COL,
        max_width=layout.COL_MAX_W,
    )
    for x0, y, x1, w in layout.COL_RULES:
        stroke_line(c, x0, y, x1, y, w, layout.COLOR_BAND)
