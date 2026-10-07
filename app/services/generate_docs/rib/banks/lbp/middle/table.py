"""Grille RIB : établissement, guichet, compte, clé, domiciliation."""

from .. import copy as texts
from .. import layout
from ..paint import draw_centred, draw_string, fill, stroke_line


def draw(c, doc, dy=0):
    if not doc.visible.middle_table:
        return
    card = doc.card
    for x0, y0, x1, y1, width in layout.TABLE_LINES:
        stroke_line(c, x0, y0 + dy, x1, y1 + dy, width)

    fill(c, layout.BRAND_TITLE_COLOR)
    draw_string(
        c, layout.TABLE_TITLE_X, layout.TABLE_TITLE_Y + dy,
        texts.TABLE_TITLE, layout.TABLE_VAL_FONT, layout.TABLE_TITLE_SIZE,
    )

    fill(c, layout.LINE_BLACK)
    heads = (
        texts.COL_ETABLISSEMENT,
        texts.COL_GUICHET,
        texts.COL_COMPTE,
        texts.COL_CLE,
        texts.COL_DOMICILIATION,
    )
    for (x, y), label in zip(layout.TABLE_HEADS, heads):
        draw_string(c, x, y + dy, label, layout.TABLE_HEAD_FONT, layout.TABLE_HEAD_SIZE)

    vals = (
        (layout.TABLE_CX_ETAB, card.etablissement, layout.TABLE_W_ETAB),
        (layout.TABLE_CX_GUICHET, card.guichet, layout.TABLE_W_GUICHET),
        (layout.TABLE_CX_COMPTE, card.compte, layout.TABLE_W_COMPTE),
        (layout.TABLE_CX_CLE, card.cle, layout.TABLE_W_CLE),
    )
    for cx, value, max_w in vals:
        if value:
            draw_centred(
                c, cx, layout.TABLE_VAL_Y + dy, value,
                layout.TABLE_VAL_FONT, layout.TABLE_VAL_SIZE,
                max_width=max_w,
            )
    if card.domiciliation:
        draw_string(
            c, layout.TABLE_DOM_X, layout.TABLE_DOM_Y + dy,
            card.domiciliation, layout.TABLE_VAL_FONT, layout.TABLE_DOM_SIZE,
            max_width=layout.TABLE_W_DOM,
        )
