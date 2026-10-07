"""Ligne ZISUBILL (facture + client)."""

from .. import layout, rules
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_barcode:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.BARCODE_X, layout.BARCODE_Y,
        rules.barcode_value(doc.card), layout.FONT, layout.SIZE_BARCODE,
        max_width=layout.BARCODE_MAX_W,
    )
