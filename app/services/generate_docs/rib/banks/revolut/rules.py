"""Règles Revolut : min/max, charset. Titulaire / ville en casse mixte. IBAN compact."""

import re
import unicodedata

from . import layout

_FALSE = {"", "0", "false", "off", "no", "n"}
_TRUE = {"1", "true", "on", "yes", "y"}

FIELDS = {
    "header_title_text": {"min": 0, "max": layout.MAX_TITLE, "charset": "text"},
    "middle_titulaire_nom": {"min": 0, "max": layout.MAX_NOM, "charset": "upper"},
    "middle_titulaire_rue": {"min": 0, "max": layout.MAX_RUE, "charset": "text"},
    "middle_titulaire_cp": {"min": 0, "max": layout.MAX_CP, "charset": "digits"},
    "middle_titulaire_ville": {"min": 0, "max": layout.MAX_VILLE, "charset": "text"},
    "middle_titulaire_dept": {"min": 0, "max": layout.MAX_DEPT, "charset": "text"},
    "middle_banque": {"min": 5, "max": layout.MAX_BANQUE, "charset": "digits"},
    "middle_guichet": {"min": 5, "max": layout.MAX_GUICHET, "charset": "digits"},
    "middle_compte": {"min": 11, "max": layout.MAX_COMPTE, "charset": "alnum"},
    "middle_cle": {"min": 2, "max": layout.MAX_CLE, "charset": "digits"},
    "middle_iban_text": {"min": 27, "max": layout.MAX_IBAN, "charset": "iban"},
    "middle_bic_text": {"min": 8, "max": layout.MAX_BIC, "charset": "alnum"},
    "middle_domiciliation_nom": {"min": 0, "max": layout.MAX_DOM_NOM, "charset": "text"},
    "middle_domiciliation_rue": {"min": 0, "max": layout.MAX_DOM_RUE, "charset": "text"},
    "middle_domiciliation_pays": {"min": 0, "max": layout.MAX_DOM_PAYS, "charset": "text"},
}

_DOC_ATTR = {
    "header_title_text": ("header", "title"),
    "middle_titulaire_nom": ("card", "titulaire_nom"),
    "middle_titulaire_rue": ("card", "titulaire_rue"),
    "middle_titulaire_cp": ("card", "titulaire_cp"),
    "middle_titulaire_ville": ("card", "titulaire_ville"),
    "middle_titulaire_dept": ("card", "titulaire_dept"),
    "middle_banque": ("card", "banque"),
    "middle_guichet": ("card", "guichet"),
    "middle_compte": ("card", "compte"),
    "middle_cle": ("card", "cle"),
    "middle_iban_text": ("card", "iban"),
    "middle_bic_text": ("card", "bic"),
    "middle_domiciliation_nom": ("card", "domiciliation_nom"),
    "middle_domiciliation_rue": ("card", "domiciliation_rue"),
    "middle_domiciliation_pays": ("card", "domiciliation_pays"),
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
    text = re.sub(r"[\x00-\x09\x0b-\x1f\x7f]", " ", text)
    if spec is None:
        return text.strip()
    kind = spec["charset"]
    if kind == "text":
        text = re.sub(r"[^\S\n]+", " ", text)
        lines = [line.strip() for line in text.split("\n")]
        text = "\n".join(lines).strip()
    else:
        text = re.sub(r" +", " ", text)
        text = text.strip()
        if kind == "digits":
            text = re.sub(r"[^0-9]", "", text)
        elif kind == "alnum":
            text = re.sub(r"[^A-Za-z0-9]", "", text).upper()
        elif kind == "iban":
            text = re.sub(r"[^A-Za-z0-9]", "", text).upper()
        elif kind == "upper":
            text = re.sub(r"[^A-Za-zÀ-ÿ0-9 '’./()-]", "", text).upper()
    if field_id in {"middle_titulaire_rue", "middle_titulaire_ville", "middle_titulaire_dept"}:
        text = re.sub(r"[A-Za-zÀ-ÿ]+", lambda m: m.group(0).capitalize(), text)
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
