# ----------------------------------------------------------------------

def is_visible(doc) -> bool:
    return bool(getattr(doc.visible, "footer_legal", True) and getattr(doc.visible, "footer", True))

# ----------------------------------------------------------------------

def draw(c, doc):
    pass
