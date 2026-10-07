"""Zone compte : une carte × 2 + filet."""

from .. import layout
from . import card, separator


def draw(c, doc):
    if not doc.visible.middle:
        return
    card.draw(c, doc, dy=0)
    separator.draw(c, doc)
    card.draw(c, doc, dy=layout.CARD_DY)
