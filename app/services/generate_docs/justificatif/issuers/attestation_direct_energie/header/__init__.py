"""Header = logo, fenêtre destinataire, titre + date."""

from . import logo, title, window


def draw(c, doc):
    if not doc.visible.header:
        return
    logo.draw(c, doc)
    window.draw(c, doc)
    title.draw(c, doc)
