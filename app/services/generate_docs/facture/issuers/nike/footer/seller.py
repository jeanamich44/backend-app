"""Émetteur + n° TVA."""

from .. import layout
from ..paint import draw_kerned, fill


def draw(c, doc):
    if not doc.visible.footer_seller:
        return
    card = doc.card
    fill(c, layout.COLOR)
    draw_kerned(
        c, layout.FOOTER_X, layout.SELLER_Y,
        card.seller, layout.FONT, layout.SIZE_BODY,
        max_width=layout.FOOTER_MAX_W,
    )
    draw_kerned(
        c, layout.FOOTER_X, layout.VAT_Y,
        card.vat, layout.FONT, layout.SIZE_BODY,
        max_width=layout.FOOTER_MAX_W,
    )
