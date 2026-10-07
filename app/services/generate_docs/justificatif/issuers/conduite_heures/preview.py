"""Sorties debug (PNG / PDF / valeurs par défaut)."""

import tempfile
from pathlib import Path

import fitz

from . import copy as texts
from . import layout, rules
from .data import from_payload
from .generate import generate


def defaults() -> dict:
    return {
        "eleve": texts.ELEVE,
        "edition": texts.EDITION,
        "rdvs": [
            {
                "jour": texts.RDV1_JOUR,
                "date": texts.RDV1_DATE,
                "debut": texts.RDV1_DEBUT,
                "fin": texts.RDV1_FIN,
                "activite": texts.RDV1_ACTIVITE,
                "commentaire": texts.RDV1_COMMENT,
            },
            {
                "jour": texts.RDV2_JOUR,
                "date": texts.RDV2_DATE,
                "debut": texts.RDV2_DEBUT,
                "fin": texts.RDV2_FIN,
                "activite": texts.RDV2_ACTIVITE,
                "commentaire": texts.RDV2_COMMENT,
            },
            {
                "jour": texts.RDV3_JOUR,
                "date": texts.RDV3_DATE,
                "debut": texts.RDV3_DEBUT,
                "fin": texts.RDV3_FIN,
                "activite": texts.RDV3_ACTIVITE,
                "commentaire": texts.RDV3_COMMENT,
            },
        ],
        "_jours": list(layout.JOURS),
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
