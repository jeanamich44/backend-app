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
        "civilite": texts.CIVILITY.strip(),
        "nom": texts.NOM,
        "prenom": texts.PRENOM,
        "client_nom": texts.CLIENT_NOM,
        "adresse": texts.ADRESSE,
        "cp_ville": texts.CP_VILLE,
        "date_facture": texts.slash_date_yy(),
        "num_facture": texts.NUM_FACTURE,
        "num_client": texts.NUM_CLIENT,
        "num_contrat": texts.NUM_CONTRAT,
        "lieu_pce": texts.LIEU_PCE,
        "lieu_bat": texts.LIEU_BAT,
        "montant_gaz": texts.MONTANT_GAZ,
        "montant_prestations": texts.MONTANT_PREST,
        "total": texts.TOTAL_TTC,
        "montant_ht": texts.MONTANT_HT,
        "montant_tva": texts.MONTANT_TVA,
        "compte": texts.COMPTE,
        "header": True,
        "header_logo": True,
        "header_title": True,
        "header_refs": True,
        "header_lieu": True,
        "header_window": True,
        "header_barcode": True,
        "header_correspond": True,
        "middle": True,
        "middle_legal": True,
        "middle_amounts": True,
        "middle_next": True,
        "middle_paiement": True,
        "footer": True,
        "footer_contacts": True,
        "footer_economies": True,
        "footer_cheque": True,
        "footer_triman": True,
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
