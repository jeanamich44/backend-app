"""Adresses de facturation et de livraison."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def _column(c, title_x, title_y, title, x, ys, lines, max_width):
    fill(c, layout.COLOR)
    draw_string(c, title_x, title_y, title, layout.FONT_BOLD, layout.SIZE_ADDR_TITLE)
    for y, line in zip(ys, lines):
        draw_string(c, x, y, line, layout.FONT, layout.SIZE_BODY, max_width=max_width)


def draw(c, doc):
    if not doc.visible.header_addresses:
        return
    card = doc.card
    _column(
        c, layout.BILL_TITLE_X, layout.BILL_TITLE_Y, texts.BILL_TITLE,
        layout.BILL_X, layout.BILL_Y,
        (card.nom, card.adresse, card.cp_ville, card.pays),
        layout.BILL_MAX_W,
    )
    _column(
        c, layout.SHIP_TITLE_X, layout.SHIP_TITLE_Y, texts.SHIP_TITLE,
        layout.SHIP_X, layout.SHIP_Y,
        (card.livraison_nom, card.livraison_adresse, card.livraison_cp_ville, card.livraison_pays),
        layout.SHIP_MAX_W,
    )
