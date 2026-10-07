from . import legal

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.footer:
        return
    if doc.visible.footer_legal:
        legal.draw(c, doc)
