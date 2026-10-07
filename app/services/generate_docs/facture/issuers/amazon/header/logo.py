"""Logo page 1 : smile amazon.fr dans le rectangle du gabarit (89.63 ou 48 × 28.80)."""

from .. import layout, rules
from ..paint import draw_image


def draw(c, doc):
    if not doc.visible.header_logo:
        return
    if rules.sold_by_amazon(doc.card):
        draw_image(
            c, layout.LOGO_FILE,
            layout.LOGO_X, layout.LOGO_Y,
            layout.LOGO_W, layout.LOGO_H,
        )
        return
    draw_image(
        c, layout.LOGO_FILE,
        layout.LOGO_X, layout.LOGO_MKP_Y,
        layout.LOGO_P2_W, layout.LOGO_P2_H,
    )
