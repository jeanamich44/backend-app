from .. import layout
from ..paint import draw_rect, draw_right, draw_string

# ----------------------------------------------------------------------


def draw(c, doc=None):
    draw_rect(c, 28.80, 616.35, 543.90, 17.76, stroke_width=layout.LINE_WIDTH_THIN)
    draw_string(c, 30.42, 629.28, "NET A PAYER AVANT IMPOT SUR LE REVENU :", layout.FONT_ARIAL_BOLD, 10.98, char_space=-0.0040, word_space=0.0130)

    draw_rect(c, 28.80, 635.85, 543.90, 13.20, stroke_width=layout.LINE_WIDTH_THIN)
    draw_string(c, 30.96, 645.10, "MONTANT NET SOCIAL :", layout.FONT_ARIAL_BOLD, 8.22, char_space=0.0050)

    if doc and getattr(doc, "calculs", None):
        calc = doc.calculs
        mns = calc.get("montant_net_social", calc.get("net_imposable", 0.0))
        draw_right(c, 569.84, 627.89, f"{calc['net_avant_impot']:.2f}", layout.FONT_HELVETICA_BOLD, 8.22)
        draw_right(c, 569.84, 645.10, f"{mns:.2f}", layout.FONT_HELVETICA_BOLD, 8.22)
