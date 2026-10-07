from ... import paint

# ----------------------------------------------------------------------

def is_visible(doc) -> bool:
    if not getattr(doc.visible, "header", True):
        return False
    if not getattr(doc.visible, "header_lateral", getattr(doc.visible, "lateral", True)):
        return False
    return bool(getattr(doc.visible, "header_lateral_barcode", getattr(doc.visible, "lateral_barcode", True)))

# ----------------------------------------------------------------------

def get_value(doc) -> str:
    raw = getattr(doc.card, "barcode_val", None)
    if raw:
        return str(raw).strip()
    f_num = getattr(doc.card, "facture_num", "F905FQ09058")
    clean = "".join(c for c in f_num.split("-")[0] if c.isalnum())
    return clean or "F905FQ09058"

# ----------------------------------------------------------------------

def get_stream(doc) -> bytes:
    val = get_value(doc)
    return paint.get_barcode_stream(val)

# ----------------------------------------------------------------------

def draw(c, doc):
    pass
