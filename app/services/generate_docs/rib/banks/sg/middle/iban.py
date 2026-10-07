"""IBAN : label Bold 10.5, valeur Regular 12 groupée."""

from .. import copy as texts
from .. import layout
from .. import rib
from ..paint import draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_iban:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.LABEL_X, layout.IBAN_LABEL_Y + dy, texts.LABEL_IBAN,
        layout.FONT_BOLD, layout.SIZE_LABEL,
    )
    if not doc.card.iban:
        return
    draw_string(
        c, layout.IBAN_X, layout.IBAN_Y + dy,
        rib.format_groups(doc.card.iban, 4),
        layout.FONT, layout.SIZE_VALUE,
        max_width=layout.IBAN_W,
    )
