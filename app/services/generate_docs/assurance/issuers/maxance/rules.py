"""Règles mémo Maxance : min/max, charset."""

import re
import unicodedata

from . import layout

_FALSE = {"", "0", "false", "off", "no", "n"}
_TRUE = {"1", "true", "on", "yes", "y"}

FIELDS = {
    "num_client": {"min": 0, "max": layout.MAX_CLIENT, "charset": "text"},
    "num_contrat": {"min": 0, "max": layout.MAX_CONTRAT, "charset": "text"},
    "num_orias": {"min": 0, "max": layout.MAX_ORIAS, "charset": "text"},
    "courtier": {"min": 0, "max": layout.MAX_COURTIER, "charset": "text"},
    "titulaire": {"min": 0, "max": layout.MAX_TITULAIRE, "charset": "text"},
    "adresse": {"min": 0, "max": layout.MAX_ADRESSE, "charset": "text"},
    "cp_ville": {"min": 0, "max": layout.MAX_VILLE, "charset": "text"},
    "pays": {"min": 0, "max": layout.MAX_PAYS, "charset": "text"},
    "date_delivrance": {"min": 0, "max": layout.MAX_DATE, "charset": "text"},
    "date_effet_jour": {"min": 0, "max": layout.MAX_JOUR, "charset": "digits"},
    "date_effet_mois": {"min": 0, "max": layout.MAX_MOIS, "charset": "digits"},
    "date_effet_annee": {"min": 0, "max": layout.MAX_ANNEE, "charset": "digits"},
    "immatriculation": {"min": 0, "max": layout.MAX_IMMAT, "charset": "upper"},
    "vehicule": {"min": 0, "max": layout.MAX_VEHICULE, "charset": "upper"},
}

_DOC_ATTR = {
    "num_client": ("card", "num_client"),
    "num_contrat": ("card", "num_contrat"),
    "num_orias": ("card", "num_orias"),
    "courtier": ("card", "courtier"),
    "titulaire": ("card", "titulaire"),
    "adresse": ("card", "adresse"),
    "cp_ville": ("card", "cp_ville"),
    "pays": ("card", "pays"),
    "date_delivrance": ("card", "date_delivrance"),
    "date_effet_jour": ("card", "date_effet_jour"),
    "date_effet_mois": ("card", "date_effet_mois"),
    "date_effet_annee": ("card", "date_effet_annee"),
    "immatriculation": ("card", "immatriculation"),
    "vehicule": ("card", "vehicule"),
}


def as_dict(data) -> dict:
    return data if isinstance(data, dict) else {}


def as_bool(value, default: bool = True) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        v = value.strip().lower()
        if v in _FALSE:
            return False
        if v in _TRUE:
            return True
        return default
    return bool(value)


def flag(data: dict, key: str, default: bool = True) -> bool:
    if key not in data:
        return default
    return as_bool(data[key], default)


_CIV = {
    "M": "M.",
    "M.": "M.",
    "MR": "M.",
    "MR.": "M.",
    "MME": "Mme",
    "MME.": "Mme",
    "MRS": "Mme",
    "MLLE": "Mlle",
    "MLLE.": "Mlle",
}


def format_titulaire(text: str) -> str:
    """Civilité + prénom en casse titre + NOM en majuscules."""
    parts = text.split()
    if not parts:
        return text
    civ = ""
    key = parts[0].upper()
    if key in _CIV:
        civ = _CIV[key]
        parts = parts[1:]
    elif key.rstrip(".") in _CIV:
        civ = _CIV[key.rstrip(".")]
        parts = parts[1:]
    if not parts:
        return civ or text
    if len(parts) == 1:
        body = parts[0].upper()
    else:
        *firsts, last = parts
        body = " ".join(p.capitalize() for p in firsts) + " " + last.upper()
    return f"{civ} {body}".strip() if civ else body


def clean(field_id: str, value) -> str:
    spec = FIELDS.get(field_id)
    if value is None or isinstance(value, bool):
        text = ""
    elif isinstance(value, (int, float)):
        text = str(value)
    elif isinstance(value, str):
        text = value
    else:
        text = ""
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\u00a0", " ").replace("\u202f", " ")
    text = re.sub(r"[\x00-\x09\x0b-\x1f\x7f]", " ", text)
    if spec is None:
        return text.strip()
    kind = spec["charset"]
    text = re.sub(r" +", " ", text).strip()
    if kind == "digits":
        text = re.sub(r"[^0-9]", "", text)
    elif kind == "upper":
        text = text.upper()
    if field_id == "titulaire":
        text = format_titulaire(text)
    max_n = spec["max"]
    if max_n is not None:
        text = text[:max_n]
    return text


def field_issue(field_id: str, value) -> str | None:
    spec = FIELDS.get(field_id)
    if spec is None:
        return None
    if len(clean(field_id, value)) < spec["min"]:
        return "min"
    return None


def payload_issues(data: dict) -> dict:
    data = as_dict(data)
    out = {}
    for field_id in FIELDS:
        if field_id not in data or isinstance(data[field_id], bool):
            continue
        issue = field_issue(field_id, data[field_id])
        if issue:
            out[field_id] = issue
    return out


def apply_payload(data: dict) -> dict:
    data = as_dict(data)
    out = dict(data)
    for field_id in FIELDS:
        if field_id in out and not isinstance(out[field_id], bool):
            out[field_id] = clean(field_id, out[field_id])
    return out


def apply_doc(doc):
    for field_id, (group, attr) in _DOC_ATTR.items():
        obj = getattr(doc, group)
        setattr(obj, attr, clean(field_id, getattr(obj, attr)))
    return doc


def public_rules() -> dict:
    return {
        field_id: {"min": spec["min"], "max": spec["max"], "charset": spec["charset"]}
        for field_id, spec in FIELDS.items()
    }


def public_limits() -> dict:
    return {field_id: spec["max"] for field_id, spec in FIELDS.items()}
