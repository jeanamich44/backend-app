"""Header = logo + bandeau + identité."""

from . import banner, identity, logo


def draw(c, doc):
    if not doc.visible.header:
        return
    logo.draw(c, doc)
    banner.draw(c, doc)
    identity.draw(c, doc)
