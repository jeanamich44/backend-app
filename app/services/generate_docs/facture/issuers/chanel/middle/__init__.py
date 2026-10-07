from . import accueil, paiement, table, totaux

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.middle:
        return
    accueil.draw(c, doc)
    table.draw(c, doc)
    totaux.draw(c, doc)
    paiement.draw(c, doc)
