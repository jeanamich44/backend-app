from . import bg, client, contact, duplicata, line, logo, meta

# ----------------------------------------------------------------------

def draw_bg(c, doc):
    if not doc.visible.header:
        return
    if doc.visible.header_bg:
        bg.draw(c, doc)

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.header:
        return
    if doc.visible.header_line:
        line.draw(c, doc)
    if doc.visible.header_logo:
        logo.draw(c, doc)
    if doc.visible.header_duplicata:
        duplicata.draw(c, doc)
    if doc.visible.header_contact:
        contact.draw(c, doc)
    if doc.visible.header_client:
        client.draw(c, doc)
    if doc.visible.header_meta:
        meta.draw(c, doc)
