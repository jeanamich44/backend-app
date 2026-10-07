"""Header = logo, fenêtre adresse, titre, n° client sidebar."""

from . import client, logo, title, window


def draw(c, doc):
    if not doc.visible.header:
        return
    logo.draw(c, doc)
    window.draw(c, doc)
    title.draw(c, doc)
    client.draw(c, doc)
