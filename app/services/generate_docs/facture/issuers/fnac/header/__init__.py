"""Header = logo, magasin/entrepôt, commande, adresses, page."""

from . import addresses, logo, order, page, store


def draw(c, doc, plan):
    if not doc.visible.header:
        return
    logo.draw(c, doc)
    store.draw(c, doc)
    order.draw(c, doc)
    addresses.draw(c, doc)
    page.draw(c, doc, plan)
