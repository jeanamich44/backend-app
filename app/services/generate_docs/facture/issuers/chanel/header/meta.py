from .. import layout, paint

# ----------------------------------------------------------------------

def draw(c, doc):
    y = layout.META_Y
    lines = [
        doc.header.date_str,
        f"Facture : {doc.header.facture_num}" if not doc.header.facture_num.startswith("Facture") else doc.header.facture_num,
        f"Caisse : {doc.header.caisse_num}" if not doc.header.caisse_num.startswith("Caisse") else doc.header.caisse_num,
        f"Folio n° : {doc.header.folio_num}" if not doc.header.folio_num.startswith("Folio") else doc.header.folio_num,
    ]
    for line in lines:
        if line:
            paint.draw_text(c, layout.META_X, y, line)
        y -= layout.META_LEADING
