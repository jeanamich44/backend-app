"""Middle = colonnes, lignes article, totaux."""

from . import columns, rows, totals


def draw(c, doc):
    if not doc.visible.middle:
        return
    columns.draw(c, doc)
    rows.draw(c, doc)
    totals.draw(c, doc)
