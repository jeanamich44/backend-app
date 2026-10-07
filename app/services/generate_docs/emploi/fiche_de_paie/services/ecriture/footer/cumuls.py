from .. import layout
from ..paint import draw_centred, draw_rect, draw_string

# ----------------------------------------------------------------------


def draw(c, doc=None):
    draw_rect(c, 28.44, 745.35, 311.64, 14.16, stroke_width=layout.LINE_WIDTH_THIN)
    draw_string(c, 165.06, 755.58, "CUMULS", layout.FONT_ARIAL_BOLD, 8.94, char_space=0.0120)

    draw_rect(c, 28.44, 759.69, 62.04, 14.16, stroke_width=layout.LINE_WIDTH_THIN)
    draw_string(c, 50.94, 769.68, "Brut", layout.FONT_ARIAL_BOLD, 8.22, char_space=0.0010)

    draw_rect(c, 90.66, 759.69, 62.40, 14.16, stroke_width=layout.LINE_WIDTH_THIN)
    draw_string(c, 101.70, 769.68, "Cotisation", layout.FONT_ARIAL_BOLD, 8.22, char_space=0.0060)

    draw_rect(c, 153.24, 759.69, 62.04, 14.16, stroke_width=layout.LINE_WIDTH_THIN)
    draw_string(c, 156.12, 769.68, "Net Imposable", layout.FONT_ARIAL_BOLD, 8.22, char_space=0.0040, word_space=-0.0080)

    draw_rect(c, 215.52, 759.69, 62.34, 14.16, stroke_width=layout.LINE_WIDTH_THIN)
    draw_string(c, 230.10, 769.68, "Hrs trav", layout.FONT_ARIAL_BOLD, 8.22, char_space=-0.0050, word_space=0.0020)
    draw_string(c, 260.94, 769.68, ".", layout.FONT_ARIAL_BOLD, 8.22)

    draw_rect(c, 278.04, 759.69, 62.04, 14.16, stroke_width=layout.LINE_WIDTH_THIN)
    draw_string(c, 281.16, 769.68, "Part Patronale", layout.FONT_ARIAL_BOLD, 8.22, char_space=-0.0030)

    draw_rect(c, 28.44, 774.03, 62.04, 14.16, stroke_width=layout.LINE_WIDTH_THIN)
    draw_rect(c, 90.66, 774.03, 62.40, 14.16, stroke_width=layout.LINE_WIDTH_THIN)
    draw_rect(c, 153.24, 774.03, 62.04, 14.16, stroke_width=layout.LINE_WIDTH_THIN)
    draw_rect(c, 215.52, 774.03, 62.34, 14.16, stroke_width=layout.LINE_WIDTH_THIN)
    draw_rect(c, 278.04, 774.03, 62.04, 14.16, stroke_width=layout.LINE_WIDTH_THIN)

    if doc and getattr(doc, "calculs", None):
        cum = doc.calculs.get("cumuls", {})
        draw_centred(c, 59.46, 783.99, f"{cum.get('brut', 0.0):.2f}", layout.FONT_ARIAL, 8.22)
        draw_centred(c, 121.86, 783.99, f"{cum.get('cotisations', 0.0):.2f}", layout.FONT_ARIAL, 8.22)
        draw_centred(c, 184.26, 783.99, f"{cum.get('net_imposable', 0.0):.2f}", layout.FONT_ARIAL, 8.22)
        draw_centred(c, 246.69, 783.99, f"{cum.get('heures', 0.0):.2f}", layout.FONT_ARIAL, 8.22)
        draw_centred(c, 309.06, 783.99, f"{cum.get('part_patronale', 0.0):.2f}", layout.FONT_ARIAL, 8.22)
