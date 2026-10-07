LIMITS = {
    "store_line_1": 40,
    "store_line_2": 35,
    "client_code": 20,
    "client_name": 40,
    "client_address_1": 35,
    "client_address_2": 35,
    "client_address_3": 30,
    "date_str": 25,
    "facture_num": 20,
    "caisse_num": 20,
    "folio_num": 10,
    "accueil_text": 50,
    "col_ref_title": 20,
    "col_qte_title": 10,
    "col_pu_title": 20,
    "col_montant_title": 20,
    "article_desc": 60,
    "article_ref": 20,
    "article_qte": 10,
    "article_pu": 15,
    "max_rows": 3,
    "desc": 60,
    "ref": 20,
    "qty": 10,
    "unit_price": 15,
    "total": 15,
    "articles_count": 30,
    "total_ht": 30,
    "total_tva": 30,
    "total_ttc": 30,
    "paiement": 40,
}

# ----------------------------------------------------------------------

def public_limits() -> dict:
    return dict(LIMITS)
