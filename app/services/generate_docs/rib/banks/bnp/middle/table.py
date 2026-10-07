"""Tableau RIB : cadre + grille vecteur, en-têtes live, valeurs centrées."""

from .. import copy as texts
from .. import layout
from ..paint import draw_centred, draw_string, fill, stroke_line, stroke_rect


def draw(c, doc, dy=0):
    if not doc.visible.middle_table:
        return
    x0, y0, x1, y1 = layout.TABLE_BOX
    stroke_rect(c, x0, y0 + dy, x1, y1 + dy, layout.BOX_STROKE, fill_hex="#ffffff")
    for x in layout.TABLE_VLINES_X:
        stroke_line(
            c, x, layout.TABLE_VLINE_Y0 + dy, x, layout.TABLE_VLINE_Y1 + dy,
            layout.GRID_STROKE,
        )
    hx0, hy, hx1, hy1 = layout.TABLE_HLINE
    stroke_line(c, hx0, hy + dy, hx1, hy1 + dy, layout.GRID_STROKE)

    fill(c, layout.COLOR)
    draw_string(
        c, layout.LABEL_RIB_XY[0], layout.LABEL_RIB_XY[1] + dy,
        texts.LABEL_RIB, layout.FONT, layout.FONT_SIZE,
    )
    draw_string(
        c, layout.REF_RIB_XY[0], layout.REF_RIB_XY[1] + dy,
        texts.REF_3, layout.FONT, layout.FONT_REF_SIZE,
    )
    heads = (
        texts.COL_BANQUE,
        texts.COL_AGENCE,
        texts.COL_COMPTE,
        texts.COL_CLE,
        texts.COL_DOM,
    )
    for (x, y), label in zip(layout.TABLE_HEADS, heads):
        draw_string(c, x, y + dy, label, layout.FONT, layout.FONT_SIZE)

    card = doc.card
    vals = (
        (layout.TABLE_CX[0], card.banque, layout.TABLE_W[0]),
        (layout.TABLE_CX[1], card.guichet, layout.TABLE_W[1]),
        (layout.TABLE_CX[2], card.compte, layout.TABLE_W[2]),
        (layout.TABLE_CX[3], card.cle, layout.TABLE_W[3]),
        (layout.TABLE_CX[4], card.domiciliation, layout.TABLE_W[4]),
    )
    for cx, value, max_w in vals:
        if value:
            draw_centred(
                c, cx, layout.TABLE_VAL_Y + dy, value,
                layout.FONT_BOLD, layout.FONT_SIZE,
                max_width=max_w,
            )
