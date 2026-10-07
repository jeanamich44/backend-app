from . import carte_verte, logo, notice, presomption, recipient

# ----------------------------------------------------------------------


def draw(c, doc):
    if not doc.visible.header:
        return
    if getattr(doc.visible, "header_logo", True):
        logo.draw(c, doc)
    if getattr(doc.visible, "header_recipient", True):
        recipient.draw(c, doc)
    if getattr(doc.visible, "header_carte_verte", True):
        carte_verte.draw(c, doc)
    if getattr(doc.visible, "header_notice", True):
        notice.draw(c, doc)
    if getattr(doc.visible, "header_presomption", True):
        presomption.draw(c, doc)
