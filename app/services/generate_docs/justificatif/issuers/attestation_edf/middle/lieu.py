"""Lieu de consommation, titulaire, n° client / compte / PDL / puissance."""

from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.middle_lieu:
        return
    card = doc.card
    fill(c, layout.COLOR)
    draw_string(
        c, layout.LIEU_ADDR_X, layout.LIEU_ADDR_Y[0],
        card.adresse, layout.FONT, layout.LIEU_ADDR_SIZE,
    )
    city = f"{card.cp} {card.ville}".strip()
    draw_string(
        c, layout.LIEU_ADDR_X, layout.LIEU_ADDR_Y[1],
        city, layout.FONT, layout.LIEU_ADDR_SIZE,
    )
    draw_string(
        c, layout.TITULAIRE_X, layout.TITULAIRE_Y,
        (card.nom or "").upper(), layout.FONT, layout.TITULAIRE_SIZE,
    )
    fill(c, layout.COLOR_BLUE)
    client = card.num_client if str(card.num_client).startswith(" ") else f" {card.num_client}"
    draw_string(
        c, layout.CLIENT_X, layout.CLIENT_Y,
        client, layout.FONT, 8.0,
    )
    fill(c, layout.COLOR)
    draw_string(
        c, layout.COMPTE_X, layout.COMPTE_Y,
        card.num_compte, layout.FONT_H, 8.0,
    )
    draw_string(
        c, layout.PDL_X, layout.PDL_Y,
        card.pdl, layout.FONT_H, 8.0,
    )
    draw_string(
        c, layout.PUIS_X, layout.PUIS_Y,
        card.puissance, layout.FONT_H, 8.0,
    )
