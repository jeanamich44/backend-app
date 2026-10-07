"""Header = filet, marque, logo, titre, émetteur, refs client."""

from . import brand, issuer, logo, refs, title


def draw(c, doc):
    if not doc.visible.header:
        return
    brand.draw(c, doc)
    logo.draw(c, doc)
    title.draw(c, doc)
    issuer.draw(c, doc)
    refs.draw(c, doc)
