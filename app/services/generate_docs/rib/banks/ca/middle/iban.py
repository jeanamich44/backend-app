"""IBAN : label à gauche, valeur à droite."""

from .. import copy as texts
from .. import layout
from ..paint import draw_right, draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_iban:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.LABEL_X, layout.IBAN_Y + dy,
        texts.LABEL_IBAN, layout.FONT_BOLD, layout.SIZE,
    )
    if doc.card.iban:
        draw_right(
            c, layout.RIGHT_X, layout.IBAN_Y + dy, doc.card.iban,
            layout.FONT, layout.SIZE, max_width=layout.IBAN_W,
        )
