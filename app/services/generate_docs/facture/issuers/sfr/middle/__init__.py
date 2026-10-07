from . import banner, recap, table

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.middle:
        return
    recap.draw(c, doc)
    banner.draw(c, doc)
    table.draw(c, doc)
