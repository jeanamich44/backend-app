from .. import copy
from ..font_dior import enc_chunk
from ..layout import PAGE_SIZE, PAGE_X, PAGE_Y
from ..paint import draw_raw_tj, draw_string

# ----------------------------------------------------------------------

def draw(c, doc):
    text = doc.middle.page_info
    if not text:
        return
    if text == copy.PAGE_INFO:
        c1 = enc_chunk("P")
        c2 = enc_chunk("age:  1 / 1")
        draw_raw_tj(c, "TT0", PAGE_SIZE, PAGE_X, PAGE_Y, f"{c1}28.3 {c2}")
    else:
        draw_string(c, "TT0", PAGE_SIZE, PAGE_X, PAGE_Y, text)
