"""Header = bande, logo, titre, filet, date, adresse myPOS."""

from . import address, bar, date, logo, title


def draw(c, doc):
    if not doc.visible.header:
        return
    bar.draw(c, doc)
    logo.draw(c, doc)
    title.draw(c, doc)
    date.draw(c, doc)
    address.draw(c, doc)
