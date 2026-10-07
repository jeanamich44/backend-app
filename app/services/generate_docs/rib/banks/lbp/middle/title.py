"""Titre de carte, à droite du logo (les deux cartes, même texte)."""

from .. import layout
from ..paint import fill, y_up


def draw(c, doc, dy=0):
    if not doc.visible.middle_title:
        return
    text = doc.card.title
    if not text:
        return
    c.setFont(layout.BRAND_TITLE_FONT, layout.BRAND_TITLE_SIZE)
    fill(c, layout.BRAND_TITLE_COLOR)
    c.drawRightString(layout.MARGIN_RIGHT, y_up(layout.BRAND_TITLE_Y + dy), text)
