"""Ligne Banque / Agence / Compte / Clé : glyphes TJ du gabarit."""

from .. import copy as texts
from .. import glyphs
from .. import layout
from ..paint import draw_glyphs, draw_string, fill


def draw(c, doc):
    if not doc.visible.middle_table:
        return
    card = doc.card
    fill(c, layout.COLOR_GRAY)
    font, size = layout.FONT, layout.SIZE_RIB
    y = layout.RIB_Y
    if card.banque == texts.BANQUE:
        draw_glyphs(c, y, glyphs.BANQUE, font, size)
    elif card.banque:
        draw_string(c, layout.RIB_XS[0], y, f"{texts.LABEL_BANQUE} {card.banque}", font, size)
    if card.guichet == texts.GUICHET:
        draw_glyphs(c, y, glyphs.AGENCE, font, size)
    elif card.guichet:
        draw_string(c, layout.RIB_XS[1], y, f"{texts.LABEL_AGENCE} {card.guichet}", font, size)
    if card.compte:
        draw_glyphs(c, y, glyphs.COMPTE_LABEL, font, size)
        draw_string(c, glyphs.COMPTE_VALUE_X, y, card.compte, font, size)
    if card.cle:
        draw_glyphs(c, y, glyphs.CLE_LABEL, font, size)
        draw_string(
            c, glyphs.CLE_VALUE_X, y, card.cle, font, size, char_space=0.0002,
        )
