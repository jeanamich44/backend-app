"""IBAN : label + valeur (texte live)."""

from .. import copy as texts
from .. import layout
from .. import rib
from ..paint import draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_iban:
        return
    fill(c, layout.LABEL_COLOR)
    draw_string(
        c, layout.RIGHT_X, layout.LABEL_IBAN_Y + dy,
        texts.LABEL_IBAN, layout.LABEL_FONT, layout.LABEL_SIZE,
    )
    value = rib.format_groups(doc.card.iban, 4) if doc.card.iban else ""
    if value:
        fill(c, layout.VALUE_COLOR)
        draw_string(
            c, layout.RIGHT_X, layout.IBAN_Y + dy, value,
            layout.VALUE_FONT, layout.VALUE_SIZE,
            max_width=layout.RIGHT_W,
        )
