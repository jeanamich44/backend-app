"""Pied : site jaune, mentions légales, réf. courrier."""

from . import legal, ref, site


def draw(c, doc):
    if not doc.visible.footer:
        return
    site.draw(c, doc)
    legal.draw(c, doc)
    ref.draw(c, doc)
