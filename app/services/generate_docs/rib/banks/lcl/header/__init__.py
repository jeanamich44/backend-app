"""Header = logo + titre, une fois par coupon."""

from .. import layout
from . import logo, title


def draw(c, doc):
    if not doc.visible.header:
        return
    for i in range(layout.CARD_COUNT):
        logo.draw(c, doc, i)
        title.draw(c, doc, i)
