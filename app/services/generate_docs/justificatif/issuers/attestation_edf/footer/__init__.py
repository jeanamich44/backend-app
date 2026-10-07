"""Pied : mentions verticales + cachet."""

from . import cachet, legal


def draw(c, doc):
    if not doc.visible.footer:
        return
    legal.draw(c, doc)
    cachet.draw(c, doc)
