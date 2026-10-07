"""Middle = refs, tableau articles, taxes, totaux, paiement."""

from .. import layout
from . import columns, pay, refs, rows, tax, totals


def draw(c, doc):
    if not doc.visible.middle:
        return
    refs.draw(c, doc)
    if doc.visible.middle_columns or doc.visible.middle_rows:
        columns.draw_grid(c, layout.n_items(doc.card))
    columns.draw(c, doc)
    rows.draw(c, doc)
    tax.draw(c, doc)
    totals.draw(c, doc)
    pay.draw(c, doc)
