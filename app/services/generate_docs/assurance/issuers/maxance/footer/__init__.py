"""Pied de page : section 9, mentions, logos, pagination."""

from . import legal


def draw(c, doc):
    if not doc.visible.footer:
        return
    legal.draw(c, doc)
