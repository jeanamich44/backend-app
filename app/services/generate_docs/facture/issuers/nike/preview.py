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
        "client_nom": texts.CLIENT_NOM,
        "adresse": texts.ADRESSE,
        "cp_ville": texts.CP_VILLE,
        "pays": texts.PAYS,
        "livraison_adresse": texts.LIVRAISON_ADRESSE,
        "livraison_cp_ville": texts.LIVRAISON_CP_VILLE,
        "livraison_pays": texts.LIVRAISON_PAYS,
        "num_commande": texts.NUM_COMMANDE,
        "num_facture": texts.NUM_FACTURE,
        "date_facture": texts.slash_date(),
        "date_envoi": texts.slash_date(),
        "date_echeance": texts.slash_date(),
        "seller": texts.SELLER,
        "vat": texts.VAT,
        "payment": texts.PAY_MODE,
        "items": [
            {
                "sku": texts.SKU,
                "desc": texts.DESC,
                "qte": texts.QTE,
                "brut": texts.BRUT,
                "remise": texts.REMISE,
                "tva": texts.TVA,
            },
            {
                "sku": texts.SKU_2,
                "desc": texts.DESC_2,
                "qte": texts.QTE_2,
                "brut": texts.BRUT_2,
                "remise": texts.REMISE_2,
                "tva": texts.TVA_2,
            },
        ],
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
