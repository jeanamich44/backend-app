"""Pied : mentions école + adresse (DejaVu + espaces Helvetica)."""

from . import legal


def draw(c, doc):
    if not doc.visible.footer:
        return
    legal.draw(c, doc)
