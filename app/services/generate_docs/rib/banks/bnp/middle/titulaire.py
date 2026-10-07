"""Titulaire : nom, rue, ville (texte live)."""

from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_titulaire:
        return
    fill(c, layout.COLOR)
    lines = (
        doc.card.titulaire_nom,
        doc.card.titulaire_rue,
        doc.card.titulaire_ville,
    )
    for y, text in zip(layout.TITULAIRE_YS, lines):
        if text:
            draw_string(
                c, layout.TITULAIRE_X, y + dy, text,
                layout.FONT_BOLD, layout.FONT_SIZE,
                max_width=layout.TITULAIRE_W,
            )
