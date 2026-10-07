"""Header = logo, titre, identité, payé, contact, adresses, commande."""

from . import addresses, contact, continuation, identity, logo, order, pay, title


def draw(c, doc, plan):
    if not doc.visible.header:
        return
    if plan.kind != "full":
        continuation.draw(c, doc)
        return
    logo.draw(c, doc)
    title.draw(c, doc)
    identity.draw(c, doc)
    pay.draw(c, doc)
    contact.draw(c, doc)
    addresses.draw(c, doc, plan)
    order.draw(c, doc, plan)
