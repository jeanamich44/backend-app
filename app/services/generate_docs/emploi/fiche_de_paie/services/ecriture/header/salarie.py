from .. import layout
from ..paint import draw_rect, draw_string

# ----------------------------------------------------------------------


def draw(c, doc=None):
    sal = getattr(doc, "salarie", None)
    draw_rect(c, 28.44, 147.45, 272.22, 67.92, stroke_width=layout.LINE_WIDTH_THIN)

    if sal:
        draw_string(c, 34.00, 160.89, f"Code Salarié : {sal.matricule}", layout.FONT_HELVETICA, 8.22)
        nir_val = str(sal.nir or "").replace(" ", "")
        draw_string(c, 187.00, 160.89, f"N° S.S : {nir_val}", layout.FONT_HELVETICA, 8.22)
        draw_string(c, 34.00, 171.89, f"Emploi : {sal.emploi}", layout.FONT_HELVETICA, 8.22)
        draw_string(c, 33.78, 184.26, "Qualification :", layout.FONT_ARIAL, 8.22, char_space=-0.0080, word_space=0.0040)
        draw_string(c, 90.48, 184.23, sal.qualification, layout.FONT_ARIAL, 8.22)
        draw_string(c, 33.78, 195.72, "Echelon :", layout.FONT_ARIAL, 8.22, char_space=-0.0090, word_space=0.0050)
        draw_string(c, 73.56, 195.69, sal.echelon, layout.FONT_ARIAL, 8.22)
        draw_string(c, 186.96, 195.72, "Coef :", layout.FONT_ARIAL, 8.22, char_space=-0.0050, word_space=0.0020)
        draw_string(c, 221.00, 194.89, sal.coefficient, layout.FONT_HELVETICA, 8.22)
        draw_string(c, 34.00, 204.89, f"Date d'ancienneté : {sal.date_anciennete}", layout.FONT_HELVETICA, 8.22)

        draw_string(c, 323.00, 159.89, sal.nom_complet, layout.FONT_HELVETICA_BOLD, 8.22)
        draw_string(c, 323.00, 170.89, sal.adresse, layout.FONT_HELVETICA, 8.22)
        draw_string(c, 323.00, 193.89, sal.code_postal, layout.FONT_HELVETICA, 8.22)
        draw_string(c, 374.00, 193.89, sal.ville, layout.FONT_HELVETICA, 8.22)
    else:
        draw_string(c, 34.00, 160.89, "Code Salarié :", layout.FONT_HELVETICA, 8.22)
        draw_string(c, 187.00, 160.89, "N° S.S :", layout.FONT_HELVETICA, 8.22)
        draw_string(c, 34.00, 171.89, "Emploi :", layout.FONT_HELVETICA, 8.22)
        draw_string(c, 33.78, 184.26, "Qualification :", layout.FONT_ARIAL, 8.22, char_space=-0.0080, word_space=0.0040)
        draw_string(c, 33.78, 195.72, "Echelon :", layout.FONT_ARIAL, 8.22, char_space=-0.0090, word_space=0.0050)
        draw_string(c, 186.96, 195.72, "Coef :", layout.FONT_ARIAL, 8.22, char_space=-0.0050, word_space=0.0020)
        draw_string(c, 34.00, 204.89, "Date d'ancienneté :", layout.FONT_HELVETICA, 8.22)
