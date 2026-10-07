"""Header = logo, titre, service client, adresses, refs."""

from . import addresses, logo, refs, service, title


def draw(c, doc):
    if not doc.visible.header:
        return
    logo.draw(c, doc)
    title.draw(c, doc)
    service.draw(c, doc)
    addresses.draw(c, doc)
    refs.draw(c, doc)
