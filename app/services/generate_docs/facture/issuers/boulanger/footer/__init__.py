from . import company, conditions, legal

# ----------------------------------------------------------------------

def is_visible(doc) -> bool:
    return bool(getattr(doc.visible, "footer", True))

# ----------------------------------------------------------------------

def get_lines(doc) -> list[str]:
    if not is_visible(doc):
        return []

    lines = []
    if conditions.is_visible(doc):
        lines.extend(conditions.get_lines(doc))
    if company.is_visible(doc):
        lines.extend(company.get_lines(doc))

    return lines

# ----------------------------------------------------------------------

def draw(c, doc):
    pass
