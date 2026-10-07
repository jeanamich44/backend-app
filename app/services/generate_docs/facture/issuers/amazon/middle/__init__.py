"""Middle = colonnes, lignes, totaux, récap TVA."""

from . import columns, rows, totals, vat


def draw(c, doc, plan):
    if not doc.visible.middle:
        return
    columns.draw(c, doc, plan)
    bottom = rows.draw(c, doc, plan)
    after = totals.draw(c, doc, plan, bottom)
    vat.draw(c, doc, plan, after)
