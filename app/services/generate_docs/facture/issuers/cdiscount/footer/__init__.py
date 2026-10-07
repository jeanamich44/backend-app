"""Footer = note (off), CGU, mentions."""

from . import cgu, legal, note


def draw(c, doc):
    if not doc.visible.footer:
        return
    note.draw(c, doc)
    cgu.draw(c, doc)
    legal.draw(c, doc)
