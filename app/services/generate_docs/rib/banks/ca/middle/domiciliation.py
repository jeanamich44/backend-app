"""Domiciliation : label gras ; valeur live à droite si renseignée."""

from .. import copy as texts
from .. import layout
from ..paint import draw_right, draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_domiciliation:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.LABEL_X, layout.DOM_Y + dy,
        texts.LABEL_DOM, layout.FONT_BOLD, layout.SIZE,
    )
    if doc.card.domiciliation:
        draw_right(
            c, layout.RIGHT_X, layout.DOM_Y + dy, doc.card.domiciliation,
            layout.FONT, layout.SIZE, max_width=layout.TITULAIRE_W,
        )
