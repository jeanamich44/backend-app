"""Header = logo + identité + bandeau titre."""

from . import banner, identity, logo


def draw(c, doc):
    if not doc.visible.header:
        return
    logo.draw(c, doc)
    identity.draw(c, doc)
    banner.draw(c, doc)
