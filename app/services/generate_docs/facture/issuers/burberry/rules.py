"""Règles déclaration Burberry : dates JJ/MM/AA, retrait magasin vs livraison."""

import re

from . import copy as texts
from . import layout

_FALSE = {"", "0", "false", "off", "no", "n"}
_TRUE = {"1", "true", "on", "yes", "y"}

FIELDS = {
    "nom": {"min": 0, "max": layout.MAX_NOM, "charset": "text"},
    "adresse": {"min": 0, "max": layout.MAX_ADRESSE, "charset": "text"},
    "ville": {"min": 0, "max": layout.MAX_VILLE, "charset": "text"},
    "cp": {"min": 0, "max": layout.MAX_CP, "charset": "text"},
    "pays": {"min": 0, "max": layout.MAX_PAYS, "charset": "text"},
    "num_commande": {"min": 0, "max": layout.MAX_REF, "charset": "text"},
    "date_commande": {"min": 0, "max": layout.MAX_DATE, "charset": "date"},
    "date_expedition": {"min": 0, "max": layout.MAX_DATE, "charset": "date"},
    "payment_mode": {"min": 0, "max": layout.MAX_PAY, "charset": "text"},
    "total": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
}

ITEM_FIELDS = {
    "sku": {"min": 0, "max": layout.MAX_SKU, "charset": "text"},
    "barcode": {"min": 0, "max": layout.MAX_BARCODE, "charset": "text"},
    "desc": {"min": 0, "max": layout.MAX_DESC, "charset": "text"},
    "desc2": {"min": 0, "max": layout.MAX_DESC, "charset": "text"},
    "taille": {"min": 0, "max": layout.MAX_TAILLE, "charset": "text"},
    "couleur": {"min": 0, "max": layout.MAX_COULEUR, "charset": "text"},
    "qte": {"min": 0, "max": layout.MAX_QTE, "charset": "qty"},
    "prix": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
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


def retrait_magasin(card) -> bool:
    return as_bool(getattr(card, "retrait_magasin", True), True)


def address_lines(card):
    """Retrait magasin : nom client + adresse boutique. Livraison : domicile."""
    if retrait_magasin(card):
        return (
            getattr(card, "nom", "") or "",
            texts.STORE_ADRESSE,
            texts.STORE_VILLE,
            texts.STORE_CP,
            texts.STORE_PAYS,
        )
    return (
        getattr(card, "nom", "") or "",
        getattr(card, "adresse", "") or "",
        getattr(card, "ville", "") or "",
        getattr(card, "cp", "") or "",
        getattr(card, "pays", "") or "",
    )


def _raw(value) -> str:
    if value is None or isinstance(value, bool):
        return ""
    if isinstance(value, (int, float)):
        return str(value)
    return str(value) if isinstance(value, str) else ""


def clean_date(value) -> str:
    digits = re.sub(r"\D", "", _raw(value))[:8]
    if len(digits) == 8:
        return f"{digits[:2]}/{digits[2:4]}/{digits[6:8]}"
    if len(digits) == 6:
        return f"{digits[:2]}/{digits[2:4]}/{digits[4:]}"
    return _raw(value).strip()[: layout.MAX_DATE]


def parse_money(value) -> float:
    text = _raw(value).strip().replace("\u00a0", " ").replace(" ", "")
    text = text.replace("€", "")
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
    return f"{round(value, 2):.2f}"


def format_qty(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return format_money(value)


def format_total(value: float) -> str:
    return f"( EUR ) {format_money(value)}"


def line_cost(item) -> tuple[float, float, float]:
    qte = parse_qty(getattr(item, "qte", 0))
    pu = parse_money(getattr(item, "prix", 0))
    return qte, pu, round(qte * pu, 2)


def invoice_total(items) -> float:
    return round(sum(line_cost(item)[2] for item in items or ()), 2)


def clean(field_id: str, value, spec=None) -> str:
    spec = spec or FIELDS.get(field_id) or {"max": 80, "charset": "text"}
    text = _raw(value)
    charset = spec.get("charset")
    if charset == "date":
        text = clean_date(text)
    elif charset == "money":
        text = format_money(parse_money(text)) if text.strip() else ""
    elif charset == "qty":
        text = format_qty(parse_qty(text)) if text.strip() else ""
    else:
        text = text.replace("\r", "").replace("\n", " ").strip()
    return text[: spec["max"]]


def clean_item(item: dict) -> dict:
    item = as_dict(item)
    return {key: clean(key, item.get(key, ""), spec) for key, spec in ITEM_FIELDS.items()}


def apply_payload(data: dict) -> dict:
    data = as_dict(data)
    out = dict(data)
    for field_id in FIELDS:
        if field_id in out and not isinstance(out[field_id], bool):
            out[field_id] = clean(field_id, out[field_id])
    if "retrait_magasin" in out:
        out["retrait_magasin"] = as_bool(out["retrait_magasin"], True)
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
    doc.card.retrait_magasin = as_bool(getattr(doc.card, "retrait_magasin", True), True)
    cleaned = []
    for item in getattr(doc.card, "items", ())[: layout.MAX_ROWS]:
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
