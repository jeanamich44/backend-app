# ----------------------------------------------------------------------

def is_visible(doc) -> bool:
    if not getattr(doc.visible, "header", True):
        return False
    if not getattr(doc.visible, "header_lateral", getattr(doc.visible, "lateral", True)):
        return False
    return bool(getattr(doc.visible, "header_lateral_sidebar", getattr(doc.visible, "lateral_sidebar", True)))

# ----------------------------------------------------------------------

def draw(c, doc):
    pass
