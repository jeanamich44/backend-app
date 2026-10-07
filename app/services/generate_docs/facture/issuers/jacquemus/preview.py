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
        "header": True,
        "header_logo": True,
        "header_contact": True,
        "header_contact_email": texts.CONTACT_EMAIL,
        "header_client": True,
        "nom": texts.NOM,
        "prenom": texts.PRENOM,
        "client_nom": texts.CLIENT_NOM,
        "client_rue": texts.CLIENT_RUE,
        "client_complement": texts.CLIENT_COMPLEMENT,
        "client_ville_cp": texts.CLIENT_VILLE_CP,
        "client_pays": texts.CLIENT_PAYS,
        "client_tel": texts.CLIENT_TEL,
        "header_val_commande": texts.VAL_COMMANDE,
        "header_val_facture": texts.VAL_FACTURE,
        "header_val_date": texts.VAL_DATE,
        "middle": True,
        "middle_payment": True,
        "val_payment": texts.VAL_PAYMENT,
        "middle_delivery": True,
        "val_delivery": texts.VAL_DELIVERY,
        "middle_table": True,
        "middle_rows": True,
        "items": [
            {
                "nom": texts.ITEM_DEFAULT_NOM,
                "ref": texts.ITEM_DEFAULT_REF,
                "couleur": texts.ITEM_DEFAULT_COULEUR,
                "taille": texts.ITEM_DEFAULT_TAILLE,
                "pays": texts.ITEM_DEFAULT_PAYS,
                "prix": texts.ITEM_DEFAULT_PRIX,
                "qte": texts.ITEM_DEFAULT_QTE,
                "sous_total": texts.ITEM_DEFAULT_PRIX,
            }
        ],
        "middle_totals": True,
        "tot_sous_total": texts.VAL_TOT_SOUS_TOTAL,
        "tot_tva": texts.VAL_TOT_TVA,
        "tot_livraison": texts.VAL_TOT_LIVRAISON,
        "tot_total": texts.VAL_TOT_TOTAL,
        "footer": True,
        "footer_legal": True,
        "footer_legal_lines": "\n".join(texts.LEGAL_LINES),
        "footer_notice": True,
        "footer_notice_lines": "\n".join(texts.EXPORTER_LINES),
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
