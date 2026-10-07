"""Grille RIB : labels outlined + code banque, guichet, compte, clé."""

from .. import layout
from ..paint import draw_label, draw_string, fill


def draw(c, doc):
    if not doc.visible.middle_table:
        return
    draw_label(c, layout.LABEL_RIB)
    draw_label(c, layout.LABEL_BANQUE)
    draw_label(c, layout.LABEL_GUICHET)
    draw_label(c, layout.LABEL_COMPTE)
    draw_label(c, layout.LABEL_CLE)
    fill(c, layout.COLOR_TEXT)
    fields = (
        (layout.BANQUE_X, doc.card.banque, layout.BANQUE_W),
        (layout.GUICHET_X, doc.card.guichet, layout.GUICHET_W),
        (layout.COMPTE_X, doc.card.compte, layout.COMPTE_W),
        (layout.CLE_X, doc.card.cle, layout.CLE_W),
    )
    for x, text, max_w in fields:
        if text:
            draw_string(
                c, x, layout.TABLE_Y, text,
                layout.FONT, layout.FONT_SIZE,
                max_width=max_w,
            )
