"""Header = logo + titre RIB, une fois par coupon."""

from .. import layout
from . import logo, title


def draw(c, doc):
    if not doc.visible.header:
        return
    for i in range(layout.CARD_COUNT):
        dy = i * layout.CARD_DY
        logo.draw(c, doc, dy)
        title.draw(c, doc, dy)
