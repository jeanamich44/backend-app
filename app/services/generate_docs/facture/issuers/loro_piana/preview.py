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
        "num_ticket": texts.NUM_TICKET,
        "ticket_caisse": texts.TICKET_CAISSE,
        "date_ticket": texts.ticket_datetime(),
        "nom": texts.NOM,
        "prenom": texts.PRENOM,
        "caissier": texts.CAISSIER,
        "payment": texts.PAYMENT,
        "monnaie": texts.MONNAIE_AMT,
        "tva_rate": texts.TVA_RATE,
        "items": [{
            "sku": texts.SKU,
            "desc": texts.DESC,
            "qte": texts.QTE,
            "prix": texts.PRIX,
        }],
        "header": True,
        "header_logo": True,
        "header_store": True,
        "header_title": True,
        "header_refs": True,
        "middle": True,
        "middle_columns": True,
        "middle_rows": True,
        "middle_totals": True,
        "middle_pay": True,
        "middle_line": True,
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
