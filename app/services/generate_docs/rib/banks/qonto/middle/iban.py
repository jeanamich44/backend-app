"""IBAN : label Bold 8.25 #999896, valeur Regular 10.5."""

from .. import copy as texts
from .. import layout
from .. import rib
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.middle_iban:
        return
    fill(c, layout.COLOR_MUTED)
    draw_string(
        c, layout.LEFT_X, layout.IBAN_LABEL_Y, texts.LABEL_IBAN,
        layout.FONT_BOLD, layout.SIZE_LABEL,
        char_space=-0.0002,
    )
    if not doc.card.iban:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.LEFT_X, layout.IBAN_VALUE_Y,
        rib.format_groups(doc.card.iban, 4),
        layout.FONT, layout.SIZE_VALUE,
        max_width=layout.IBAN_W,
        char_space=-0.0002,
    )
