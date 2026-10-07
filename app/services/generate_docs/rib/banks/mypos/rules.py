"""Règles MyPOS : min/max, charset. Société / adresse / titulaire en capitales."""

import re
import unicodedata

from . import layout

_FALSE = {"", "0", "false", "off", "no", "n"}
_TRUE = {"1", "true", "on", "yes", "y"}

_UPPER = {
    "middle_nom_societe",
    "middle_adresse",
    "middle_cp_ville",
    "middle_titulaire_nom",
}

FIELDS = {
    "header_title_text": {"min": 0, "max": layout.MAX_TITLE, "charset": "text"},
    "header_date_text": {"min": 0, "max": layout.MAX_DATE, "charset": "text"},
    "middle_nom_societe": {"min": 0, "max": layout.MAX_NOM, "charset": "text"},
    "middle_num_enregistrement": {"min": 0, "max": layout.MAX_SIREN, "charset": "alnum"},
    "middle_adresse": {"min": 0, "max": layout.MAX_ADRESSE, "charset": "text"},
    "middle_cp_ville": {"min": 0, "max": layout.MAX_VILLE, "charset": "text"},
    "middle_pays": {"min": 0, "max": layout.MAX_PAYS, "charset": "text"},
    "middle_titulaire_nom": {"min": 0, "max": layout.MAX_TITULAIRE, "charset": "text"},
    "middle_compte": {"min": 0, "max": layout.MAX_COMPTE, "charset": "digits"},
    "middle_iban_text": {"min": 15, "max": layout.MAX_IBAN, "charset": "iban"},
    "middle_bic_text": {"min": 8, "max": layout.MAX_BIC, "charset": "alnum"},
    "middle_devise": {"min": 0, "max": layout.MAX_DEVISE, "charset": "alnum"},
    "footer_page_text": {"min": 0, "max": layout.MAX_PAGE, "charset": "digits"},
}

_DOC_ATTR = {
    "header_title_text": ("header", "title"),
    "header_date_text": ("header", "date"),
    "middle_nom_societe": ("card", "nom_societe"),
    "middle_num_enregistrement": ("card", "num_enregistrement"),
    "middle_adresse": ("card", "adresse"),
    "middle_cp_ville": ("card", "cp_ville"),
    "middle_pays": ("card", "pays"),
    "middle_titulaire_nom": ("card", "titulaire"),
    "middle_compte": ("card", "compte"),
    "middle_iban_text": ("card", "iban"),
    "middle_bic_text": ("card", "bic"),
    "middle_devise": ("card", "devise"),
    "footer_page_text": ("footer", "page"),
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
    if kind == "text":
        text = re.sub(r"[^\S\n]+", " ", text)
        text = text.strip()
        if field_id in _UPPER:
            text = text.upper()
    else:
        text = re.sub(r" +", " ", text)
        text = text.strip()
        if kind == "digits":
            text = re.sub(r"[^0-9]", "", text)
        elif kind == "alnum":
            text = re.sub(r"[^A-Za-z0-9]", "", text).upper()
        elif kind == "iban":
            text = re.sub(r"[^A-Za-z0-9]", "", text).upper()
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
