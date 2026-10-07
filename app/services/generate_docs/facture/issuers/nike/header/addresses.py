"""Commande expédiée / facture adressée, colonne droite."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_addresses:
        return
    card = doc.card
    fill(c, layout.COLOR)
    draw_string(
        c, layout.ADDR_LABEL_X, layout.SHIP_LABEL_Y[0],
        texts.ORDER_LABEL, layout.FONT_BOLD, layout.SIZE_BODY,
    )
    draw_string(
        c, layout.ADDR_LABEL_X, layout.SHIP_LABEL_Y[1],
        texts.SHIPPED_TO_LABEL, layout.FONT_BOLD, layout.SIZE_BODY,
    )
    for y, line in zip(layout.SHIP_Y, (
        card.livraison_adresse, card.livraison_cp_ville, card.livraison_pays,
    )):
        draw_string(
            c, layout.ADDR_VALUE_X, y,
            line, layout.FONT, layout.SIZE_BODY,
            max_width=layout.ADDR_MAX_W,
        )
    draw_string(
        c, layout.ADDR_LABEL_X, layout.BILL_LABEL_Y[0],
        texts.INVOICE_LABEL, layout.FONT_BOLD, layout.SIZE_BODY,
    )
    draw_string(
        c, layout.ADDR_LABEL_X, layout.BILL_LABEL_Y[1],
        texts.BILLED_TO_LABEL, layout.FONT_BOLD, layout.SIZE_BODY,
    )
    for y, line in zip(layout.BILL_Y, (
        card.nom, card.adresse, card.cp_ville, card.pays,
    )):
        draw_string(
            c, layout.ADDR_VALUE_X, y,
            line, layout.FONT, layout.SIZE_BODY,
            max_width=layout.ADDR_MAX_W,
        )
