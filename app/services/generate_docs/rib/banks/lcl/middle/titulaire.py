"""Titulaire : libellé navy Regular + nom Bold, même ligne."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill, width


def draw(c, doc, i=0):
    if not doc.visible.middle_titulaire:
        return
    label = texts.LABEL_TITULAIRE
    fill(c, layout.NAVY)
    y = layout.TITULAIRE_Y + layout.dy(i)
    draw_string(
        c, layout.TITULAIRE_LABEL_X, y, label,
        layout.FONT, layout.TITULAIRE_SIZE,
    )
    nom = doc.card.titulaire_nom
    if not nom:
        return
    x = layout.TITULAIRE_LABEL_X + width(label, layout.FONT, layout.TITULAIRE_SIZE)
    max_w = min(layout.TITULAIRE_W, layout.BOX_OUTER[2] - layout.BEVEL_OUTER - x)
    draw_string(
        c, x, y, nom,
        layout.FONT_BOLD, layout.TITULAIRE_SIZE,
        max_width=max_w,
    )
