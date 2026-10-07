from . import client, contact, logo, meta

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.header:
        return
    logo.draw(c, doc)
    contact.draw(c, doc)
    client.draw(c, doc)
    meta.draw(c, doc)
