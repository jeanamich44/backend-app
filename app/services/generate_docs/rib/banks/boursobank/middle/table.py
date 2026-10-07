"""Bloc RIB : label, en-têtes et valeurs (texte live, pas de cadre vecteur)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_table:
        return
    fill(c, layout.LABEL_COLOR)
    draw_string(
        c, layout.RIGHT_X, layout.LABEL_RIB_Y + dy,
        texts.LABEL_RIB, layout.LABEL_FONT, layout.LABEL_SIZE,
    )
    fill(c, layout.HEAD_COLOR)
    heads = (
        texts.COL_BANQUE,
        texts.COL_GUICHET,
        texts.COL_COMPTE,
        texts.COL_CLE,
    )
    for x, label in zip(layout.TABLE_XS, heads):
        draw_string(
            c, x, layout.TABLE_HEAD_Y + dy, label,
            layout.HEAD_FONT, layout.HEAD_SIZE,
        )
    fill(c, layout.VALUE_COLOR)
    card = doc.card
    vals = (
        card.banque,
        card.guichet,
        card.compte,
        card.cle,
    )
    for x, value, max_w in zip(layout.TABLE_XS, vals, layout.TABLE_W):
        if value:
            draw_string(
                c, x, layout.TABLE_VAL_Y + dy, value,
                layout.VALUE_FONT, layout.VALUE_SIZE,
                max_width=max_w,
            )
