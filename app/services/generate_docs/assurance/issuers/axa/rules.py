import re

from . import copy
from .data import Doc

# ----------------------------------------------------------------------


def clean_immat(v: str) -> str:
    if not v:
        return ""
    raw = re.sub(r"[^A-Za-z0-9]", "", v).upper()
    if len(raw) == 7 and raw[:2].isalpha() and raw[2:5].isdigit() and raw[5:].isalpha():
        return f"{raw[:2]}-{raw[2:5]}-{raw[5:]}"
    return v.strip().upper()


def apply_doc(doc: Doc) -> Doc:
    if not doc.header.edition_date:
        doc.header.edition_date = copy.default_edition_date()
    if not doc.middle.info_effet:
        doc.middle.info_effet = copy.default_info_effet()
    if doc.middle.vehicule_immat:
        doc.middle.vehicule_immat = clean_immat(doc.middle.vehicule_immat)
    return doc


def apply_payload(payload: dict | None = None) -> dict:
    p = dict(payload or {})
    if not p.get("edition_date"):
        p["edition_date"] = copy.default_edition_date()
    if not p.get("info_effet"):
        p["info_effet"] = copy.default_info_effet()
    if "vehicule_immat" in p and p["vehicule_immat"]:
        p["vehicule_immat"] = clean_immat(p["vehicule_immat"])
    return p


def public_limits() -> dict:
    return {}


def public_rules() -> dict:
    return {}
