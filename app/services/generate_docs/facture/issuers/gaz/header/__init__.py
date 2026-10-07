"""Header = logo, bandeau, refs, lieu, fenêtre OCRB, code, à quoi correspond."""

from . import barcode, correspond, lieu, logo, refs, title, window


def draw(c, doc):
    if not doc.visible.header:
        return
    logo.draw(c, doc)
    title.draw(c, doc)
    refs.draw(c, doc)
    lieu.draw(c, doc)
    window.draw(c, doc)
    barcode.draw(c, doc)
    correspond.draw(c, doc)
