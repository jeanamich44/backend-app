from . import notes, sepa

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.footer:
        return
    notes.draw(c, doc)
    sepa.draw(c, doc)
