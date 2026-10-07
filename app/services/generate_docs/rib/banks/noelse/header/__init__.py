"""Header = cadre or, motif, titre IBAN, wordmark, filets de coupe."""

from .. import layout
from . import frame, logo, pattern, separator, title


def draw(c, doc):
    if not doc.visible.header:
        return
    for i, dy in enumerate(layout.CARD_OFFSETS):
        frame.draw(c, doc, dy)
        pattern.draw(c, doc, dy)
        title.draw(c, doc, i)
        logo.draw(c, doc, dy)
    separator.draw(c, doc)
