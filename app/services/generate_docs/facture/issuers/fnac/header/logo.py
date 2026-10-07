"""Logo fnac.com — même XObject 120×108 sur magasin et en ligne (gabarits)."""

from .. import layout
from ..paint import draw_image


def draw(c, doc):
    if not doc.visible.header_logo:
        return
    draw_image(
        c, layout.LOGO_FILE,
        layout.LOGO_X, layout.LOGO_Y,
        layout.LOGO_W, layout.LOGO_H,
    )
