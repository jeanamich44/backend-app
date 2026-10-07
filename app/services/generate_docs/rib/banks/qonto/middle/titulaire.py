"""Titulaire : label Bold 8.25, 3 lignes Regular 9, domiciliation Regular 6."""

from .. import copy as texts
from .. import glyphs
from .. import layout
from ..paint import draw_glyphs, draw_string, fill


def draw(c, doc):
    if not doc.visible.middle_titulaire:
        return
    fill(c, layout.COLOR_MUTED)
    if texts.LABEL_TITULAIRE == "Titulaire":
        draw_glyphs(
            c, layout.TITULAIRE_LABEL_Y, glyphs.TITULAIRE,
            layout.FONT_BOLD, layout.SIZE_LABEL,
        )
    elif texts.LABEL_TITULAIRE:
        draw_string(
            c, layout.LEFT_X, layout.TITULAIRE_LABEL_Y, texts.LABEL_TITULAIRE,
            layout.FONT_BOLD, layout.SIZE_LABEL,
        )
    fill(c, layout.COLOR)
    lines = (
        doc.card.titulaire_nom,
        doc.card.titulaire_rue,
        doc.card.titulaire_ville,
    )
    for y, text in zip(layout.TITULAIRE_YS, lines):
        if not text:
            continue
        draw_string(
            c, layout.LEFT_X, y, text,
            layout.FONT, layout.SIZE_TITULAIRE,
            max_width=layout.TITULAIRE_W,
        )
    fill(c, layout.COLOR_MUTED)
    if texts.DOMICILIATION.startswith("Domiciliation: Qonto"):
        draw_glyphs(
            c, layout.DOMICILE_Y, glyphs.DOMICILE,
            layout.FONT, layout.SIZE_DOMICILE,
        )
    else:
        draw_string(
            c, layout.LEFT_X, layout.DOMICILE_Y, texts.DOMICILIATION,
            layout.FONT, layout.SIZE_DOMICILE,
            max_width=layout.DOMICILE_W,
        )
