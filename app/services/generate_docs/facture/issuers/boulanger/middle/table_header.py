from .. import copy, layout
from ..paint import escape_pdf

# ----------------------------------------------------------------------

def is_visible(doc) -> bool:
    return bool(getattr(doc.visible, "middle_table_header", True) and getattr(doc.visible, "middle", True))

# ----------------------------------------------------------------------

def get_line(doc) -> str:
    if not is_visible(doc):
        return "() '"
    pad = " " * layout.PAD_COLUMNS
    mode = getattr(doc.card, "mode", copy.MODE_EN_LIGNE)
    if mode == copy.MODE_EN_LIGNE:
        return f"()({pad}{escape_pdf(doc.card.table_header_text)}) '"
    return f"({pad}{escape_pdf(doc.card.table_header_text)}) '"

# ----------------------------------------------------------------------

def draw(c, doc):
    pass
