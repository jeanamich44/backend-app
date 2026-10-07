from . import delivery, payment, rows, table, totals

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.middle:
        return
    payment.draw(c, doc)
    delivery.draw(c, doc)
    table.draw(c, doc)
    rows.draw(c, doc)
    totals.draw(c, doc)
