from . import layout

# ----------------------------------------------------------------------

FIELDS = {
    "header_contact_email": {"min": 0, "max": layout.MAX_EMAIL, "charset": "text"},
    "client_nom": {"min": 0, "max": layout.MAX_CLIENT_NOM, "charset": "text"},
    "client_rue": {"min": 0, "max": layout.MAX_CLIENT_RUE, "charset": "text"},
    "client_complement": {"min": 0, "max": layout.MAX_CLIENT_COMPLEMENT, "charset": "text"},
    "client_ville_cp": {"min": 0, "max": layout.MAX_CLIENT_VILLE_CP, "charset": "text"},
    "client_pays": {"min": 0, "max": layout.MAX_CLIENT_PAYS, "charset": "text"},
    "client_tel": {"min": 0, "max": layout.MAX_CLIENT_TEL, "charset": "text"},
    "header_client_lines": {"min": 0, "max": 300, "charset": "text"},
    "header_val_commande": {"min": 0, "max": layout.MAX_COMMANDE, "charset": "text"},
    "header_val_facture": {"min": 0, "max": layout.MAX_FACTURE, "charset": "text"},
    "header_val_date": {"min": 0, "max": layout.MAX_DATE, "charset": "text"},
    "val_payment": {"min": 0, "max": 100, "charset": "text"},
    "val_delivery": {"min": 0, "max": 100, "charset": "text"},
    "tot_sous_total": {"min": 0, "max": 40, "charset": "text"},
    "tot_tva": {"min": 0, "max": 40, "charset": "text"},
    "tot_livraison": {"min": 0, "max": 40, "charset": "text"},
    "tot_total": {"min": 0, "max": 40, "charset": "text"},
    "footer_legal_lines": {"min": 0, "max": 500, "charset": "text"},
    "footer_notice_lines": {"min": 0, "max": 500, "charset": "text"},
}

# ----------------------------------------------------------------------

def apply_doc(doc):
    if doc.header.contact_email and len(doc.header.contact_email) > layout.MAX_EMAIL:
        doc.header.contact_email = doc.header.contact_email[:layout.MAX_EMAIL]
    if doc.header.client_nom and len(doc.header.client_nom) > layout.MAX_CLIENT_NOM:
        doc.header.client_nom = doc.header.client_nom[:layout.MAX_CLIENT_NOM]
    if doc.header.client_rue and len(doc.header.client_rue) > layout.MAX_CLIENT_RUE:
        doc.header.client_rue = doc.header.client_rue[:layout.MAX_CLIENT_RUE]
    if doc.header.client_complement and len(doc.header.client_complement) > layout.MAX_CLIENT_COMPLEMENT:
        doc.header.client_complement = doc.header.client_complement[:layout.MAX_CLIENT_COMPLEMENT]
    if doc.header.client_ville_cp and len(doc.header.client_ville_cp) > layout.MAX_CLIENT_VILLE_CP:
        doc.header.client_ville_cp = doc.header.client_ville_cp[:layout.MAX_CLIENT_VILLE_CP]
    if doc.header.client_pays and len(doc.header.client_pays) > layout.MAX_CLIENT_PAYS:
        doc.header.client_pays = doc.header.client_pays[:layout.MAX_CLIENT_PAYS]
    if doc.header.client_tel and len(doc.header.client_tel) > layout.MAX_CLIENT_TEL:
        doc.header.client_tel = doc.header.client_tel[:layout.MAX_CLIENT_TEL]
    if doc.header.val_commande and len(doc.header.val_commande) > layout.MAX_COMMANDE:
        doc.header.val_commande = doc.header.val_commande[:layout.MAX_COMMANDE]
    if doc.header.val_facture and len(doc.header.val_facture) > layout.MAX_FACTURE:
        doc.header.val_facture = doc.header.val_facture[:layout.MAX_FACTURE]
    if doc.header.val_date and len(doc.header.val_date) > layout.MAX_DATE:
        doc.header.val_date = doc.header.val_date[:layout.MAX_DATE]
    return doc

# ----------------------------------------------------------------------

def public_limits() -> dict:
    limits = {k: v["max"] for k, v in FIELDS.items()}
    limits["max_rows"] = layout.MAX_ROWS
    return limits

# ----------------------------------------------------------------------

def public_rules() -> list:
    return []
