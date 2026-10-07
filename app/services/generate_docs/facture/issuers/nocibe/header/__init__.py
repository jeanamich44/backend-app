from . import adresses, commande, logo, titre

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.header:
        return
    if doc.visible.header_logo:
        logo.draw(c, doc)
    if doc.visible.header_titre:
        titre.draw(c, doc)
    if doc.visible.header_facturation or doc.visible.header_livraison:
        adresses.draw(c, doc)
    if doc.visible.header_commande:
        commande.draw(c, doc)
