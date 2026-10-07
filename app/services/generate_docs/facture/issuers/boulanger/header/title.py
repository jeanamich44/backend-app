from .. import paint

# ----------------------------------------------------------------------

def is_visible(doc) -> bool:
    if not getattr(doc.visible, "header", True):
        return False
    return bool(getattr(doc.visible, "header_title", True))

# ----------------------------------------------------------------------

def get_line(doc) -> str:
    card = doc.card
    d_type = getattr(card, "doc_type", "FACTURE")
    f_num = getattr(card, "facture_num", "F905 FQ09058-23/002")
    f_date = getattr(card, "facture_date", "19.12.2023")
    f_time = getattr(card, "facture_time", "19:23")
    f_page = getattr(card, "facture_page", "1/1")

    t_str = f"{d_type:<19} {f_num} du {f_date} {f_time}   P   {f_page}"
    raw = f"{' ' * 37}{t_str}"
    return paint.escape_pdf(raw)

# ----------------------------------------------------------------------

def draw(c, doc):
    pass
