"""Middle = colonnes, lignes, TVA, totaux."""

from . import columns, rows, ship, vat


def draw(c, doc, plan):
    if not doc.visible.middle:
        return
    columns.draw(c, doc, plan)
    rows.draw(c, doc, plan)
    ship.draw(c, doc, plan)
    vat.draw(c, doc, plan)
