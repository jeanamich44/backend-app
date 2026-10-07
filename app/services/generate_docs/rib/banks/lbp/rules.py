"""Règles LBP uniquement (pas le filet BFB/BNP).

Titres et titulaire en MAJ. Notices / footer en casse mixte.
Compte 11 car. alnum (lettre possible, ex. M). BIC affiché lettre par lettre.
"""

import re
import unicodedata

from . import rib

_FALSE = {"", "0", "false", "off", "no", "n"}
_TRUE = {"1", "true", "on", "yes", "y"}
_UPPER_KEEP = re.compile(r"[^A-Za-zÀ-ÿ0-9 '’./()-]")

FIELDS = {
    "header_title_text": {"min": 0, "max": 40, "charset": "upper"},
    "header_notice_fr_text": {"min": 0, "max": 800, "charset": "text"},
    "header_notice_en_text": {"min": 0, "max": 500, "charset": "text"},
    "middle_title_text": {"min": 0, "max": 40, "charset": "upper"},
    "middle_etablissement": {"min": 5, "max": 5, "charset": "digits"},
    "middle_guichet": {"min": 5, "max": 5, "charset": "digits"},
    "middle_compte": {"min": 11, "max": 11, "charset": "alnum"},
    "middle_cle": {"min": 2, "max": 2, "charset": "digits"},
    "middle_iban": {"min": 27, "max": 35, "charset": "iban"},
    "middle_bic": {"min": 8, "max": 27, "charset": "bic_spaced"},
    "middle_domiciliation": {"min": 0, "max": 55, "charset": "upper"},
    "middle_titulaire_nom": {"min": 1, "max": 60, "charset": "upper"},
    "middle_titulaire_opt1": {"min": 0, "max": 60, "charset": "upper"},
    "middle_titulaire_opt2": {"min": 0, "max": 60, "charset": "upper"},
    "middle_titulaire_rue": {"min": 0, "max": 60, "charset": "upper"},
    "middle_titulaire_ville": {"min": 0, "max": 60, "charset": "upper"},
    "footer_line1_text": {"min": 0, "max": 220, "charset": "text"},
    "footer_line2_text": {"min": 0, "max": 220, "charset": "text"},
    "footer_code_text": {"min": 0, "max": 16, "charset": "code"},
}

_DOC_ATTR = {
    "header_title_text": ("header", "title"),
    "header_notice_fr_text": ("header", "notice_fr"),
    "header_notice_en_text": ("header", "notice_en"),
    "middle_title_text": ("card", "title"),
    "middle_etablissement": ("card", "etablissement"),
    "middle_guichet": ("card", "guichet"),
    "middle_compte": ("card", "compte"),
    "middle_cle": ("card", "cle"),
    "middle_iban": ("card", "iban"),
    "middle_bic": ("card", "bic"),
    "middle_domiciliation": ("card", "domiciliation"),
    "middle_titulaire_nom": ("card", "titulaire_nom"),
    "middle_titulaire_opt1": ("card", "titulaire_opt1"),
    "middle_titulaire_opt2": ("card", "titulaire_opt2"),
    "middle_titulaire_rue": ("card", "titulaire_rue"),
    "middle_titulaire_ville": ("card", "titulaire_ville"),
    "footer_line1_text": ("footer", "line1"),
    "footer_line2_text": ("footer", "line2"),
    "footer_code_text": ("footer", "code"),
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
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = re.sub(r"[\x00-\x1f\x7f]", " ", text)
    text = re.sub(r" +", " ", text)
    if spec is None:
        return text.strip()
    kind = spec["charset"]
    if kind == "digits":
        text = re.sub(r"[^0-9]", "", text)
    elif kind == "alnum":
        text = re.sub(r"[^A-Za-z0-9]", "", text).upper()
    elif kind == "iban":
        text = re.sub(r"[^A-Za-z0-9 ]", "", text).upper()
        text = re.sub(r" +", " ", text).strip()
    elif kind == "bic_spaced":
        text = rib.format_bic(re.sub(r"[^A-Za-z0-9]", "", text)[:11])
    elif kind == "code":
        text = re.sub(r"[^A-Za-z0-9_]", "", text).upper()
    elif kind == "upper":
        text = _UPPER_KEEP.sub("", text).upper()
        text = re.sub(r" +", " ", text).strip()
    else:
        text = text.lstrip()
    max_n = spec["max"]
    if max_n is not None:
        text = text[:max_n]
    return text


def field_issue(field_id: str, value) -> str | None:
    spec = FIELDS.get(field_id)
    if spec is None:
        return None
    cleaned = clean(field_id, value)
    if spec["charset"] == "bic_spaced":
        n = len(rib.compact(cleaned))
    elif spec["charset"] == "iban":
        n = len(rib.compact(cleaned))
    else:
        n = len(cleaned)
    if n < spec["min"]:
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
        if field_id in out and not isinstance(data.get(field_id), bool):
            out[field_id] = clean(field_id, out[field_id])
    if "header_brand_title_text" in out and isinstance(data.get("header_brand_title_text"), str):
        out["header_brand_title_text"] = clean("middle_title_text", out["header_brand_title_text"])
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
