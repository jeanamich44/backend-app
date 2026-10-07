"""Trois colonnes : facturation, livraison, vendeur (hauteur dynamique)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill, fill_rect


def _col(c, x, y0, values, max_width):
    y = y0
    for line in values:
        draw_string(
            c, x, y, line or "",
            layout.FONT_UNI, layout.SIZE_SMALL,
            max_width=max_width,
        )
        y += layout.COL_PITCH


def draw(c, doc, plan):
    if not doc.visible.header_addresses:
        return
    header = plan.header
    fill(c, layout.COLOR)
    uni = layout.FONT_UNI
    draw_string(
        c, layout.BILL_TITLE_X, layout.COL_TITLE_Y,
        texts.BILL_TITLE, uni, layout.SIZE_UNI_LG,
    )
    draw_string(
        c, layout.SHIP_TITLE_X, layout.COL_TITLE_Y,
        texts.SHIP_TITLE, uni, layout.SIZE_UNI_LG,
    )
    draw_string(
        c, layout.SELLER_TITLE_X, layout.COL_TITLE_Y,
        texts.SELLER_TITLE, uni, layout.SIZE_UNI_LG,
    )
    xs = layout.COL_X
    ws = layout.COL_MAX_W
    y0 = layout.COL_DATA_Y0
    _col(c, xs[0], y0, header["bill"], ws[0])
    _col(c, xs[1], y0, header["ship"], ws[1])
    _col(c, xs[2], y0, header["seller"], ws[2])
    left, right = layout.RULE_X
    fill_rect(
        c, left, layout.CONTACT_RULE_Y, right,
        layout.CONTACT_RULE_Y + layout.RULE_H, layout.COLOR_LINE,
    )
    fill_rect(
        c, left, header["addr_rule"], right,
        header["addr_rule"] + layout.RULE_H, layout.COLOR_LINE,
    )
