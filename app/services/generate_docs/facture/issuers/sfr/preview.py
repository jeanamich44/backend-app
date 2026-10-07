import tempfile
from pathlib import Path
import fitz
from . import copy as texts
from . import rules
from .data import from_payload
from .generate import generate

# ----------------------------------------------------------------------

def defaults(mode: str = "en_ligne") -> dict:
    return {
        "header": True,
        "header_logo": True,
        "header_service": True,
        "header_company": True,
        "header_account": True,
        "header_recipient": True,
        "middle": True,
        "middle_recap": True,
        "middle_banner": True,
        "middle_table": True,
        "footer": True,
        "footer_notes": True,
        "footer_sepa": True,
        "service_faq_url": texts.SERVICE_URL,
        "service_phone": texts.SERVICE_PHONE,
        "service_siege": texts.SERVICE_SIEGE,
        "company_name": texts.COMPANY_SERVICE,
        "company_address": texts.COMPANY_ADDRESS,
        "company_capital_rcs": texts.COMPANY_CAPITAL,
        "company_tva_ape": texts.COMPANY_TVA,
        "nom": texts.NOM,
        "prenom": texts.PRENOM,
        "client_nom": texts.CLIENT_NOM,
        "titulaire_ligne": texts.ACCOUNT_TITULAIRE_NAME,
        "num_compte_client": texts.ACCOUNT_COMPTE_NUM,
        "date_facture": "2026-09-01",
        "num_facture": "169793",
        "destinataire_nom": texts.RECIPIENT_NOM,
        "destinataire_adresse": texts.RECIPIENT_ADRESSE,
        "destinataire_cp_ville": texts.RECIPIENT_CP_VILLE,
        "montant_ht": "6.25",
        "montant_tva": "1.25",
        "taux_tva": "20.0 %",
        "total_ttc": "7.50",
        "solde_ht": "0.00",
        "solde_ttc": "0.00",
        "net_a_payer_ht": "6.25",
        "net_a_payer_ttc": "7.50",
        "items": [
            {
                "numero_ligne": texts.ITEM_NUM_LIGNE,
                "description": texts.ITEM_DESCRIPTION,
                "date": texts.ITEM_DATE,
                "montant_ttc": texts.ITEM_MONTANT_TTC,
            }
        ],
        "item_numero_ligne": texts.ITEM_NUM_LIGNE,
        "item_description": texts.ITEM_DESCRIPTION,
        "item_date": texts.ITEM_DATE,
        "item_montant_ttc": texts.ITEM_MONTANT_TTC,
        "total_facture_ht": texts.TOTAL_HT_VAL,
        "total_facture_ttc": texts.TOTAL_TTC_VAL,
        "mention_encaissement": texts.TVA_ENCAISSEMENT,
        "footer_note": texts.FOOTER_NOTE,
        "sepa_ligne1": texts.FOOTER_SEPA_L1,
        "sepa_ligne2": texts.FOOTER_SEPA_L2,
        "_limits": rules.public_limits(),
        "_rules": rules.public_rules(),
    }

# ----------------------------------------------------------------------

def pdf_bytes(payload: dict | None = None) -> bytes:
    doc = from_payload(payload)
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        path = Path(tmp.name)
    try:
        generate(doc, dest=path)
        return path.read_bytes()
    finally:
        path.unlink(missing_ok=True)

# ----------------------------------------------------------------------

def pack_pdf_bytes(payload: dict | None = None, count: int = 1) -> bytes:
    return pdf_bytes(payload)

# ----------------------------------------------------------------------

def png_from_pdf(pdf: bytes, scale: float = 2.0) -> bytes:
    doc = fitz.open(stream=pdf, filetype="pdf")
    pix = doc[0].get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
    doc.close()
    return pix.tobytes("png")

# ----------------------------------------------------------------------

def png_bytes(payload: dict | None = None, scale: float = 2.0) -> bytes:
    return png_from_pdf(pdf_bytes(payload), scale)
