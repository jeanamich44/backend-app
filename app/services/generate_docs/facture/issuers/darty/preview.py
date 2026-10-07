"""Sorties debug (PNG / PDF / valeurs par défaut)."""

import tempfile
from pathlib import Path

import fitz

from . import copy as texts
from . import rules
from .data import from_payload
from .generate import generate


def defaults() -> dict:
    return {
        "nom": texts.NOM,
        "prenom": texts.PRENOM,
        "adresse": texts.ADRESSE,
        "cp_ville": texts.CP_VILLE,
        "pays": texts.PAYS,
        "livraison_nom": texts.NOM,
        "livraison_prenom": texts.PRENOM,
        "livraison_adresse": texts.ADRESSE,
        "livraison_cp_ville": texts.CP_VILLE,
        "livraison_pays": texts.PAYS,
        "num_commande": texts.NUM_COMMANDE,
        "date_commande": texts.slash_date(),
        "date_facture": texts.slash_date(),
        "payment": texts.PAYMENT,
        "items": [
            {
                "sku": texts.SKU,
                "desc": texts.DESC,
                "desc2": texts.DESC2,
                "qte": texts.QTE,
                "ht": texts.HT,
                "tva": texts.TVA,
                "date_delivrance": texts.slash_date(),
            },
        ],
        "header": True,
        "header_logo": True,
        "header_issuer": True,
        "header_addresses": True,
        "header_title": True,
        "middle": True,
        "middle_order": True,
        "middle_columns": True,
        "middle_rows": True,
        "middle_totals": True,
        "footer": True,
        "footer_page": True,
        "footer_legal": True,
        "_limits": rules.public_limits(),
        "_rules": rules.public_rules(),
    }


def pdf_bytes(payload: dict | None = None) -> bytes:
    doc = from_payload(payload)
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        path = Path(tmp.name)
    try:
        generate(doc, dest=path)
        return path.read_bytes()
    finally:
        path.unlink(missing_ok=True)


def png_from_pdf(pdf: bytes, scale: float = 2.0) -> bytes:
    doc = fitz.open(stream=pdf, filetype="pdf")
    pix = doc[0].get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
    doc.close()
    return pix.tobytes("png")


def png_bytes(payload: dict | None = None, scale: float = 2.0) -> bytes:
    return png_from_pdf(pdf_bytes(payload), scale)
