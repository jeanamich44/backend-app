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
        "adresse": texts.ADRESSE,
        "cp_ville": texts.CP_VILLE,
        "date": texts.paris_date(),
        "num_client": texts.NUM_CLIENT,
        "depuis": texts.DEPUIS,
        "header": True,
        "header_logo": True,
        "header_window": True,
        "header_title": True,
        "middle": True,
        "middle_refs": True,
        "middle_body": True,
        "middle_sign": True,
        "middle_note": True,
        "footer": True,
        "footer_site": True,
        "footer_legal": True,
        "footer_ref": True,
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
