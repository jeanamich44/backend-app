"""Header = logo, FACTURE/date/n°, adresses."""

from . import addresses, logo, title


def draw(c, doc):
    if not doc.visible.header:
        return
    logo.draw(c, doc)
    title.draw(c, doc)
    addresses.draw(c, doc)
