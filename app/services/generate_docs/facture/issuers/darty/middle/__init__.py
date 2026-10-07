"""Middle = commande, tableau, totaux."""

from . import columns, order, rows, totals


def draw(c, doc):
    if not doc.visible.middle:
        return
    order.draw(c, doc)
    columns.draw(c, doc)
    rows.draw(c, doc)
    totals.draw(c, doc)
