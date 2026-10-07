import tempfile
from pathlib import Path
import fitz
from . import copy as texts
from . import rules
from .data import from_payload
from .generate import generate

# ----------------------------------------------------------------------

def defaults() -> dict:
    return {
        "nom": texts.NOM,
        "prenom": texts.PRENOM,
        "adresse": texts.ADRESSE,
        "cp": texts.CP,
        "ville": texts.VILLE,
        "client_nom": texts.CLIENT_NOM,
        "client_rue": texts.ADRESSE,
        "client_cp_ville": texts.CP_VILLE,
        "client_num": texts.CLIENT_NUM,
        "client_tel": texts.CLIENT_TEL,
        "store_nom": texts.EL_STORE_NOM,
        "store_rue1": texts.EL_STORE_RUE1,
        "store_rue2": texts.EL_STORE_RUE2,
        "store_cp": "59810",
        "store_ville": "LESQUIN",
        "store_cp_ville": texts.EL_STORE_CP_VILLE,
        "store_siret": texts.EL_STORE_SIRET,
        "store_tel": texts.EL_STORE_TEL,
        "mode": "en_ligne",
        "facture_num": texts.EL_FACTURE_NUM,
        "facture_date": texts.slash_date(),
        "facture_time": "19:23",
        "barcode_val": texts.EL_BARCODE_VAL,
        "items": [
            {
                "nom": texts.EL_ARTICLE_1_NOM,
                "code": texts.EL_ARTICLE_1_CODE,
                "qte": texts.EL_ARTICLE_1_QTE,
                "pu_ttc": texts.EL_ARTICLE_1_PU_TTC,
                "total_ttc": texts.EL_ARTICLE_1_TOTAL_TTC,
                "tva_taux": texts.EL_ARTICLE_1_TVA_TAUX,
                "ecopart": texts.EL_ARTICLE_1_ECOPART,
                "garantie_reparation": texts.EL_ARTICLE_1_GARANTIE_REPARATION,
                "dispo_pieces": texts.EL_ARTICLE_1_DISPO_PIECES,
            }
        ],
        "extra_line_nom": texts.EL_EXTRA_NOM,
        "extra_line_pu_ttc": texts.EL_EXTRA_PU_TTC,
        "extra_line_total": texts.EL_EXTRA_TOTAL_TTC,
        "total_ht": texts.EL_TOTAL_HT,
        "total_ttc": texts.EL_TOTAL_TTC,
        "dont_tva": texts.EL_DONT_TVA,
        "dont_ecopart": texts.EL_DONT_ECOPART,
        "reglement_mode": texts.EL_REGLEMENT_MODE,
        "reglement_montant": texts.EL_REGLEMENT_MONTANT,
        "header": True,
        "middle": True,
        "footer": True,
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

def png_from_pdf(pdf: bytes, scale: float = 2.0) -> bytes:
    doc = fitz.open(stream=pdf, filetype="pdf")
    pix = doc[0].get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
    doc.close()
    return pix.tobytes("png")

# ----------------------------------------------------------------------

def png_bytes(payload: dict | None = None, scale: float = 2.0) -> bytes:
    return png_from_pdf(pdf_bytes(payload), scale)
