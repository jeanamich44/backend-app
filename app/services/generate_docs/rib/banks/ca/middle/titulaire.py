"""Intitulé du compte : label à gauche, lignes titulaire à droite.

Le complément (raison sociale, détail…) est optionnel : s'il est vide,
rue et ville remontent, sans laisser de trou.
"""

from .. import copy as texts
from .. import layout
from ..paint import draw_right, draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_titulaire:
        return
    card = doc.card
    fill(c, layout.COLOR)
    draw_string(
        c, layout.LABEL_X, layout.TITULAIRE_Y + dy,
        texts.LABEL_TITULAIRE, layout.FONT_BOLD, layout.SIZE,
    )
    y = layout.TITULAIRE_Y
    for value in (
        card.titulaire_nom,
        card.titulaire_opt,
        card.titulaire_rue,
        card.titulaire_ville,
    ):
        if not value:
            continue
        draw_right(
            c, layout.RIGHT_X, y + dy, value,
            layout.FONT, layout.SIZE, max_width=layout.TITULAIRE_W,
        )
        y += layout.TITULAIRE_LEADING
