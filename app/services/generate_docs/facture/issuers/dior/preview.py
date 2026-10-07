import fitz
from . import copy
from .data import from_payload
from .generate import generate
from .rules import LIMITS

# ----------------------------------------------------------------------

def defaults() -> dict:
    return {
        "header": True,
        "header_bg": True,
        "header_logo": True,
        "header_duplicata": True,
        "duplicata": copy.DUPLICATA,
        "header_line": True,
        "header_contact": True,
        "contact_line_0": copy.CONTACT_LINES[0],
        "contact_line_1": copy.CONTACT_LINES[1],
        "contact_line_2": copy.CONTACT_LINES[2],
        "contact_line_3": copy.CONTACT_LINES[3],
        "contact_line_4": copy.CONTACT_LINES[4],
        "header_client": True,
        "civilite": copy.CIVILITE,
        "nom": copy.NOM,
        "prenom": copy.PRENOM,
        "client_nom": copy.CLIENT_NOM,
        "client_email": copy.CLIENT_EMAIL,
        "client_tel": copy.CLIENT_TEL,
        "header_meta": True,
        "vente_title": copy.VENTE_TITLE,
        "oper": copy.OPER,
        "trans": copy.TRANS,
        "store": copy.STORE,
        "store_num": copy.STORE_NUM,
        "date_str": copy.DATE_STR,
        "middle": True,
        "middle_page": True,
        "page_info": copy.PAGE_INFO,
        "middle_vendeur": True,
        "vendeur": copy.VENDEUR,
        "middle_articles": True,
        "items": [
            {
                "ref": copy.ARTICLE_REF,
                "desc": copy.ARTICLE_DESC,
                "qty": copy.ARTICLE_QTY,
                "unit_price": copy.ARTICLE_UNIT_PRICE,
                "total": copy.ARTICLE_TOTAL,
            }
        ],
        "article_ref": copy.ARTICLE_REF,
        "article_desc": copy.ARTICLE_DESC,
        "article_qty": copy.ARTICLE_QTY,
        "article_unit_price": copy.ARTICLE_UNIT_PRICE,
        "article_total": copy.ARTICLE_TOTAL,
        "count_label": copy.ARTICLE_COUNT,
        "total_facture": copy.TOTAL_FACTURE,
        "middle_line": True,
        "middle_totals": True,
        "middle_pay": True,
        "payment_method": copy.PAYMENT_METHOD,
        "payment_amount": copy.PAYMENT_AMOUNT,
        "rendu_amount": copy.RENDU_AMOUNT,
        "total_ht": copy.TOTAL_HT,
        "tva_product": copy.TVA_PRODUCT,
        "tva_rate": copy.TVA_RATE,
        "tva_amount": copy.TVA_AMOUNT,
        "total_ttc": copy.TOTAL_TTC,
        "middle_code": True,
        "code": copy.CODE,
        "footer": True,
        "footer_legal": True,
        "line_0": copy.LEGAL_LINE_0,
        "line_1": copy.LEGAL_LINE_1,
        "line_2": copy.LEGAL_LINE_2,
        "line_3": copy.LEGAL_LINE_3,
        "line_4": copy.LEGAL_LINE_4,
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
