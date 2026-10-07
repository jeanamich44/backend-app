"""Header = logo, Nike.com, refs, adresses, titre Facture."""

from . import addresses, brand, logo, refs, title


def draw(c, doc):
    if not doc.visible.header:
        return
    logo.draw(c, doc)
    brand.draw(c, doc)
    refs.draw(c, doc)
    addresses.draw(c, doc)
    title.draw(c, doc)
