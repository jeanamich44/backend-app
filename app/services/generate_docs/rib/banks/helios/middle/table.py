"""Tableau RIB : labels 2× fill, valeurs fill+stroke."""

from .. import copy as texts
from .. import layout
from ..paint import draw_centered_label, draw_centered_value, draw_label, draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_table:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.RIB_TITLE_X, layout.RIB_TITLE_Y + dy, texts.RIB_TITLE + " ",
        layout.FONT_BOLD, layout.SIZE_SECTION,
    )
    fill(c, layout.LABEL_COLOR)
    draw_label(
        c, layout.RIB_SUP_X, layout.RIB_SUP_Y + dy, texts.SUP_RIB,
        layout.FONT, layout.SIZE_SUP,
    )
    heads = (texts.COL_BANQUE, texts.COL_GUICHET, texts.COL_COMPTE, texts.COL_CLE)
    vals = (doc.card.banque, doc.card.guichet, doc.card.compte, doc.card.cle)
    for (x0, x1), label, value in zip(layout.TABLE_COLS, heads, vals):
        fill(c, layout.LABEL_COLOR)
        draw_centered_label(
            c, x0, x1, layout.TABLE_LABEL_Y + dy, label,
            layout.FONT, layout.SIZE_FIELD,
        )
        if value:
            draw_centered_value(
                c, x0, x1, layout.TABLE_Y + dy, value,
                layout.FONT, layout.SIZE_FIELD,
            )
