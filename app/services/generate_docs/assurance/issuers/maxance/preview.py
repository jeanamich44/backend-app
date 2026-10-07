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
        "num_client": texts.NUM_CLIENT,
        "num_contrat": texts.NUM_CONTRAT,
        "num_orias": texts.NUM_ORIAS,
        "courtier": texts.COURTIER,
        "titulaire": texts.TITULAIRE,
        "adresse": texts.ADRESSE,
        "cp_ville": texts.CP_VILLE,
        "pays": texts.PAYS,
        "date_delivrance": texts.DATE_DELIVRANCE,
        "date_effet_jour": texts.DATE_EFFET_JOUR,
        "date_effet_mois": texts.DATE_EFFET_MOIS,
        "date_effet_annee": texts.DATE_EFFET_ANNEE,
        "immatriculation": texts.IMMATRICULATION,
        "vehicule": texts.VEHICULE,
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
