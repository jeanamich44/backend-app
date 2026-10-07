from . import details, table, totals

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.middle:
        return
    shift = 0.0
    if doc.visible.middle_table:
        shift = table.draw(c, doc)
    if doc.visible.middle_totals:
        totals.draw(c, doc, shift=shift)
    if doc.visible.middle_details:
        details.draw(c, doc, shift=shift)
