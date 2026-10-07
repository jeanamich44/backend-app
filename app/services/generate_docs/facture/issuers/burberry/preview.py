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
        "ville": texts.VILLE,
        "cp": texts.CP,
        "pays": texts.PAYS,
        "retrait_magasin": True,
        "num_commande": texts.NUM_COMMANDE,
        "date_commande": texts.slash_date(),
        "date_expedition": texts.slash_date(),
        "payment_mode": texts.PAYMENT,
        "items": [
            {
                "sku": texts.SKU,
                "barcode": texts.BARCODE,
                "desc": texts.DESC,
                "desc2": texts.DESC2,
                "taille": texts.TAILLE,
                "couleur": texts.COULEUR,
                "qte": texts.QTE,
                "prix": texts.PRIX,
            },
        ],
        "_payment_modes": list(texts.PAYMENT_MODES),
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
