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
        "livraison_email": texts.EMAIL,
        "livraison_nom": texts.CLIENT_NOM,
        "livraison_prenom": texts.PRENOM,
        "livraison_adresse": texts.ADRESSE,
        "livraison_cp_ville": texts.VILLE,
        "livraison_pays": texts.PAYS_WEB,
        "facturation_email": texts.EMAIL,
        "facturation_nom": texts.CLIENT_NOM,
        "facturation_prenom": texts.PRENOM,
        "facturation_adresse": texts.ADRESSE,
        "facturation_cp_ville": texts.VILLE,
        "facturation_pays": texts.PAYS_WEB,
        "store_nom": texts.STORE_WEB_NOM,
        "store_l1": texts.STORE_WEB_L1,
        "store_l2": texts.STORE_WEB_L2,
        "store_l3": texts.STORE_WEB_L3,
        "num_commande": texts.NUM_COMMANDE,
        "date_commande": texts.DATE_WEB,
        "num_facture": texts.NUM_FACTURE,
        "date_facture": texts.DATE_WEB,
        "nref": texts.NREF,
        "matricule": texts.MATRICULE,
        "payment_mode": texts.PAYMENT_WEB,
        "echeance": texts.DATE_WEB,
        "tva_code": texts.TVA_CODE_WEB,
        "tva_rate": texts.TVA_RATE,
        "frais_ht": texts.FRAIS_HT,
        "tva_frais": texts.TVA_FRAIS,
        "pays_expedition": texts.SHIP,
        "en_ligne": True,
        "items": [
            {
                "nom": texts.PRODUIT,
                "subtitle": texts.SUBTITLE,
                "ean": texts.EAN,
                "reference": texts.REFERENCE,
                "qte": texts.QTE,
                "pu_ht": texts.PU_HT,
                "pu_ttc": texts.PU_TTC,
                "pu_brut_ht": texts.PU_BRUT,
                "remise_ht": texts.REMISE_HT,
                "serial": texts.SERIAL,
                "distribution": texts.DISTRIBUTION,
                "pieces": texts.PIECES,
                "garantie": texts.GARANTIE,
                "eco_ht": texts.ECO_HT,
                "eco_ttc": texts.ECO_TTC,
            },
        ],
        "_payment_modes": list(texts.PAYMENT_MODES),
        "_rules": rules.public_rules(),
        "_channel_web": {
            "store_nom": texts.STORE_WEB_NOM,
            "store_l1": texts.STORE_WEB_L1,
            "store_l2": texts.STORE_WEB_L2,
            "store_l3": texts.STORE_WEB_L3,
            "payment_mode": texts.PAYMENT_WEB,
            "tva_code": texts.TVA_CODE_WEB,
            "date_commande": texts.DATE_WEB,
            "date_facture": texts.DATE_WEB,
            "echeance": texts.DATE_WEB,
            "livraison_pays": texts.PAYS_WEB,
            "facturation_pays": texts.PAYS_WEB,
        },
        "_channel_magasin": {
            "store_nom": texts.STORE_MAG_NOM,
            "store_l1": texts.STORE_MAG_L1,
            "store_l2": texts.STORE_MAG_L2,
            "store_l3": texts.STORE_MAG_L3,
            "payment_mode": texts.PAYMENT_MAG,
            "tva_code": texts.TVA_CODE_MAG,
            "date_commande": texts.DATE_MAG,
            "date_facture": texts.DATE_MAG,
            "echeance": texts.DATE_MAG,
            "livraison_pays": texts.PAYS_MAG,
            "facturation_pays": texts.PAYS_MAG,
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
