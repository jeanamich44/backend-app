"""Middle = tableau articles + totaux."""

from . import table, totals


def draw(c, doc):
    if not doc.visible.middle:
        return
    table.draw(c, doc)
    totals.draw(c, doc)
