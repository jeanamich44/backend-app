"""Logo BforBank."""

from .. import layout
from ..paint import draw_logo


def draw(c, doc):
    if not doc.visible.header_logo:
        return
    draw_logo(
        c, layout.LOGO_FILE,
        layout.LOGO_X, layout.LOGO_Y_TOP,
        layout.LOGO_W, layout.LOGO_H,
    )
