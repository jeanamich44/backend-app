from .. import layout
from ..paint import draw_centred, draw_rect, draw_right, draw_string

# ----------------------------------------------------------------------


def draw(c, doc=None):
    draw_rect(c, 414.24, 693.57, 158.82, 14.16, stroke_width=layout.LINE_WIDTH_THIN)
    draw_string(c, 466.98, 703.50, "NET A", layout.FONT_ARIAL_BOLD, 7.98, word_space=0.0020)
    draw_string(c, 492.90, 703.50, "PA", layout.FONT_ARIAL_BOLD, 7.98, char_space=0.0170)
    draw_string(c, 503.76, 703.50, "YER", layout.FONT_ARIAL_BOLD, 7.98, char_space=0.0170)

    draw_rect(c, 414.24, 707.91, 158.82, 14.16, stroke_width=layout.LINE_WIDTH_THIN)

    draw_rect(c, 414.24, 740.79, 158.82, 14.16, stroke_width=layout.LINE_WIDTH_THIN)
    draw_string(c, 415.44, 751.74, "NET IMPOSA", layout.FONT_ARIAL_BOLD, 7.98, char_space=0.0020)
    draw_string(c, 464.88, 751.74, "BLE :", layout.FONT_ARIAL_BOLD, 7.98, word_space=0.0020)

    draw_rect(c, 414.24, 758.37, 158.82, 14.16, stroke_width=layout.LINE_WIDTH_THIN)
    draw_string(c, 415.26, 768.48, "Al", layout.FONT_ARIAL_BOLD, 7.98, char_space=-0.2420)
    draw_string(c, 423.00, 768.48, "lègement des cotisations :", layout.FONT_ARIAL_BOLD, 7.98, char_space=-0.0050, word_space=0.0080)

    draw_rect(c, 414.24, 774.03, 158.82, 14.16, stroke_width=layout.LINE_WIDTH_THIN)
    draw_string(c, 415.26, 784.50, "Total v", layout.FONT_ARIAL_BOLD, 7.98, char_space=-0.0080, word_space=0.0110)
    draw_string(c, 440.76, 784.50, "ersé par l'employ", layout.FONT_ARIAL_BOLD, 7.98, word_space=0.0020)
    draw_string(c, 505.92, 784.50, "eur :", layout.FONT_ARIAL_BOLD, 7.98, word_space=0.0020)

    if doc and getattr(doc, "calculs", None):
        calc = doc.calculs
        draw_centred(c, 493.65, 716.89, f"{calc['net_a_payer']:.2f}", layout.FONT_HELVETICA_BOLD, 8.22)
        draw_right(c, 571.01, 751.74, f"{calc['net_imposable']:.2f}", layout.FONT_ARIAL_BOLD, 7.98)
        draw_right(c, 571.01, 768.48, f"{calc['allegement_cotisations']:.2f}", layout.FONT_ARIAL_BOLD, 7.98)
        draw_right(c, 571.01, 784.50, f"{calc['total_verse_employeur']:.2f}", layout.FONT_ARIAL_BOLD, 7.98)
