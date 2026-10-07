from reportlab.lib.colors import HexColor

from .. import copy, layout
from ..paint import draw_static_block, draw_string

# ----------------------------------------------------------------------


def draw(c, doc):
    f = doc.footer

    default_legal = (
        f.legal_l1 == copy.LEGAL_L1
        and f.legal_l2 == copy.LEGAL_L2
        and f.legal_l3 == copy.LEGAL_L3
        and f.legal_l4 == copy.LEGAL_L4
    )

    if default_legal:
        draw_static_block(c, 0)
    else:
        c.setFillColor(HexColor(layout.COLOR_BLACK))
        draw_string(c, 14.17, 800.84, f.legal_l1, layout.FONT_NARROW, 6.00)
        draw_string(c, 14.17, 808.84, f.legal_l2, layout.FONT_NARROW, 6.00)
        draw_string(c, 14.17, 816.84, f.legal_l3, layout.FONT_NARROW, 6.00)
        draw_string(c, 14.17, 824.84, f.legal_l4, layout.FONT_NARROW, 6.00)
