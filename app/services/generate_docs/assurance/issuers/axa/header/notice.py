from reportlab.lib.colors import HexColor

from .. import copy, layout
from ..paint import draw_rect, draw_static_block, draw_string

# ----------------------------------------------------------------------


def draw(c, doc):
    h = doc.header

    if h.memo_title == copy.MEMO_TITLE and h.memo_conserver == copy.MEMO_CONSERVER:
        draw_static_block(c, 22)
    else:
        c.setFillColor(HexColor(layout.COLOR_BLUE_DARK))
        draw_string(c, 217.32, 226.12, h.memo_title, layout.FONT_BOLD, 8.76)
        c.setFillColor(HexColor("#333399"))
        draw_string(c, 307.68, 226.12, h.memo_conserver, layout.FONT_BOLD, 8.28)

    draw_rect(c, 51.36, 232.12, 471.00, 23.16, fill_color=layout.COLOR_BLUE_NOTICE)

    if h.notice_l1 == copy.NOTICE_L1 and h.notice_l2 == copy.NOTICE_L2:
        c.saveState()
        c.setStrokeColor(HexColor(layout.COLOR_RED_TITLE))
        c.setFillColor(HexColor(layout.COLOR_RED_TITLE))
        c.setLineWidth(0.078)
        c._code.append("2 Tr\n")
        draw_static_block(c, 25)
        draw_static_block(c, 26)
        c.restoreState()
    else:
        c.saveState()
        c.setStrokeColor(HexColor(layout.COLOR_RED_TITLE))
        c.setFillColor(HexColor(layout.COLOR_RED_TITLE))
        c.setLineWidth(0.078)
        c._code.append("2 Tr\n")
        draw_string(c, 54.84, 241.00, h.notice_l1, layout.FONT_LIGHT, 7.80)
        draw_string(c, 260.04, 251.08, h.notice_l2, layout.FONT_LIGHT, 7.80)
        c.restoreState()
