from .. import layout
from ..paint import draw_rect, draw_string

# ----------------------------------------------------------------------


def draw(c, doc=None):
    per = getattr(doc, "periode", None)
    draw_rect(c, 323.28, 96.63, 250.38, 45.12, stroke_width=layout.LINE_WIDTH_THIN)

    if per:
        draw_string(c, 329.00, 108.89, f"Période de paie du {per.date_debut} au {per.date_fin}", layout.FONT_HELVETICA, 8.22)
        draw_string(c, 328.68, 122.16, "Paiement :", layout.FONT_ARIAL, 8.22, char_space=-0.0130, word_space=0.0090)
        mode_str = per.mode_paiement or ""
        if mode_str.lower().startswith("par "):
            mode_str = mode_str[4:]
        draw_string(c, 373.92, 122.16, "Par", layout.FONT_ARIAL, 8.22)
        draw_string(c, 391.38, 122.16, mode_str, layout.FONT_ARIAL, 8.22)
        draw_string(c, 442.00, 122.16, per.date_paiement, layout.FONT_HELVETICA, 8.22)
        val_plafond = float(per.plafond_mensuel_ss) if per.plafond_mensuel_ss is not None else 3864.0
        draw_string(c, 329.00, 132.89, f"Plafond du mois : {val_plafond:.2f}", layout.FONT_HELVETICA, 8.22)
    else:
        draw_string(c, 329.00, 108.89, "Période de paie du", layout.FONT_HELVETICA, 8.22)
        draw_string(c, 328.68, 122.16, "Paiement :", layout.FONT_ARIAL, 8.22, char_space=-0.0130, word_space=0.0090)
        draw_string(c, 329.00, 132.89, "Plafond du mois :", layout.FONT_HELVETICA, 8.22)

