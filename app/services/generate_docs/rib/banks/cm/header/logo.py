"""Logo Crédit Mutuel (assets/logos) + barre verticale (chrome/)."""

from .. import layout
from ..paint import draw_chrome, draw_image


def draw(c, doc, dy=0):
    if not doc.visible.header_logo:
        return
    draw_image(
        c, layout.LOGO_FILE,
        layout.LOGO_X, layout.LOGO_Y_TOP + dy,
        layout.LOGO_W, layout.LOGO_H,
    )
    draw_chrome(
        c, layout.STRIPE_FILE,
        layout.STRIPE_X, layout.STRIPE_Y_TOP + dy,
        layout.STRIPE_W, layout.STRIPE_H,
    )
