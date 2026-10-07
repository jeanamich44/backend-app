"""Numéros et dates, colonne gauche."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_refs:
        return
    card = doc.card
    fill(c, layout.COLOR)
    rows = (
        (layout.REF_Y[0], texts.INVOICE_NO_LABEL, card.num_facture),
        (layout.REF_Y[1], texts.ORDER_NO_LABEL, card.num_commande),
        (layout.DATE_Y[0], texts.INVOICE_DATE_LABEL, card.date_facture),
        (layout.DATE_Y[1], texts.SHIP_DATE_LABEL, card.date_envoi),
        (layout.DATE_Y[2], texts.DUE_DATE_LABEL, card.date_echeance),
    )
    for y, label, value in rows:
        draw_string(
            c, layout.REF_LABEL_X, y,
            label, layout.FONT_BOLD, layout.SIZE_BODY,
        )
        draw_string(
            c, layout.REF_VALUE_X, y,
            value, layout.FONT, layout.SIZE_BODY,
            max_width=layout.REF_MAX_W,
        )
