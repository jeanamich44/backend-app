"""Logo LCL : PNG 172×40 du gabarit, posé 86×20."""

from .. import layout
from ..paint import draw_image


def draw(c, doc, i=0):
    if not doc.visible.header_logo:
        return
    draw_image(
        c, layout.LOGO_FILE,
        layout.LOGO_X, layout.LOGO_Y_TOP + layout.dy(i),
        layout.LOGO_W, layout.LOGO_H,
    )
