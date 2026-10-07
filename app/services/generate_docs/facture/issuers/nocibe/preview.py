import fitz
from . import copy, rules
from .data import from_payload
from .generate import generate

# ----------------------------------------------------------------------

def defaults() -> dict:
    return {
        "header": True,
        "header_logo": True,
        "header_titre": True,
        "facture_num": copy.FACTURE_NUM,
        "date_emission": copy.DATE_EMISSION,
        "header_facturation": True,
        "facturation_titre": copy.TITRE_FACTURATION,
        "nom": copy.NOM,
        "prenom": copy.PRENOM,
        "client_nom": copy.CLIENT_NOM,
        "client_rue": copy.CLIENT_RUE,
        "client_ville": copy.CLIENT_VILLE,
        "client_pays": copy.CLIENT_PAYS,
        "header_livraison": True,
        "livraison_titre": copy.TITRE_LIVRAISON,
        "livraison_nom": copy.LIVRAISON_NOM,
        "livraison_rue": copy.LIVRAISON_RUE,
        "livraison_ville": copy.LIVRAISON_VILLE,
        "livraison_pays": copy.LIVRAISON_PAYS,
        "header_commande": True,
        "commande_date": copy.COMMANDE_DATE,
        "commande_mode": copy.COMMANDE_MODE,
        "commande_expedition": copy.COMMANDE_EXPEDITION,
        "commande_etat": copy.COMMANDE_ETAT,
        "middle": True,
        "middle_table": True,
        "middle_totals": True,
        "middle_details": True,
        "items": [
            {
                "ref": copy.ITEM_REF.strip(),
                "desc": copy.ITEM_DESC,
                "tva_rate": copy.ITEM_TVA_RATE,
                "qty": copy.ITEM_QTY,
                "unit_price": copy.ITEM_PRICE_BRUT,
                "remise": copy.ITEM_REMISE,
                "remise_code": copy.ITEM_REMISE_CODE,
                "net_ht": copy.ITEM_NET_HT,
            }
        ],
        "total_ht": copy.DEFAULT_TOTAL_HT,
        "total_tva": copy.DEFAULT_TOTAL_TVA,
        "total_ttc": copy.DEFAULT_TOTAL_TTC,
        "tva_rate_pct": "20.00 %",
        "tva_base_ht": copy.DEFAULT_TOTAL_HT.replace(",", "."),
        "tva_montant": copy.DEFAULT_TOTAL_TVA,
        "reglement_date": copy.DEFAULT_REGLEMENT_DATE,
        "reglement_mode": copy.DEFAULT_REGLEMENT_MODE,
        "reglement_montant": copy.DEFAULT_REGLEMENT_MONTANT,
        "_limits": rules.public_limits(),
        "_rules": rules.public_rules(),
    }

# ----------------------------------------------------------------------

build = from_payload

# ----------------------------------------------------------------------

def pdf_bytes(data: dict | None = None) -> bytes:
    doc = build(data)
    return generate(doc)

# ----------------------------------------------------------------------

def png_from_pdf(raw_pdf: bytes, scale: float = 2.5) -> bytes:
    doc = fitz.open("pdf", raw_pdf)
    page = doc[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
    return pix.tobytes("png")

# ----------------------------------------------------------------------

def png_bytes(data: dict | None = None, scale: float = 2.5) -> bytes:
    return png_from_pdf(pdf_bytes(data), scale=scale)
