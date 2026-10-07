"""Informations Client : facturation + livraison."""

from .. import copy as texts
from .. import layout, rules
from ..paint import draw_string, fill


def _block(c, x, max_w, name, rue, cp, split_nom):
    names = rules.titulaire_lines(name, split_nom)
    street_y, cp_y = rules.addr_ys(names)
    y0 = layout.ADDR_Y0
    pitch = layout.ADDR_PITCH
    for i, line in enumerate(names):
        draw_string(
            c, x, y0 + i * pitch, line,
            layout.FONT, layout.SIZE_ADDR, max_width=max_w,
        )
    if rue:
        draw_string(
            c, x, street_y, rules.format_street(rue),
            layout.FONT, layout.SIZE_ADDR, max_width=max_w,
        )
    if cp:
        draw_string(
            c, x, cp_y, rules.format_street(cp),
            layout.FONT, layout.SIZE_ADDR, max_width=max_w,
        )


def draw(c, doc):
    if not doc.visible.header_addresses:
        return
    card = doc.card
    fill(c, layout.COLOR)
    draw_string(
        c, layout.CLIENT_X, layout.CLIENT_Y,
        texts.CLIENT, layout.FONT, layout.SIZE_CLIENT,
    )
    fill(c, layout.COLOR_LABEL)
    draw_string(
        c, layout.BILL_TITLE_X, layout.ADDR_TITLE_Y,
        texts.BILL_TITLE, layout.FONT_BOLD, layout.SIZE_ADDR_TITLE,
    )
    draw_string(
        c, layout.SHIP_TITLE_X, layout.ADDR_TITLE_Y,
        texts.SHIP_TITLE, layout.FONT_BOLD, layout.SIZE_ADDR_TITLE,
    )
    fill(c, layout.COLOR_MUTED)
    _block(
        c, layout.BILL_X, layout.ADDR_MAX_W,
        card.nom, card.adresse, card.cp_ville, False,
    )
    _block(
        c, layout.SHIP_X, layout.SHIP_MAX_W,
        card.livraison_nom, card.livraison_adresse, card.livraison_cp_ville, True,
    )
