from . import legal, notice

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.footer:
        return
    legal.draw(c, doc)
    notice.draw(c, doc)
