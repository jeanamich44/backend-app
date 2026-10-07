from .. import copy
from ..font_dior import enc_chunk
from ..layout import DUPLICATA_SIZE, DUPLICATA_X, DUPLICATA_Y
from ..paint import draw_raw_tj, draw_string

# ----------------------------------------------------------------------

def draw(c, doc):
    text = doc.header.duplicata
    if not text:
        return
    if text == copy.DUPLICATA:
        c1 = enc_chunk("DUPLICA")
        c2 = enc_chunk("T")
        c3 = enc_chunk("A")
        tj_body = f"{c1}74.5 {c2}84.2 {c3}"
        draw_raw_tj(c, "TT0", DUPLICATA_SIZE, DUPLICATA_X, DUPLICATA_Y, tj_body)
    else:
        draw_string(c, "TT0", DUPLICATA_SIZE, DUPLICATA_X, DUPLICATA_Y, text)
