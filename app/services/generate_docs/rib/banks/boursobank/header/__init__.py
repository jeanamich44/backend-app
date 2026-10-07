"""Header = logo + titre + sous-titre, une fois par coupon."""

from .. import layout
from . import logo, subtitle, title


def draw(c, doc):
    if not doc.visible.header:
        return
    for i in range(layout.CARD_COUNT):
        dy = i * layout.CARD_DY
        logo.draw(c, doc, dy)
        title.draw(c, doc, dy)
        subtitle.draw(c, doc, dy)
