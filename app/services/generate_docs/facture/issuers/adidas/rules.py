"""Règles facture Adidas : longueurs, dates JJ.MM.AAAA, montants."""

import re

from . import layout

_FALSE = {"", "0", "false", "off", "no", "n"}
_TRUE = {"1", "true", "on", "yes", "y"}

FIELDS = {
    "nom": {"min": 0, "max": layout.MAX_NOM, "charset": "text"},
    "adresse": {"min": 0, "max": layout.MAX_ADRESSE, "charset": "text"},
    "cp_ville": {"min": 0, "max": layout.MAX_VILLE, "charset": "text"},
    "pays": {"min": 0, "max": layout.MAX_PAYS, "charset": "upper"},
    "livraison_nom": {"min": 0, "max": layout.MAX_NOM, "charset": "text"},
    "livraison_adresse": {"min": 0, "max": layout.MAX_ADRESSE, "charset": "text"},
    "livraison_cp_ville": {"min": 0, "max": layout.MAX_VILLE, "charset": "text"},
    "livraison_pays": {"min": 0, "max": layout.MAX_PAYS, "charset": "upper"},
    "num_commande": {"min": 0, "max": layout.MAX_REF, "charset": "upper"},
    "num_facture": {"min": 0, "max": layout.MAX_REF, "charset": "upper"},
    "date_facture": {"min": 0, "max": layout.MAX_DATE, "charset": "date"},
    "date_livraison": {"min": 0, "max": layout.MAX_DATE, "charset": "date"},
    "total": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
}

ITEM_FIELDS = {
    "sku": {"min": 0, "max": layout.MAX_SKU, "charset": "upper"},
    "taille": {"min": 0, "max": layout.MAX_TAILLE, "charset": "text"},
    "nom": {"min": 0, "max": layout.MAX_PRODUIT, "charset": "text"},
    "qte": {"min": 0, "max": layout.MAX_QTE, "charset": "qty"},
    "pu_ht": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
    "pu_ttc": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
}

_DOC_ATTR = {key: ("card", key) for key in FIELDS}
_ITEM_KEYS = tuple(ITEM_FIELDS)


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


def _raw(value) -> str:
    if value is None or isinstance(value, bool):
        return ""
    if isinstance(value, (int, float)):
        return str(value)
    return str(value) if isinstance(value, str) else ""


def clean_date(value) -> str:
    digits = re.sub(r"\D", "", _raw(value))[:8]
    if len(digits) == 8:
        return f"{digits[:2]}.{digits[2:4]}.{digits[4:]}"
    if len(digits) == 6:
        return f"{digits[:2]}.{digits[2:4]}.{digits[4:]}"
    return _raw(value).strip()[: layout.MAX_DATE]


def parse_money(value) -> float:
    text = _raw(value).strip().replace("\u00a0", " ").replace(" ", "")
    if not text:
        return 0.0
    if "," in text and "." in text:
        text = text.replace(".", "").replace(",", ".")
    else:
        text = text.replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return 0.0


def parse_qty(value) -> float:
    return parse_money(value)


def format_money(value: float) -> str:
    return f"{value:.2f}".replace(".", ",")


def format_qty(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return format_money(value)


def line_amounts(item):
    qte = parse_qty(getattr(item, "qte", 0))
    ht = parse_money(getattr(item, "pu_ht", 0))
    ttc = parse_money(getattr(item, "pu_ttc", 0))
    return qte, ht, ttc, qte * ht, qte * ttc


def invoice_totals(items) -> tuple[float, float, float]:
    sous = 0.0
    montant = 0.0
    for item in items or ():
        _qte, _ht, _ttc, line_ht, line_ttc = line_amounts(item)
        sous += line_ttc
        montant += line_ht
    return sous, montant, sous - montant


def clean(field_id: str, value, spec=None) -> str:
    spec = spec or FIELDS.get(field_id) or {"max": 80, "charset": "text"}
    text = _raw(value)
    charset = spec.get("charset")
    if charset == "date":
        text = clean_date(text)
    elif charset == "upper":
        text = re.sub(r"\s+", " ", text).strip().upper()
    elif charset == "money":
        text = format_money(parse_money(text)) if text.strip() else ""
    elif charset == "qty":
        text = format_qty(parse_qty(text)) if text.strip() else ""
    else:
        text = text.replace("\r", "").replace("\n", " ").strip()
    return text[: spec["max"]]


def clean_item(item: dict) -> dict:
    item = as_dict(item)
    out = {}
    for key, spec in ITEM_FIELDS.items():
        out[key] = clean(key, item.get(key, ""), spec)
    return out


def apply_payload(data: dict) -> dict:
    data = as_dict(data)
    out = dict(data)
    for field_id in FIELDS:
        if field_id in out and not isinstance(out[field_id], bool):
            out[field_id] = clean(field_id, out[field_id])
    raw_items = out.get("items")
    if isinstance(raw_items, list):
        items = []
        for item in raw_items[: layout.MAX_ROWS]:
            if isinstance(item, dict):
                items.append(clean_item(item))
        out["items"] = items
    return out


def apply_doc(doc):
    for field_id, (group, attr) in _DOC_ATTR.items():
        obj = getattr(doc, group)
        setattr(obj, attr, clean(field_id, getattr(obj, attr)))
    cleaned = []
    for item in doc.card.items[: layout.MAX_ROWS]:
        payload = {key: getattr(item, key, "") for key in _ITEM_KEYS}
        data = clean_item(payload)
        for key, value in data.items():
            setattr(item, key, value)
        cleaned.append(item)
    doc.card.items = cleaned
    return doc


def public_rules() -> dict:
    out = {
        field_id: {"min": spec["min"], "max": spec["max"], "charset": spec["charset"]}
        for field_id, spec in FIELDS.items()
    }
    out["items"] = {
        key: {"min": spec["min"], "max": spec["max"], "charset": spec["charset"]}
        for key, spec in ITEM_FIELDS.items()
    }
    return out


def public_limits() -> dict:
    limits = {field_id: spec["max"] for field_id, spec in FIELDS.items()}
    limits["max_rows"] = layout.MAX_ROWS
    limits.update({f"item_{key}": spec["max"] for key, spec in ITEM_FIELDS.items()})
    return limits
