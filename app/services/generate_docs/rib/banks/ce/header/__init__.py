"""Header = logo + titre + texte (chaque coupon)."""

from .. import layout
from . import logo, text, title


def draw_card(c, doc, dy=0):
    if not doc.visible.header:
        return
    logo.draw(c, doc, dy)
    title.draw(c, doc, dy)
    text.draw(c, doc, dy)


def draw(c, doc):
    for i in range(layout.CARD_COUNT):
        draw_card(c, doc, i * layout.CARD_DY)
