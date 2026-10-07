"""Sorties debug (PNG / PDF / valeurs par défaut)."""

import io
import tempfile
from pathlib import Path

import fitz
from PIL import Image

from . import copy as texts
from . import rules
from .data import from_payload
from .generate import generate


def defaults() -> dict:
    return {
        "nom": texts.NOM,
        "prenom": texts.PRENOM,
        "adresse": texts.ADRESSE,
        "cp_ville": texts.VILLE_DEPT,
        "pays": texts.PAYS,
        "livraison_nom": texts.NOM,
        "livraison_prenom": texts.PRENOM,
        "livraison_adresse": texts.ADRESSE,
        "livraison_cp_ville": texts.VILLE,
        "livraison_pays": texts.PAYS,
        "seller_nom": texts.SELLER_AMZ,
        "seller_adresse": texts.SELLER_AMZ_ADDR,
        "seller_adresse2": "",
        "seller_cp_ville": texts.SELLER_AMZ_CITY,
        "seller_pays": texts.SELLER_AMZ_PAYS,
        "seller_tva": texts.SELLER_AMZ_TVA,
        "payment_ref": texts.PAYMENT_REF,
        "num_facture": texts.NUM_FACTURE_AMZ,
        "date_facture": texts.DATE_FACTURE,
        "total": texts.TOTAL,
        "num_commande": texts.NUM_COMMANDE,
        "date_commande": texts.DATE_COMMANDE,
        "expedition_ht": texts.EXPEDITION_HT,
        "expedition_ttc": texts.EXPEDITION_TTC,
        "remise_ht": texts.REMISE_HT,
        "remise_ttc": texts.REMISE_TTC,
        "tva_rate": texts.TVA_TEXT,
        "sold_by_amazon": True,
        "items": [
            {
                "nom": texts.PRODUIT,
                "note": texts.NOTE_PIECES,
                "qte": texts.QTE,
                "pu_ht": texts.PU_HT,
                "pu_ttc": texts.PU_TTC,
                "asin": texts.ASIN,
            },
        ],
        "_limits": rules.public_limits(),
        "_rules": rules.public_rules(),
        "_issuer_amazon": {
            "seller_nom": texts.SELLER_AMZ,
            "seller_adresse": texts.SELLER_AMZ_ADDR,
            "seller_adresse2": "",
            "seller_cp_ville": texts.SELLER_AMZ_CITY,
            "seller_pays": texts.SELLER_AMZ_PAYS,
            "seller_tva": texts.SELLER_AMZ_TVA,
            "num_facture": texts.NUM_FACTURE_AMZ,
        },
        "_issuer_market": {
            "seller_nom": texts.SELLER_MKP,
            "seller_adresse": texts.SELLER_MKP_ADDR,
            "seller_adresse2": "",
            "seller_cp_ville": texts.SELLER_MKP_CITY,
            "seller_pays": texts.SELLER_MKP_PAYS,
            "seller_tva": texts.SELLER_MKP_TVA,
            "num_facture": texts.NUM_FACTURE_MKP,
        },
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
    pixs = [
        page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
        for page in doc
    ]
    doc.close()
    if len(pixs) == 1:
        return pixs[0].tobytes("png")
    gap = max(8, int(8 * scale))
    width = max(p.width for p in pixs)
    height = sum(p.height for p in pixs) + gap * (len(pixs) - 1)
    canvas = Image.new("RGB", (width, height), (14, 15, 18))
    y = 0
    for pix in pixs:
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        canvas.paste(im, (0, y))
        y += pix.height + gap
    buf = io.BytesIO()
    canvas.save(buf, format="PNG")
    return buf.getvalue()


def png_bytes(payload: dict | None = None, scale: float = 2.0) -> bytes:
    return png_from_pdf(pdf_bytes(payload), scale)
