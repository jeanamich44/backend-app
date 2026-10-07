from . import barcode, logo, sidebar

# ----------------------------------------------------------------------

def is_visible(doc) -> bool:
    if not getattr(doc.visible, "header", True):
        return False
    return bool(getattr(doc.visible, "header_lateral", getattr(doc.visible, "lateral", True)))

# ----------------------------------------------------------------------

def draw(c, doc):
    pass
