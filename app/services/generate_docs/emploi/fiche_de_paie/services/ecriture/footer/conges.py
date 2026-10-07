from .. import layout
from ..paint import draw_centred, draw_rect, draw_string

# ----------------------------------------------------------------------


def draw(c, doc=None):
    draw_rect(c, 56.82, 693.57, 283.26, 14.16, stroke_width=layout.LINE_WIDTH_THIN)
    draw_string(c, 77.28, 704.70, "CP N-1", layout.FONT_ARIAL, 8.22, char_space=0.0010, word_space=-0.0050)
    draw_string(c, 144.48, 704.70, "CP N", layout.FONT_ARIAL, 8.22, char_space=-0.0090, word_space=0.0050)
    draw_string(c, 250.50, 704.70, "Repos Compensateur", layout.FONT_ARIAL, 8.22, char_space=-0.0030)

    draw_rect(c, 28.44, 707.73, 28.38, 37.50, stroke_width=layout.LINE_WIDTH_THIN)
    draw_string(c, 37.56, 717.90, "Dû", layout.FONT_ARIAL, 8.22, char_space=0.0030)
    draw_string(c, 35.76, 728.94, "Pris", layout.FONT_ARIAL, 8.22, char_space=-0.0080)
    draw_string(c, 32.10, 740.04, "Reste", layout.FONT_ARIAL, 8.22, char_space=0.0040)

    draw_rect(c, 56.82, 707.73, 283.26, 37.50, stroke_width=layout.LINE_WIDTH_THIN)

    if doc and getattr(doc, "conges", None):
        cng = doc.conges
        draw_centred(c, 90.75, 717.87, f"{cng.cp_n1_du:.2f}", layout.FONT_ARIAL, 8.22)
        draw_centred(c, 154.29, 717.87, f"{cng.cp_n_du:.2f}", layout.FONT_ARIAL, 8.22)
        draw_centred(c, 290.45, 717.87, f"{cng.repos_compensateur_du:.2f}", layout.FONT_ARIAL, 8.22)

        draw_centred(c, 90.75, 728.91, f"{cng.cp_n1_pris:.2f}", layout.FONT_ARIAL, 8.22)
        draw_centred(c, 154.29, 728.91, f"{cng.cp_n_pris:.2f}", layout.FONT_ARIAL, 8.22)
        draw_centred(c, 290.45, 728.91, f"{cng.repos_compensateur_pris:.2f}", layout.FONT_ARIAL, 8.22)

        draw_centred(c, 90.75, 740.01, f"{cng.cp_n1_reste:.2f}", layout.FONT_ARIAL, 8.22)
        draw_centred(c, 154.29, 740.01, f"{cng.cp_n_reste:.2f}", layout.FONT_ARIAL, 8.22)
        draw_centred(c, 290.45, 740.01, f"{cng.repos_compensateur_reste:.2f}", layout.FONT_ARIAL, 8.22)
