"""Header = logo, titre, service client, commande, adresses."""

from . import addresses, logo, order, service, title


def draw(c, doc):
    if not doc.visible.header:
        return
    logo.draw(c, doc)
    title.draw(c, doc)
    service.draw(c, doc)
    order.draw(c, doc)
    addresses.draw(c, doc)
