"""IBAN : label Ubuntu Light, valeur Calibri groupée en nbsp."""

from .. import copy as texts
from .. import layout
from .. import rib
from ..paint import draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_iban:
        return
    fill(c, layout.LABEL_COLOR)
    draw_string(
        c, layout.IBAN_X, layout.IBAN_LABEL_Y + dy,
        texts.LABEL_IBAN, layout.LABEL_FONT, layout.LABEL_SIZE,
    )
    if not doc.card.iban:
        return
    fill(c, layout.VALUE_COLOR)
    draw_string(
        c, layout.IBAN_X, layout.IBAN_Y + dy,
        rib.format_nbsp(doc.card.iban),
        layout.FONT_IBAN, layout.IBAN_SIZE,
        max_width=layout.IBAN_W, stroke=False,
    )
