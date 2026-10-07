"""Cartouches Livraison / Facturation + titulaire dummy."""

from .. import copy as texts
from .. import layout, rules
from ..chrome import vectors
from ..paint import draw_strokes, draw_string, draw_vertical, fill


def _block(c, y0, name, rue, cp, pays):
    lines = (
        rules.format_titulaire(name),
        rules.format_street(rue),
        rules.format_street(cp),
        pays or "",
    )
    for i, line in enumerate(lines):
        if not line:
            continue
        draw_string(
            c, layout.ADDR_X, y0 + i * layout.ADDR_PITCH,
            line, layout.FONT, layout.SIZE_ADDR,
            max_width=layout.ADDR_MAX_W,
        )


def draw(c, doc):
    if not doc.visible.header_addresses:
        return
    draw_strokes(c, vectors.ADDR_STROKES)
    fill(c, layout.COLOR)
    draw_vertical(
        c, layout.LABEL_V_X, layout.LABEL_SHIP_Y,
        texts.LABEL_SHIP, layout.FONT, layout.SIZE_LABEL_V,
    )
    draw_vertical(
        c, layout.LABEL_V_X, layout.LABEL_BILL_Y,
        texts.LABEL_BILL, layout.FONT, layout.SIZE_LABEL_V,
    )
    card = doc.card
    _block(
        c, layout.SHIP_Y0,
        card.livraison_nom, card.livraison_adresse,
        card.livraison_cp_ville, card.livraison_pays,
    )
    _block(
        c, layout.BILL_Y0,
        card.nom, card.adresse, card.cp_ville, card.pays,
    )
