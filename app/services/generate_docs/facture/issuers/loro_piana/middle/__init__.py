"""Middle = tableau, totaux, paiement, filet bas."""

from . import columns, line, pay, rows, totals


def draw(c, doc):
    if not doc.visible.middle:
        return
    columns.draw(c, doc)
    rows.draw(c, doc)
    totals.draw(c, doc)
    pay.draw(c, doc)
    line.draw(c, doc)
