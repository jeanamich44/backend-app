from .. import layout
from ..paint import draw_rect, draw_string

# ----------------------------------------------------------------------


def draw(c, doc=None):
    draw_rect(c, 323.28, 51.39, 250.38, 22.20, stroke_width=layout.LINE_WIDTH_THIN)
    draw_string(c, 405.60, 65.76, "BULLETIN DE PA", layout.FONT_ARIAL_BOLD, 8.94, word_space=-0.0230)
    draw_string(c, 479.34, 65.76, "YE", layout.FONT_ARIAL_BOLD, 8.94, char_space=-0.0220)
