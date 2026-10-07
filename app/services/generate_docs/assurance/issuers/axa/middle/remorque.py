from reportlab.lib.colors import HexColor

from .. import copy, layout
from ..paint import draw_static_block, draw_string

# ----------------------------------------------------------------------


def draw(c, doc):
    m = doc.middle

    if (
        m.remorque_title == copy.REMORQUE_TITLE
        and m.remorque_l1 == copy.REMORQUE_L1
        and m.remorque_l2 == copy.REMORQUE_L2
    ):
        draw_static_block(c, 19)
        draw_static_block(c, 3)
    else:
        c.setFillColor(HexColor(layout.COLOR_BLACK))
        draw_string(c, 79.92, 398.56, m.remorque_title, layout.FONT_BOLD, 5.88)
        draw_string(c, 170.64, 391.60, m.remorque_l1, layout.FONT_REGULAR, 5.88)
        draw_string(c, 170.64, 406.96, m.remorque_l2, layout.FONT_REGULAR, 5.88)
