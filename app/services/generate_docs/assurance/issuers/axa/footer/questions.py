from reportlab.lib.colors import HexColor

from .. import copy, layout
from ..paint import draw_static_block, draw_string

# ----------------------------------------------------------------------


def draw(c, doc):
    f = doc.footer

    if f.questions_text == copy.QUESTIONS_TEXT:
        draw_static_block(c, 8)
    else:
        c.setFillColor(HexColor(layout.COLOR_BLACK))
        draw_string(c, 52.20, 648.64, f.questions_text, layout.FONT_REGULAR, 5.88)

    if f.renvoi_l1 == copy.RENVOI_L1 and f.renvoi_l2 == copy.RENVOI_L2:
        draw_static_block(c, 13)
    else:
        c.setFillColor(HexColor(layout.COLOR_BLACK))
        draw_string(c, 52.08, 702.64, f.renvoi_l1, layout.FONT_ITALIC, 5.40)
        draw_string(c, 52.08, 709.72, f.renvoi_l2, layout.FONT_ITALIC, 5.40)
