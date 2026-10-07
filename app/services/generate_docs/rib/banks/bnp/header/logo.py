"""Logo BNP (les trois coupons, même dessin)."""

from .. import layout
from ..paint import draw_svg


def draw(c, doc, dy=0):
    if not doc.visible.header_logo:
        return
    draw_svg(
        c, layout.LOGO_FILE,
        layout.LOGO_X, layout.LOGO_Y_TOP + dy,
        layout.LOGO_W, layout.LOGO_H,
    )
