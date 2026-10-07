"""Footer = pagination + n° RIB, une fois en bas de page."""

from . import page, rib


def draw(c, doc):
    if not doc.visible.footer:
        return
    page.draw(c, doc)
    rib.draw(c, doc)
