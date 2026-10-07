from reportlab.lib.colors import HexColor

from .. import copy, layout
from ..paint import draw_static_block, draw_string

# ----------------------------------------------------------------------


def draw(c, doc):
    m = doc.middle

    if m.couverture_l1 == copy.COUVERTURE_L1 and m.couverture_l2 == copy.COUVERTURE_L2:
        draw_static_block(c, 15)
    else:
        c.setFillColor(HexColor(layout.COLOR_BLACK))
        draw_string(c, 52.20, 467.68, m.couverture_l1, layout.FONT_REGULAR, 5.88)
        draw_string(c, 52.20, 475.36, m.couverture_l2, layout.FONT_REGULAR, 5.88)
