from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth

from .. import copy, layout
from ..paint import draw_rect, draw_static_block, draw_string

# ----------------------------------------------------------------------


def draw(c, doc):
    h = doc.header

    if h.presomption_souligne == copy.PRESOMPTION_SOULIGNE and h.presomption_valable == copy.PRESOMPTION_VALABLE:
        draw_static_block(c, 21)
        draw_rect(c, 52.20, 267.04, 278.28, 0.36, fill_color=layout.COLOR_BLUE_DARK)
    else:
        c.setFillColor(HexColor(layout.COLOR_BLUE_DARK))
        draw_string(c, 52.20, 266.32, h.presomption_souligne, layout.FONT_REGULAR, 5.88)
        w_line = stringWidth(h.presomption_souligne, layout.FONT_REGULAR, 5.88)
        draw_rect(c, 52.20, 267.04, w_line, 0.36, fill_color=layout.COLOR_BLUE_DARK)
        c.setFillColor(HexColor(layout.COLOR_BLACK))
        lines = h.presomption_valable.split("\n")
        if len(lines) == 1 and stringWidth(lines[0], layout.FONT_REGULAR, 5.88) > 470.0:
            words = lines[0].split(" ")
            mid = len(words) // 2
            lines = [" ".join(words[:mid]), " ".join(words[mid:])]
        for i, l in enumerate(lines):
            draw_string(c, 52.20, 274.36 + i * 7.68, l, layout.FONT_REGULAR, 5.88)

    if h.obligation_fva_l1 == copy.OBLIGATION_FVA_L1 and h.obligation_fva_l2 == copy.OBLIGATION_FVA_L2:
        draw_static_block(c, 24)
    else:
        c.setFillColor(HexColor(layout.COLOR_BLACK))
        draw_string(c, 52.20, 301.12, h.obligation_fva_l1, layout.FONT_REGULAR, 5.88)
        draw_string(c, 52.20, 308.80, h.obligation_fva_l2, layout.FONT_REGULAR, 5.88)

    if h.politesse == copy.POLITESSE:
        draw_static_block(c, 23)
    else:
        c.setFillColor(HexColor(layout.COLOR_BLACK))
        draw_string(c, 52.20, 320.32, h.politesse, layout.FONT_REGULAR, 5.88)
