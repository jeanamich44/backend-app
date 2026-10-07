"""Header = logo, émetteur, adresses, titre."""

from . import addresses, issuer, logo, title


def draw(c, doc):
    if not doc.visible.header:
        return
    logo.draw(c, doc)
    issuer.draw(c, doc)
    addresses.draw(c, doc)
    title.draw(c, doc)
