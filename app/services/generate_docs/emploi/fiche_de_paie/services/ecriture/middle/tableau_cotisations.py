from ...calculs import calculate_payroll
from .. import layout
from ..paint import draw_rect, draw_right, draw_string, stroke_line

# ----------------------------------------------------------------------


def draw(c, doc=None):
    draw_rect(c, 28.80, 257.97, 543.90, 356.82, stroke_width=layout.LINE_WIDTH_THICK)
    stroke_line(c, 28.80, 270.99, 572.70, 270.99, width=layout.LINE_WIDTH_THICK)

    stroke_line(c, 328.38, 257.97, 328.38, 614.79, width=layout.LINE_WIDTH_THICK)
    stroke_line(c, 390.60, 257.97, 390.60, 614.79, width=layout.LINE_WIDTH_THICK)
    stroke_line(c, 446.82, 257.97, 446.82, 614.79, width=layout.LINE_WIDTH_THICK)
    stroke_line(c, 505.32, 257.97, 505.32, 614.79, width=layout.LINE_WIDTH_THICK)

    draw_string(c, 31.56, 267.21, "Libellé", layout.FONT_ARIAL, 8.94)
    draw_string(c, 348.78, 267.21, "Base", layout.FONT_ARIAL, 8.94, char_space=0.0050)
    draw_string(c, 392.10, 267.21, "Taux Salarial", layout.FONT_ARIAL, 8.94, char_space=0.0050, word_space=-0.0290)
    draw_string(c, 452.22, 267.21, "Part Salarié", layout.FONT_ARIAL, 8.94, char_space=-0.0010, word_space=-0.0220)
    draw_string(c, 508.26, 267.21, "Part Employ", layout.FONT_ARIAL, 8.94, char_space=-0.0040, word_space=-0.0190)
    draw_string(c, 556.68, 267.21, "eur", layout.FONT_ARIAL, 8.94, char_space=0.0070)

    if not doc or not getattr(doc, "calculs", None):
        return

    calc = doc.calculs
    cot = calc.get("cotisations", {})

    draw_string(c, 34.32, 278.37, "SALAIRE DE BASE", layout.FONT_ARIAL_BOLD, 7.98)
    draw_right(c, 384.47, 278.37, f"{calc['heures']:.2f}", layout.FONT_ARIAL_BOLD, 7.98)
    draw_right(c, 440.69, 278.37, f"{calc['taux_horaire_base']:.3f}", layout.FONT_ARIAL_BOLD, 7.98)
    draw_right(c, 499.19, 278.37, f"{calc['salaire_base']:.2f}", layout.FONT_ARIAL_BOLD, 7.98)

    draw_string(c, 34.32, 287.55, "Prime habillage", layout.FONT_ARIAL, 7.98)
    draw_right(c, 384.47, 287.55, f"{calc['prime_habillage']:.2f}", layout.FONT_ARIAL, 7.98)
    draw_right(c, 499.19, 287.55, f"{calc['prime_habillage']:.2f}", layout.FONT_ARIAL, 7.98)

    draw_string(c, 34.32, 297.21, "SALAIRE BRUT", layout.FONT_ARIAL_BOLD, 7.98)
    draw_right(c, 384.47, 297.21, f"{calc['heures']:.2f}", layout.FONT_ARIAL_BOLD, 7.98)
    draw_right(c, 440.69, 297.21, f"{calc['taux_horaire_brut']:.3f}", layout.FONT_ARIAL_BOLD, 7.98)
    draw_right(c, 499.19, 297.21, f"{calc['salaire_brut']:.2f}", layout.FONT_ARIAL_BOLD, 7.98)

    draw_string(c, 34.32, 306.69, "Santé", layout.FONT_ARIAL_BOLD, 7.98)

    draw_string(c, 34.32, 315.87, "Sécurité Sociale - Maladie Maternité Invalidité Décès", layout.FONT_ARIAL_ITALIC, 7.98)
    draw_right(c, 384.47, 315.87, f"{calc['salaire_brut']:.2f}", layout.FONT_ARIAL_ITALIC, 7.98)
    draw_right(c, 567.42, 315.87, f"-{cot['maladie_ss_patronale']:.2f}", layout.FONT_ARIAL_ITALIC, 7.98)

    draw_string(c, 34.32, 325.29, "Complémentaire Santé", layout.FONT_ARIAL_ITALIC, 7.98)
    draw_right(c, 384.47, 325.29, f"{calc.get('base_mutuelle', 3428.00):.2f}", layout.FONT_ARIAL_ITALIC, 7.98)
    draw_right(c, 440.69, 325.29, "0.980", layout.FONT_ARIAL_ITALIC, 7.98)
    draw_right(c, 499.19, 325.29, f"-{cot['mutuelle_salariale']:.2f}", layout.FONT_ARIAL_ITALIC, 7.98)
    draw_right(c, 567.42, 325.29, f"-{cot['mutuelle_patronale']:.2f}", layout.FONT_ARIAL_ITALIC, 7.98)

    draw_string(c, 34.32, 334.95, "Accident Du Travail - Maladies Professionnelles", layout.FONT_ARIAL_BOLD, 7.98)
    draw_right(c, 384.47, 334.95, f"{calc['salaire_brut']:.2f}", layout.FONT_ARIAL_BOLD, 7.98)
    draw_right(c, 567.42, 334.95, f"-{cot['accident_travail_patronale']:.2f}", layout.FONT_ARIAL_BOLD, 7.98)

    draw_string(c, 34.32, 344.37, "Retraite", layout.FONT_ARIAL_BOLD, 7.98)

    draw_string(c, 34.32, 353.55, "Sécurité Sociale Plafonnée", layout.FONT_ARIAL_ITALIC, 7.98)
    draw_right(c, 384.47, 353.55, f"{calc['base_ss']:.2f}", layout.FONT_ARIAL_ITALIC, 7.98)
    draw_right(c, 440.69, 353.55, "6.900", layout.FONT_ARIAL_ITALIC, 7.98)
    draw_right(c, 499.19, 353.55, f"-{cot['retraite_plafonnee_salariale']:.2f}", layout.FONT_ARIAL_ITALIC, 7.98)
    draw_right(c, 567.42, 353.55, f"-{cot['retraite_plafonnee_patronale']:.2f}", layout.FONT_ARIAL_ITALIC, 7.98)

    draw_string(c, 34.32, 363.03, "Sécurité Sociale Déplafonnée", layout.FONT_ARIAL_ITALIC, 7.98)
    draw_right(c, 384.47, 363.03, f"{calc['salaire_brut']:.2f}", layout.FONT_ARIAL_ITALIC, 7.98)
    draw_right(c, 440.69, 363.03, "0.400", layout.FONT_ARIAL_ITALIC, 7.98)
    draw_right(c, 499.19, 363.03, f"-{cot['retraite_deplafonnee_salariale']:.2f}", layout.FONT_ARIAL_ITALIC, 7.98)
    draw_right(c, 567.42, 363.03, f"-{cot['retraite_deplafonnee_patronale']:.2f}", layout.FONT_ARIAL_ITALIC, 7.98)

    taux_agirc_sal_pct = calc.get("taux_agirc_sal", 0.0401) * 100.0
    draw_string(c, 34.32, 372.45, "Complémentaire Tranche 1", layout.FONT_ARIAL_ITALIC, 7.98)
    draw_right(c, 384.47, 372.45, f"{calc['base_ss']:.2f}", layout.FONT_ARIAL_ITALIC, 7.98)
    draw_right(c, 440.69, 372.45, f"{taux_agirc_sal_pct:.3f}", layout.FONT_ARIAL_ITALIC, 7.98)
    draw_right(c, 499.19, 372.45, f"-{cot['agirc_t1_salariale']:.2f}", layout.FONT_ARIAL_ITALIC, 7.98)
    draw_right(c, 567.42, 372.45, f"-{cot['agirc_t1_patronale']:.2f}", layout.FONT_ARIAL_ITALIC, 7.98)

    draw_string(c, 34.32, 382.11, "Famille", layout.FONT_ARIAL_BOLD, 7.98)
    draw_right(c, 384.47, 382.11, f"{calc['salaire_brut']:.2f}", layout.FONT_ARIAL_BOLD, 7.98)
    draw_right(c, 567.42, 382.11, f"-{cot['famille_patronale']:.2f}", layout.FONT_ARIAL_BOLD, 7.98)

    draw_string(c, 34.32, 391.53, "Assurance Chômage", layout.FONT_ARIAL_BOLD, 7.98)

    draw_string(c, 34.32, 400.71, "Chômage", layout.FONT_ARIAL_ITALIC, 7.98)
    draw_right(c, 384.47, 400.71, f"{calc['salaire_brut']:.2f}", layout.FONT_ARIAL_ITALIC, 7.98)
    draw_right(c, 567.42, 400.71, f"-{cot['chomage_patronale']:.2f}", layout.FONT_ARIAL_ITALIC, 7.98)

    draw_string(c, 34.32, 410.37, "Autres Contributions Dues Par L'Employeur", layout.FONT_ARIAL_BOLD, 7.98)
    draw_right(c, 384.47, 410.37, f"{calc['salaire_brut']:.2f}", layout.FONT_ARIAL_BOLD, 7.98)
    draw_right(c, 567.42, 410.37, f"-{cot['autres_contributions_patronale']:.2f}", layout.FONT_ARIAL_BOLD, 7.98)

    draw_string(c, 34.32, 419.85, "CSG Déductible de l'Impôt sur le Revenu", layout.FONT_ARIAL_BOLD, 7.98)
    draw_right(c, 384.47, 419.85, f"{calc['base_csg']:.2f}", layout.FONT_ARIAL_BOLD, 7.98)
    draw_right(c, 440.69, 419.85, "6.800", layout.FONT_ARIAL_BOLD, 7.98)
    draw_right(c, 499.19, 419.85, f"-{cot['csg_deductible']:.2f}", layout.FONT_ARIAL_BOLD, 7.98)

    draw_string(c, 34.32, 429.27, "CSG/CRDS non Déductible de l'Impot sur le Revenu", layout.FONT_ARIAL_BOLD, 7.98)
    draw_right(c, 384.47, 429.27, f"{calc['base_csg']:.2f}", layout.FONT_ARIAL_BOLD, 7.98)
    draw_right(c, 440.69, 429.27, "2.900", layout.FONT_ARIAL_BOLD, 7.98)
    draw_right(c, 499.19, 429.27, f"-{cot['csg_crds_non_deductible']:.2f}", layout.FONT_ARIAL_BOLD, 7.98)

    draw_string(c, 34.32, 438.69, "TOTAL RETENUES", layout.FONT_ARIAL_BOLD, 7.98)
    draw_right(c, 499.19, 438.69, f"-{calc['total_retenues_salariales']:.2f}", layout.FONT_ARIAL_BOLD, 7.98)
    draw_right(c, 567.42, 438.69, f"-{calc['total_retenues_patronales']:.2f}", layout.FONT_ARIAL_BOLD, 7.98)

    draw_string(c, 34.32, 447.87, "Réint. compl. santé net impo.", layout.FONT_ARIAL, 7.98)
    draw_right(c, 384.47, 447.87, f"{calc['reintegration_mutuelle']:.2f}", layout.FONT_ARIAL, 7.98)
    draw_right(c, 440.69, 447.87, "-100.000", layout.FONT_ARIAL, 7.98)
    draw_right(c, 499.19, 447.87, f"{calc['reintegration_mutuelle']:.2f}", layout.FONT_ARIAL, 7.98)

    draw_string(c, 34.32, 457.53, "NET IMPOSABLE", layout.FONT_ARIAL_BOLD, 7.98)
    draw_right(c, 499.19, 457.53, f"{calc['net_imposable']:.2f}", layout.FONT_ARIAL_BOLD, 7.98)

    draw_string(c, 34.32, 466.77, "PAS - BAREME METROPOLE", layout.FONT_ARIAL, 7.98)
    draw_right(c, 384.47, 466.77, f"{calc['net_imposable']:.2f}", layout.FONT_ARIAL, 7.98)
    draw_right(c, 440.69, 466.77, f"{calc['taux_pas']:.3f}", layout.FONT_ARIAL, 7.98)
    draw_right(c, 499.19, 466.77, f"-{calc['pas_montant']:.2f}", layout.FONT_ARIAL, 7.98)

    draw_string(c, 34.32, 476.19, "Remboursement frais pro.", layout.FONT_ARIAL, 7.98)
    draw_right(c, 384.47, 476.19, f"{calc['frais_professionnels']:.2f}", layout.FONT_ARIAL, 7.98)
    draw_right(c, 499.19, 476.19, f"{calc['frais_professionnels']:.2f}", layout.FONT_ARIAL, 7.98)

    draw_string(c, 34.32, 485.85, "NET A PAYER", layout.FONT_ARIAL_BOLD, 7.98)
    draw_right(c, 499.19, 485.85, f"{calc['net_a_payer']:.2f}", layout.FONT_HELVETICA_BOLD, 7.98)
