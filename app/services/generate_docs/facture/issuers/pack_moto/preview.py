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
        "adresse": texts.ADRESSE_BILL,
        "cp_ville": texts.CP_BILL,
        "pays": texts.PAYS,
        "livraison_nom": texts.CLIENT_NOM,
        "livraison_prenom": texts.PRENOM,
        "livraison_societe": texts.SOCIETE,
        "livraison_adresse": texts.ADRESSE_SHIP,
        "livraison_cp_ville": texts.CP_SHIP,
        "livraison_pays": texts.PAYS,
        "num_facture": texts.NUM_FACTURE,
        "date_facture": texts.slash_date(),
        "num_commande": texts.NUM_COMMANDE,
        "date_commande": texts.slash_date(),
        "payment": texts.PAYMENT,
        "transporteur": texts.TRANSPORTEUR,
        "frais": texts.FRAIS,
        "items": [{
            "sku": texts.SKU,
            "desc": texts.DESC,
            "qte": texts.QTE,
            "pu": texts.PU,
            "tva": texts.TVA,
        }],
        "header": True,
        "header_logo": True,
        "header_title": True,
        "header_addresses": True,
        "middle": True,
        "middle_refs": True,
        "middle_columns": True,
        "middle_rows": True,
        "middle_tax": True,
        "middle_totals": True,
        "middle_pay": True,
        "footer": True,
        "footer_returns": True,
        "footer_issuer": True,
        "footer_tcpdf": True,
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
