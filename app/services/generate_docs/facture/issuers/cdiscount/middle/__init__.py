"""Middle = produit, tableau, totaux, vendeur."""

from . import columns, heading, rows, totals, vendor


def draw(c, doc):
    if not doc.visible.middle:
        return
    heading.draw(c, doc)
    columns.draw(c, doc)
    rows.draw(c, doc)
    totals.draw(c, doc)
    vendor.draw(c, doc)
