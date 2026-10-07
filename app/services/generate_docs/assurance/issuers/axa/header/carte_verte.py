from reportlab.lib.colors import HexColor

from .. import copy, layout
from ..paint import draw_rect, draw_static_block, draw_string, stroke_line, y_up

# ----------------------------------------------------------------------


def draw(c, doc):
    h = doc.header

    draw_rect(c, 153.12, 147.04, 369.24, 64.32, fill_color=layout.COLOR_GREY_RAPPEL)
    if layout.CARTE_VERTE_IMG.is_file():
        c.drawImage(str(layout.CARTE_VERTE_IMG), 55.20, y_up(144.88 + 65.40), width=89.16, height=65.40)
    stroke_line(c, 55.56, 145.84, 144.00, 210.76, width=1.44, hex_color=layout.COLOR_RED_TITLE)
    stroke_line(c, 55.56, 209.80, 143.16, 147.28, width=1.44, hex_color=layout.COLOR_RED_TITLE)

    if h.rappel_title == copy.RAPPEL_TITLE:
        draw_static_block(c, 27)
    else:
        c.setFillColor(HexColor(layout.COLOR_RED_TITLE))
        draw_string(c, 245.40, 162.04, h.rappel_title, layout.FONT_REGULAR, 7.80)

    if (
        h.rappel_l1 == copy.RAPPEL_L1
        and h.rappel_l2 == copy.RAPPEL_L2
        and h.rappel_l3 == copy.RAPPEL_L3
    ):
        draw_static_block(c, 28)
    else:
        c.setFillColor(HexColor(layout.COLOR_BLACK))
        draw_string(c, 154.56, 182.68, h.rappel_l1, layout.FONT_REGULAR, 6.84)
        draw_string(c, 154.56, 191.56, h.rappel_l2, layout.FONT_REGULAR, 6.84)
        draw_string(c, 154.56, 200.44, h.rappel_l3, layout.FONT_REGULAR, 6.84)
