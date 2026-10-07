from . import footer, header, layout, middle, paint

# ----------------------------------------------------------------------


def draw(c, doc=None):
    if doc is None or getattr(doc, "visible", None) is None or doc.visible.header:
        header.draw(c, doc)
    if doc is None or getattr(doc, "visible", None) is None or doc.visible.middle:
        middle.draw(c, doc)
    if doc is None or getattr(doc, "visible", None) is None or doc.visible.footer:
        footer.draw(c, doc)
