"""Bloc adresse haut de page (nom + rue + ville + pays)."""

from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_adresse:
        return
    lines = (
        doc.card.titulaire_nom,
        doc.header.rue,
        doc.header.ville,
        doc.header.pays,
    )
    fill(c, layout.COLOR_TEXT)
    for y, text in zip(layout.ADDR_YS, lines):
        if text:
            draw_string(
                c, layout.ADDR_X, y, text,
                layout.FONT, layout.FONT_SIZE,
                max_width=layout.ADDR_W,
            )
