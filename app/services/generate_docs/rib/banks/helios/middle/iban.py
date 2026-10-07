"""IBAN : libellé gris (2× fill) + valeur fill+stroke."""

from .. import copy as texts
from .. import layout
from .. import rib
from ..paint import draw_label, draw_value, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_iban:
        return
    fill(c, layout.LABEL_COLOR)
    draw_label(
        c, layout.FIELD_X, layout.IBAN_LABEL_Y + dy, texts.LABEL_IBAN + " ",
        layout.FONT, layout.SIZE_FIELD,
    )
    draw_label(
        c, layout.IBAN_SUP_X, layout.IBAN_SUP_Y + dy, texts.SUP_IBAN,
        layout.FONT, layout.SIZE_SUP,
    )
    draw_label(
        c, layout.IBAN_COLON_X, layout.IBAN_LABEL_Y + dy, texts.COLON,
        layout.FONT, layout.SIZE_FIELD,
    )
    if not doc.card.iban:
        return
    draw_value(
        c, layout.IBAN_X, layout.IBAN_LABEL_Y + dy,
        rib.format_groups(doc.card.iban, 4),
        layout.FONT, layout.SIZE_FIELD,
        max_width=layout.IBAN_W,
    )
