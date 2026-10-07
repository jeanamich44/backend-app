"""IBAN : label outlined + valeur."""

from .. import layout
from ..paint import draw_label, draw_string, fill


def draw(c, doc):
    if not doc.visible.middle_iban:
        return
    draw_label(c, layout.LABEL_IBAN)
    text = doc.card.iban
    if text:
        fill(c, layout.COLOR_TEXT)
        draw_string(
            c, layout.IBAN_X, layout.IBAN_Y, text,
            layout.FONT, layout.FONT_SIZE,
            max_width=layout.IBAN_W,
        )
