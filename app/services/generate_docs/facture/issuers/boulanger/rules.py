from .data import FactureBoulanger

# ----------------------------------------------------------------------

LIMITS = {
    "mode": 10,
    "seller_type": 15,
    "doc_type": 20,
    "facture_num": 30,
    "facture_date": 12,
    "facture_time": 10,
    "facture_page": 10,
    "store_nom": 40,
    "store_rue1": 40,
    "store_rue2": 40,
    "store_lieu": 40,
    "store_cp_ville": 40,
    "store_siret": 40,
    "store_tel": 20,
    "seller_name": 40,
    "seller_rue": 40,
    "seller_cp_ville": 40,
    "seller_siret": 30,
    "seller_tva": 30,
    "seller_capital": 30,
    "seller_rcs": 40,
    "client_nom": 40,
    "client_rue": 40,
    "client_cp_ville": 40,
    "client_tel": 20,
    "client_num": 20,
    "barcode_val": 30,
    "table_header_text": 85,
    "extra_line_nom": 38,
    "extra_line_code": 10,
    "extra_line_qte": 5,
    "extra_line_pu_ttc": 10,
    "extra_line_tva": 7,
    "extra_line_total": 10,
    "club_nom": 38,
    "club_code": 10,
    "club_qte": 5,
    "club_pu_ttc": 10,
    "club_tva_taux": 7,
    "club_total_ttc": 10,
    "total_ht": 10,
    "total_ttc": 10,
    "dont_tva": 10,
    "dont_tva_taux": 6,
    "dont_ecopart": 10,
    "reglement_mode": 30,
    "reglement_montant": 10,
    "notice_cumul": 60,
    "notice_merci": 40,
    "notice_garantie_1": 45,
    "notice_garantie_2": 45,
    "notice_garantie_3": 40,
    "conditions_type": 15,
    "usage_pro": 10,
    "livraison": 10,
    "mise_en_service": 10,
    "company_nom": 40,
    "company_capital": 40,
    "company_rue": 40,
    "company_rcs": 40,
    "company_cp_ville": 40,
    "company_tva": 40,
    "company_ape": 20,
    "item_nom": 38,
    "item_code": 10,
    "item_qte": 5,
    "item_pu_ttc": 10,
    "item_tva_taux": 7,
    "item_total_ttc": 10,
    "item_ecopart": 10,
    "item_garantie_non_retenue": 45,
    "item_garantie_reparation": 45,
    "item_dispo_pieces_label": 60,
    "item_dispo_pieces": 30,
    "item_vendeur": 40,
}

# ----------------------------------------------------------------------

def public_limits() -> dict:
    return dict(LIMITS)

# ----------------------------------------------------------------------

def public_rules() -> dict:
    return {
        "max_items": 3,
        "min_items": 1,
    }

# ----------------------------------------------------------------------

def apply_doc(doc: FactureBoulanger) -> FactureBoulanger:
    from . import copy
    if doc.card.mode == copy.MODE_MAGASIN and doc.card.seller_type == copy.SELLER_TIERS:
        doc.card.seller_type = copy.SELLER_BOULANGER

    for k, max_len in LIMITS.items():
        if hasattr(doc.card, k):
            val = getattr(doc.card, k, None)
            if isinstance(val, str) and len(val) > max_len:
                setattr(doc.card, k, val[:max_len])

    if not doc.card.items:
        from .data import default_items
        doc.card.items = default_items(doc.card.mode)
    elif len(doc.card.items) > 3:
        doc.card.items = doc.card.items[:3]

    item_limits = {
        "nom": LIMITS["item_nom"],
        "code": LIMITS["item_code"],
        "qte": LIMITS["item_qte"],
        "pu_ttc": LIMITS["item_pu_ttc"],
        "tva_taux": LIMITS["item_tva_taux"],
        "total_ttc": LIMITS["item_total_ttc"],
        "ecopart": LIMITS["item_ecopart"],
        "garantie_non_retenue": LIMITS["item_garantie_non_retenue"],
        "garantie_reparation": LIMITS["item_garantie_reparation"],
        "dispo_pieces_label": LIMITS["item_dispo_pieces_label"],
        "dispo_pieces": LIMITS["item_dispo_pieces"],
        "vendeur": LIMITS["item_vendeur"],
    }

    for itm in doc.card.items:
        for attr, mlen in item_limits.items():
            if hasattr(itm, attr):
                v = getattr(itm, attr, None)
                if isinstance(v, str) and len(v) > mlen:
                    setattr(itm, attr, v[:mlen])

    return doc
