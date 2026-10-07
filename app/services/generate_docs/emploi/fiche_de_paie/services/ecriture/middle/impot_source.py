from .. import layout
from ..paint import draw_centred, draw_rect, draw_right, draw_string

# ----------------------------------------------------------------------


def draw(c, doc=None):
    draw_rect(c, 28.44, 650.79, 266.34, 14.22, stroke_width=layout.LINE_WIDTH_THIN)
    draw_string(c, 123.72, 660.84, "Impôt sur le rev", layout.FONT_ARIAL_BOLD, 8.22, word_space=-0.0040)
    draw_string(c, 184.74, 660.84, "enu", layout.FONT_ARIAL_BOLD, 8.22, char_space=0.0030)

    draw_rect(c, 295.62, 650.79, 62.04, 14.22, stroke_width=layout.LINE_WIDTH_THIN)
    draw_string(c, 316.92, 660.84, "Base", layout.FONT_ARIAL_BOLD, 8.22, char_space=-0.0060)

    draw_rect(c, 358.56, 650.79, 96.90, 14.22, stroke_width=layout.LINE_WIDTH_THIN)
    draw_string(c, 362.10, 660.84, "Taux non personnalisé", layout.FONT_ARIAL_BOLD, 8.22, char_space=0.0040, word_space=-0.0070)

    draw_rect(c, 455.88, 650.79, 116.82, 14.22, stroke_width=layout.LINE_WIDTH_THIN)
    draw_string(c, 498.24, 660.84, "Montant", layout.FONT_ARIAL_BOLD, 8.22, char_space=0.0100)

    draw_rect(c, 28.44, 665.55, 266.34, 14.16, stroke_width=layout.LINE_WIDTH_THIN)
    draw_rect(c, 295.62, 665.55, 62.04, 14.16, stroke_width=layout.LINE_WIDTH_THIN)
    draw_rect(c, 358.56, 665.55, 96.90, 14.16, stroke_width=layout.LINE_WIDTH_THIN)
    draw_rect(c, 455.88, 665.55, 116.82, 14.16, stroke_width=layout.LINE_WIDTH_THIN)

    if doc and getattr(doc, "calculs", None):
        calc = doc.calculs
        draw_string(c, 109.62, 675.45, "PAS - Taux non personnalisé", layout.FONT_ARIAL, 7.98)
        draw_centred(c, 326.64, 675.45, f"{calc['net_imposable']:.2f}", layout.FONT_ARIAL, 7.98)
        draw_centred(c, 407.01, 675.45, f"{calc['taux_pas']:.2f}", layout.FONT_ARIAL, 7.98)
        draw_right(c, 571.01, 675.45, f"{calc['pas_montant']:.2f}", layout.FONT_ARIAL, 7.98)
