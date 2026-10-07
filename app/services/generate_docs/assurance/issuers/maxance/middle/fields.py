"""Sections 1–5 : valeurs variables (titres rejoués via static.spans)."""

from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    card = doc.card
    fill(c, layout.COLOR)
    draw_string(
        c, layout.EFFET_JOUR_X, layout.EFFET_Y,
        card.date_effet_jour, layout.FONT_BOLD, layout.SIZE_VALUE,
    )
    draw_string(
        c, layout.EFFET_MOIS_X, layout.EFFET_Y,
        card.date_effet_mois, layout.FONT_BOLD, layout.SIZE_VALUE,
    )
    draw_string(
        c, layout.EFFET_ANNEE_X, layout.EFFET_Y,
        card.date_effet_annee, layout.FONT_BOLD, layout.SIZE_VALUE,
    )
    draw_string(
        c, layout.CONTRAT_VALUE_X, layout.CONTRAT_VALUE_Y,
        card.num_contrat, layout.FONT, layout.SIZE_VALUE, max_width=160,
    )
    draw_string(
        c, layout.IMMAT_VALUE_X, layout.IMMAT_VALUE_Y,
        card.immatriculation, layout.FONT, layout.SIZE_VALUE, max_width=150,
    )
    draw_string(
        c, layout.LEFT_X, layout.VEHICULE_Y,
        card.vehicule, layout.FONT, layout.SIZE_VALUE, max_width=500,
    )
