"""IBAN : label centré, valeur groupée avec 7 espaces, centrée dans le volet gauche."""

from .. import copy as texts
from .. import layout
from .. import rib
from ..paint import draw_centered, draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_iban:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.IBAN_HEAD_X, layout.IBAN_HEAD_Y + dy, texts.LABEL_IBAN_HEAD,
        layout.LABEL_FONT, layout.SIZE_LABEL, max_width=layout.IBAN_HEAD_W,
    )
    x0, x1 = layout.TABLE_COLS[0][0], layout.TABLE_COLS[-1][1]
    draw_centered(
        c, x0, x1, layout.IBAN_LABEL_Y + dy, texts.LABEL_IBAN,
        layout.LABEL_FONT, layout.SIZE_LABEL,
    )
    if not doc.card.iban:
        return
    draw_centered(
        c, x0, x1, layout.IBAN_Y + dy,
        rib.format_wide(doc.card.iban, 4, layout.IBAN_GAP),
        layout.VALUE_FONT, layout.SIZE_VALUE,
    )
