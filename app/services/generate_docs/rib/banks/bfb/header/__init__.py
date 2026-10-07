"""Header = logo, adresse, titre."""

from . import adresse, logo, title


def draw(c, doc):
    if not doc.visible.header:
        return
    logo.draw(c, doc)
    adresse.draw(c, doc)
    title.draw(c, doc)
