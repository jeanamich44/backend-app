"""Header = logo, boutique, Reçu, refs ticket."""

from . import logo, refs, store, title


def draw(c, doc):
    if not doc.visible.header:
        return
    logo.draw(c, doc)
    store.draw(c, doc)
    title.draw(c, doc)
    refs.draw(c, doc)
