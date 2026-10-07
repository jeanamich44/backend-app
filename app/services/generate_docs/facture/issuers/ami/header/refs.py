"""Adresse client, date, n° facture + chrome PO / envoi."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_refs:
        return
    card = doc.card
    fill(c, layout.COLOR)
    font = layout.FONT
    size = layout.SIZE_BODY
    max_w = layout.REF_MAX_W
    draw_string(c, layout.REF_ADDR_X, layout.REF_ADDR_Y, card.adresse, font, size, max_w)
    draw_string(c, layout.REF_CP_X, layout.REF_CP_Y, card.cp, font, size, max_w)
    draw_string(
        c, layout.REF_DATE_X, layout.REF_DATE_Y,
        texts.DATE_PREFIX + (card.date_facture or ""), font, size, max_w,
    )
    draw_string(c, layout.REF_PO_X, layout.REF_PO_Y, texts.PO_LINE, font, size, max_w)
    draw_string(
        c, layout.REF_INV_X, layout.REF_INV_Y,
        texts.INVOICE_PREFIX + (card.num_facture or ""), font, size, max_w,
    )
    draw_string(c, layout.REF_SHIP_X, layout.REF_SHIP_Y, texts.SHIP_LINE, font, size, max_w)
