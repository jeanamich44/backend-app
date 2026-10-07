# ----------------------------------------------------------------------

def is_visible(doc) -> bool:
    if not getattr(doc.visible, "header", True):
        return False
    if not getattr(doc.visible, "header_lateral", getattr(doc.visible, "lateral", True)):
        return False
    return bool(getattr(doc.visible, "header_lateral_logo", getattr(doc.visible, "lateral_logo", True)))

# ----------------------------------------------------------------------

def draw(c, doc):
    pass
