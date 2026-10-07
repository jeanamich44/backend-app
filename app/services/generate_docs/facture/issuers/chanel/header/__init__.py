from . import client, contact, logo, meta

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.header:
        return
    if doc.visible.header_logo:
        logo.draw(c, doc)
    if doc.visible.header_contact:
        contact.draw(c, doc)
    if doc.visible.header_client:
        client.draw(c, doc)
    if doc.visible.header_meta:
        meta.draw(c, doc)
