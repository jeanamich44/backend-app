"""Titulaire : label + 4 lignes fixes (trou si une ligne est vide)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_titulaire:
        return
    card = doc.card
    fill(c, layout.LABEL_COLOR)
    draw_string(
        c, layout.TITULAIRE_X, layout.TITULAIRE_LABEL_Y + dy,
        texts.LABEL_TITULAIRE, layout.LABEL_FONT, layout.LABEL_SIZE,
        max_width=layout.TITULAIRE_W,
    )
    fill(c, layout.VALUE_COLOR)
    prefix = (card.titulaire_prefix or "").strip()
    nom = (card.titulaire_nom or "").strip()
    if prefix and nom:
        p_clean = prefix.rstrip(".").upper()
        nom_words = nom.split()
        first_word = nom_words[0].rstrip(".").upper() if nom_words else ""
        if first_word in {p_clean, "M", "MR", "MME", "MLLE", "MONSIEUR", "MADAME"}:
            first = nom
        else:
            first = f"{prefix} {nom}"
    else:
        first = prefix or nom
    rows = (
        first,
        card.titulaire_rue,
        card.titulaire_opt,
        card.titulaire_ville,
    )
    for i, value in enumerate(rows):
        if not value:
            continue
        draw_string(
            c, layout.TITULAIRE_X,
            layout.TITULAIRE_Y + i * layout.TITULAIRE_LEADING + dy,
            value, layout.VALUE_FONT, layout.VALUE_SIZE,
            max_width=layout.TITULAIRE_W,
        )
