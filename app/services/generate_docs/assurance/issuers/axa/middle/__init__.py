from . import assureur, couverture, remorque, vehicule

# ----------------------------------------------------------------------


def draw(c, doc):
    if not doc.visible.middle:
        return
    if getattr(doc.visible, "middle_vehicule", True):
        vehicule.draw(c, doc)
    if getattr(doc.visible, "middle_remorque", True):
        remorque.draw(c, doc)
    if getattr(doc.visible, "middle_assureur", True):
        assureur.draw(c, doc)
    if getattr(doc.visible, "middle_couverture", True):
        couverture.draw(c, doc)
