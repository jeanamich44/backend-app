"""Header = fil d'Ariane (page) + logo + titre (chaque coupon)."""

from .. import layout
from . import crumb, logo, title


def draw(c, doc):
    if not doc.visible.header:
        return
    crumb.draw(c, doc)
    for i in range(layout.CARD_COUNT):
        dy = i * layout.CARD_DY
        logo.draw(c, doc, dy)
        title.draw(c, doc, dy)
