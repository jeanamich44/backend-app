"""Règles ticket Loro Piana : date JJ-MM-AAAA HH:MM:SS, montants 80.00."""

import re

from . import layout

_FALSE = {"", "0", "false", "off", "no", "n"}
_TRUE = {"1", "true", "on", "yes", "y"}

FIELDS = {
    "num_ticket": {"min": 0, "max": layout.MAX_TICKET, "charset": "text"},
    "ticket_caisse": {"min": 0, "max": layout.MAX_CAISSE, "charset": "text"},
    "date_ticket": {"min": 0, "max": layout.MAX_DATETIME, "charset": "datetime"},
    "caissier": {"min": 0, "max": layout.MAX_CAISSIER, "charset": "text"},
    "payment": {"min": 0, "max": layout.MAX_PAY, "charset": "text"},
    "monnaie": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
    "tva_rate": {"min": 0, "max": layout.MAX_TVA, "charset": "money"},
    "total": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
}

ITEM_FIELDS = {
    "sku": {"min": 0, "max": layout.MAX_SKU, "charset": "text"},
    "desc": {"min": 0, "max": layout.MAX_DESC, "charset": "text"},
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


def _raw(value) -> str:
    if value is None or isinstance(value, bool):
        return ""
    if isinstance(value, (int, float)):
        return str(value)
    return str(value) if isinstance(value, str) else ""


def clean_datetime(value) -> str:
    text = re.sub(r"\s+", " ", _raw(value)).strip()
    match = re.match(
        r"^(\d{1,2})[./-](\d{1,2})[./-](\d{2,4})(?:[ T](\d{1,2}):(\d{1,2})(?::(\d{1,2}))?)?$",
        text,
    )
    if not match:
        return text[: layout.MAX_DATETIME]
    day, month, year = int(match.group(1)), int(match.group(2)), match.group(3)
    if len(year) == 2:
        year = "20" + year
    hour = int(match.group(4) or 0)
    minute = int(match.group(5) or 0)
    second = int(match.group(6) or 0)
    day = min(max(day, 1), 31)
    month = min(max(month, 1), 12)
    hour = min(max(hour, 0), 23)
    minute = min(max(minute, 0), 59)
    second = min(max(second, 0), 59)
    return f"{day:02d}-{month:02d}-{int(year):04d} {hour:02d}:{minute:02d}:{second:02d}"


def parse_money(value) -> float:
    text = _raw(value).strip().replace("\u00a0", " ").replace(" ", "")
    text = text.replace("€", "").replace("%", "")
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


def format_money(value: float) -> str:
    return f"{round(value, 2):.2f}"


def format_euro(value: float) -> str:
    return "€" + format_money(value)


def format_qty(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return format_money(value)


def format_pct(value: float) -> str:
    return format_money(value) + " %"


def line_total(item) -> float:
    return round(parse_money(item.prix) * parse_money(item.qte), 2)


def items_total(items) -> float:
    return round(sum(line_total(item) for item in items or ()), 2)


def qty_total(items) -> float:
    return sum(parse_money(getattr(item, "qte", 0)) for item in items or ())


def vat_amount(ttc: float, rate: float) -> float:
    if ttc == 0 or rate == 0:
        return 0.0
    return round(ttc * rate / (100.0 + rate), 2)


def clean_item(item: dict) -> dict:
    item = as_dict(item)
    return {key: clean(key, item.get(key, ""), spec) for key, spec in ITEM_FIELDS.items()}


def format_ticket_caisse(value) -> str:
    s = _raw(value).strip()
    if not s:
        return ""
    parts = [p.strip() for p in re.split(r"[\s-]+", s) if p.strip()]
    if len(parts) == 3:
        return f"{parts[0].upper()} - {parts[1]} - {parts[2]}"
    if len(parts) == 2:
        return f"{parts[0].upper()} - {parts[1]}"
    m = re.match(r"^([A-Za-z]{2}\d{2})(\d{2})(\d{4,})$", s)
    if m:
        return f"{m.group(1).upper()} - {m.group(2)} - {m.group(3)}"
    return s


def clean(field_id: str, value, spec=None) -> str:
    spec = spec or FIELDS.get(field_id) or ITEM_FIELDS.get(field_id) or {
        "max": 80, "charset": "text",
    }
    text = _raw(value)
    if field_id == "ticket_caisse":
        text = format_ticket_caisse(text)
    charset = spec.get("charset")
    if charset == "datetime":
        text = clean_datetime(text)
    elif charset == "money":
        text = format_money(max(0.0, parse_money(text))) if text.strip() else ""
    elif charset == "qty":
        text = format_qty(max(0.0, parse_money(text))) if text.strip() else ""
    else:
        text = text.replace("\r", "").replace("\n", " ").strip()
    return text[: spec["max"]]


def apply_payload(data: dict) -> dict:
    data = as_dict(data)
    out = dict(data)
    prenom = str(data.get("prenom") or "").strip()
    nom = str(data.get("nom") or "").strip()
    if prenom and nom:
        if not data.get("caissier"):
            out["caissier"] = nom if prenom.lower() in nom.lower() else f"{nom} {prenom}"
    elif nom or prenom:
        if not data.get("caissier"):
            out["caissier"] = nom or prenom
    d_ticket = str(data.get("date_ticket") or data.get("date") or "").strip()
    h_ticket = str(data.get("heure_ticket") or data.get("heure") or "").strip()
    if d_ticket and h_ticket and " " not in d_ticket:
        out["date_ticket"] = f"{d_ticket} {h_ticket}"
    elif d_ticket:
        out["date_ticket"] = d_ticket

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
    limits.update({key: spec["max"] for key, spec in ITEM_FIELDS.items()})
    limits["max_rows"] = layout.MAX_ROWS
    return limits
