from .. import copy
from ..font_dior import enc_chunk
from ..layout import VENDEUR_SIZE, VENDEUR_X, VENDEUR_Y
from ..paint import draw_raw_tj, draw_string

# ----------------------------------------------------------------------

def draw(c, doc):
    text = doc.middle.vendeur
    if not text:
        return
    if text == copy.VENDEUR:
        c1 = enc_chunk("V")
        c2 = enc_chunk("endeur: Maria")
        draw_raw_tj(c, "TT0", VENDEUR_SIZE, VENDEUR_X, VENDEUR_Y, f"{c1}120.1 {c2}")
    else:
        line = f"Vendeur: {text}"
        draw_string(c, "TT0", VENDEUR_SIZE, VENDEUR_X, VENDEUR_Y, line)
