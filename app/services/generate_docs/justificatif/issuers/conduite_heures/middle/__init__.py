"""Middle = lignes de rendez-vous."""

from . import table


def draw(c, doc):
    if not doc.visible.middle:
        return
    table.draw(c, doc)
