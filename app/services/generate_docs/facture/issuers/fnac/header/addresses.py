"""Encadrés Livraison / Facturation — labels 90° hors cadre, texte selon canal."""

from .. import copy as texts
from .. import flow, layout
from ..paint import clip_rect, draw_string, draw_vertical, fill


def _column(c, x, lines):
    max_w = layout.ADDR_X1 - x - 4
    for y, text, bold, size in lines:
        font = layout.FONT_BOLD if bold else layout.FONT
        fill(c, layout.COLOR)
        draw_string(c, x, y, text, font, size, max_width=max_w)


def _label(c, y0, y1, text):
    c.saveState()
    clip_rect(
        c,
        layout.ADDR_LABEL_CLIP_X0, y0,
        layout.ADDR_LABEL_CLIP_X1, y1,
    )
    fill(c, layout.COLOR)
    draw_vertical(
        c, layout.ADDR_LABEL_X, y1,
        text, layout.FONT, layout.SIZE_7,
    )
    c.restoreState()


def draw(c, doc):
    if not doc.visible.header_addresses:
        return
    fill(c, layout.COLOR)
    _label(c, layout.ADDR_LIV_Y0, layout.ADDR_LIV_Y1, texts.LIVRAISON)
    _label(c, layout.ADDR_FAC_Y0, layout.ADDR_FAC_Y1, texts.FACTURATION)
    (liv_x, liv), (fac_x, fac) = flow.address_columns(doc.card)
    _column(c, liv_x, liv)
    _column(c, fac_x, fac)
