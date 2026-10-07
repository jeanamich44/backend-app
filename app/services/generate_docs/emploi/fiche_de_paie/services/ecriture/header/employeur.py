from .. import layout
from ..paint import draw_rect, draw_string

# ----------------------------------------------------------------------


def draw(c, doc=None):
    emp = getattr(doc, "employeur", None)
    draw_rect(c, 28.44, 51.39, 272.22, 90.36, stroke_width=layout.LINE_WIDTH_THIN)

    if emp:
        draw_string(c, 34.00, 64.89, emp.raison_sociale, layout.FONT_HELVETICA_BOLD, 8.94)
        draw_string(c, 33.78, 76.89, emp.adresse, layout.FONT_ARIAL, 8.22)
        draw_string(c, 34.00, 97.89, emp.code_postal, layout.FONT_HELVETICA, 8.22)
        draw_string(c, 85.00, 97.89, emp.ville, layout.FONT_HELVETICA, 8.22)
        draw_string(c, 34.00, 108.89, f"Etablissement : {emp.etablissement}", layout.FONT_HELVETICA, 8.22)
        draw_string(c, 34.00, 120.89, f"SIRET : {emp.siret}", layout.FONT_HELVETICA, 8.22)
        draw_string(c, 187.08, 122.10, "NACE ", layout.FONT_ARIAL, 8.22, char_space=-0.0090, word_space=0.0050)
        draw_string(c, 221.34, 122.13, emp.code_naf, layout.FONT_ARIAL, 8.22)
    else:
        draw_string(c, 34.00, 108.89, "Etablissement :", layout.FONT_HELVETICA, 8.22)
        draw_string(c, 34.00, 120.89, "SIRET :", layout.FONT_HELVETICA, 8.22)
        draw_string(c, 187.08, 122.10, "NACE ", layout.FONT_ARIAL, 8.22, char_space=-0.0090, word_space=0.0050)
