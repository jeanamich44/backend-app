"""Sorties debug (PNG / PDF / valeurs par défaut)."""

import tempfile
from dataclasses import asdict
from pathlib import Path

import fitz

from . import rules
from .data import Card, from_payload
from .generate import generate


def defaults() -> dict:
    out = asdict(Card())
    out["_limits"] = rules.public_limits()
    out["_rules"] = rules.public_rules()
    return out


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
