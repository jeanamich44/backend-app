"""En-tête de continuation (page 2+) : logo 48×28.80, titre, n° facture."""

from .. import copy as texts
from .. import layout
from ..paint import draw_image, draw_string, fill, width


def draw(c, doc):
    vis = doc.visible
    if vis.header_logo:
        draw_image(
            c, layout.LOGO_FILE,
            layout.LOGO_X, layout.LOGO_P2_Y,
            layout.LOGO_P2_W, layout.LOGO_P2_H,
        )
    fill(c, layout.COLOR)
    if vis.header_title:
        draw_string(
            c, layout.TITLE_P2_X, layout.TITLE_P2_Y,
            texts.TITLE, layout.FONT_UNI, layout.SIZE_TITLE,
        )
    if vis.header_title or vis.header_pay:
        inv_text = texts.PAY_INV_CONT + (doc.card.num_facture or "")
        inv_w = width(inv_text, layout.FONT_UNI, layout.SIZE_SMALL)
        inv_x = min(layout.INV_P2_X, layout.RULE_X[1] - inv_w)
        draw_string(
            c, inv_x, layout.INV_P2_Y,
            inv_text,
            layout.FONT_UNI, layout.SIZE_SMALL,
            max_width=240,
        )
