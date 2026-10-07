import fitz
from . import copy
from .data import from_payload
from .generate import generate
from .rules import LIMITS

# ----------------------------------------------------------------------

def defaults() -> dict:
    return {
        "header": True,
        "header_logo": True,
        "header_contact": True,
        "store_line_1": copy.STORE_LINE_1,
        "store_line_2": copy.STORE_LINE_2,
        "header_client": True,
        "civilite": copy.CIVILITE,
        "nom": copy.NOM,
        "prenom": copy.PRENOM,
        "client_nom": copy.CLIENT_NOM,
        "client_code": copy.CLIENT_CODE,
        "client_name": copy.CLIENT_NAME,
        "client_address_1": copy.CLIENT_ADDRESS_1,
        "client_address_2": copy.CLIENT_ADDRESS_2,
        "client_address_3": copy.CLIENT_ADDRESS_3,
        "header_meta": True,
        "date_str": copy.DATE_STR,
        "facture_num": copy.FACTURE_NUM,
        "caisse_num": copy.CAISSE_NUM,
        "folio_num": copy.FOLIO_NUM,
        "middle": True,
        "middle_accueil": True,
        "accueil_text": copy.ACCUEIL_TEXT,
        "middle_table": True,
        "col_ref_title": copy.COL_REF_TITLE,
        "col_qte_title": copy.COL_QTE_TITLE,
        "col_pu_title": copy.COL_PU_TITLE,
        "col_montant_title": copy.COL_MONTANT_TITLE,
        "items": [
            {
                "desc": copy.ARTICLE_DESC,
                "ref": copy.ARTICLE_REF,
                "qty": copy.ARTICLE_QTE,
                "unit_price": copy.ARTICLE_PU,
                "total": copy.ARTICLE_MONTANT,
            }
        ],
        "article_desc": copy.ARTICLE_DESC,
        "article_ref": copy.ARTICLE_REF,
        "article_qte": copy.ARTICLE_QTE,
        "article_pu": copy.ARTICLE_PU,
        "article_montant": copy.ARTICLE_MONTANT,
        "articles_count": copy.ARTICLES_COUNT,
        "middle_totaux": True,
        "total_ht": "110,00",
        "total_tva": "22,00",
        "total_ttc": "132,00",
        "middle_paiement": True,
        "mode_paiement": "ESPECES EUROS",
        "footer": False,
        "_limits": LIMITS,
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
