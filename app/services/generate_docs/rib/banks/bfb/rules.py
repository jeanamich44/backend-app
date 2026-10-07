"""Règles BFB : min/max, charset. Filet moteur (pas celles de LBP/BNP).

Pays « France » et domiciliation restent en casse mixte (virgules).
Titulaire / rue / ville en MAJ. BIC compact (pas lettre par lettre).
"""

import re
import unicodedata

_FALSE = {"", "0", "false", "off", "no", "n"}
_TRUE = {"1", "true", "on", "yes", "y"}

# BFB : adresse d'agence / domiciliation en casse mixte (virgules, « France »).
# Titulaire + rue/ville d'en-tête en MAJ. BIC compact, pas espacé.
FIELDS = {
    "middle_titulaire_nom": {"min": 1, "max": 40, "charset": "upper"},
    "header_rue": {"min": 0, "max": 42, "charset": "upper"},
    "header_ville": {"min": 0, "max": 40, "charset": "upper"},
    "header_pays": {"min": 0, "max": 20, "charset": "text"},
    "middle_banque": {"min": 5, "max": 5, "charset": "digits"},
    "middle_guichet": {"min": 5, "max": 5, "charset": "digits"},
    "middle_compte": {"min": 11, "max": 11, "charset": "alnum"},
    "middle_cle": {"min": 2, "max": 2, "charset": "digits"},
    "middle_iban_text": {"min": 27, "max": 34, "charset": "iban"},
    "middle_bic_text": {"min": 8, "max": 11, "charset": "alnum"},
    "middle_domiciliation_text": {"min": 0, "max": 80, "charset": "text"},
}

_UPPER_KEEP = re.compile(r"[^A-Za-zÀ-ÿ0-9 '’./()-]")

_DOC_ATTR = {
    "middle_titulaire_nom": ("card", "titulaire_nom"),
    "header_rue": ("header", "rue"),
    "header_ville": ("header", "ville"),
    "header_pays": ("header", "pays"),
    "middle_banque": ("card", "banque"),
    "middle_guichet": ("card", "guichet"),
    "middle_compte": ("card", "compte"),
    "middle_cle": ("card", "cle"),
    "middle_iban_text": ("card", "iban"),
    "middle_bic_text": ("card", "bic"),
    "middle_domiciliation_text": ("card", "domiciliation"),
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
    elif kind == "upper":
        text = _UPPER_KEEP.sub("", text).upper()
        text = re.sub(r" +", " ", text).strip()
    else:
        text = text.strip()
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
        if field_id in out:
            out[field_id] = clean(field_id, out[field_id])
    for alias, field_id in (
        ("middle_iban", "middle_iban_text"),
        ("middle_bic", "middle_bic_text"),
        ("middle_domiciliation", "middle_domiciliation_text"),
    ):
        if alias in out and isinstance(data.get(alias), str):
            out[alias] = clean(field_id, out[alias])
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
