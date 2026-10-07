"""BIC : label Ubuntu Light, valeur Calibri compacte."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_bic:
        return
    fill(c, layout.LABEL_COLOR)
    draw_string(
        c, layout.BIC_X, layout.IBAN_LABEL_Y + dy,
        texts.LABEL_BIC, layout.LABEL_FONT, layout.LABEL_SIZE,
    )
    if not doc.card.bic:
        return
    fill(c, layout.VALUE_COLOR)
    draw_string(
        c, layout.BIC_X, layout.IBAN_Y + dy,
        doc.card.bic, layout.FONT_IBAN, layout.IBAN_SIZE,
        max_width=layout.BIC_W, stroke=False,
    )
