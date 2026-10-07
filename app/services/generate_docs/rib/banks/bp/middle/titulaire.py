"""Titulaire : label gras + « : » + nom (texte live)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_titulaire:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.LABEL_X, layout.TITULAIRE_Y + dy,
        texts.LABEL_TITULAIRE, layout.FONT_BOLD, layout.SIZE,
    )
    nom = (doc.card.titulaire_nom or "").strip()
    text = f" : {nom}" if nom else " :"
    draw_string(
        c, layout.TITULAIRE_VAL_X, layout.TITULAIRE_Y + dy, text,
        layout.FONT, layout.SIZE, max_width=layout.MAX_LINE,
    )
