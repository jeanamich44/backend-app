"""Header = bandeau, logo, titre, commande, adresses."""

from . import addresses, banner, logo, order, title


def draw(c, doc):
    if not doc.visible.header:
        return
    banner.draw(c, doc)
    logo.draw(c, doc)
    title.draw(c, doc)
    order.draw(c, doc)
    addresses.draw(c, doc)
