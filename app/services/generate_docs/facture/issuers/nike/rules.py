"""Règles facture Nike : dates j/m/aaaa, montants 1,23 €, qté 1.00."""

import re

from . import layout

_FALSE = {"", "0", "false", "off", "no", "n"}
_TRUE = {"1", "true", "on", "yes", "y"}

FIELDS = {
    "nom": {"min": 0, "max": layout.MAX_NOM, "charset": "text"},
    "adresse": {"min": 0, "max": layout.MAX_ADRESSE, "charset": "text"},
    "cp_ville": {"min": 0, "max": layout.MAX_VILLE, "charset": "text"},
    "pays": {"min": 0, "max": layout.MAX_PAYS, "charset": "upper"},
    "livraison_adresse": {"min": 0, "max": layout.MAX_ADRESSE, "charset": "text"},
    "livraison_cp_ville": {"min": 0, "max": layout.MAX_VILLE, "charset": "text"},
    "livraison_pays": {"min": 0, "max": layout.MAX_PAYS, "charset": "upper"},
    "num_commande": {"min": 0, "max": layout.MAX_REF, "charset": "upper"},
    "num_facture": {"min": 0, "max": layout.MAX_REF, "charset": "upper"},
    "date_facture": {"min": 0, "max": layout.MAX_DATE, "charset": "date"},
    "date_envoi": {"min": 0, "max": layout.MAX_DATE, "charset": "date"},
    "date_echeance": {"min": 0, "max": layout.MAX_DATE, "charset": "date"},
    "seller": {"min": 0, "max": layout.MAX_SELLER, "charset": "text"},
    "vat": {"min": 0, "max": layout.MAX_VAT, "charset": "text"},
    "payment": {"min": 0, "max": layout.MAX_PAY, "charset": "text"},
    "total": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
}

ITEM_FIELDS = {
    "sku": {"min": 0, "max": layout.MAX_SKU, "charset": "upper"},
    "desc": {"min": 0, "max": layout.MAX_DESC, "charset": "desc"},
    "qte": {"min": 0, "max": layout.MAX_QTE, "charset": "qty"},
    "brut": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
    "remise": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
    "tva": {"min": 0, "max": layout.MAX_TVA, "charset": "tva"},
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
    text = _raw(value).strip()
    match = re.match(r"^(\d{1,2})[./-](\d{1,2})[./-](\d{2,4})$", text)
    if match:
        day, month, year = int(match.group(1)), int(match.group(2)), match.group(3)
        if len(year) == 2:
            year = "20" + year
        return f"{day}/{month}/{int(year)}"
    digits = re.sub(r"\D", "", text)[:8]
    if len(digits) == 8:
        return f"{int(digits[:2])}/{int(digits[2:4])}/{int(digits[4:])}"
    return text[: layout.MAX_DATE]


def parse_money(value) -> float:
    text = _raw(value).strip().replace("\u00a0", " ").replace(" ", "").replace("€", "")
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
    return f"{round(value, 2):.2f}".replace(".", ",")


def format_euro(value: float) -> str:
    return format_money(value) + " €"


def format_qty(value: float) -> str:
    return f"{round(value, 2):.2f}"


def format_qty_int(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return format_qty(value)


def format_tva(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return format_money(value)


def line_amounts(item):
    qte = parse_qty(getattr(item, "qte", 0))
    brut = parse_money(getattr(item, "brut", 0))
    remise = parse_money(getattr(item, "remise", 0))
    tva_pct = parse_money(getattr(item, "tva", layout.TVA_RATE))
    ttc_unit = round(brut - remise, 2)
    rate = tva_pct / 100.0
    ht_unit = round(ttc_unit / (1.0 + rate), 2) if rate != -1 else ttc_unit
    line_ttc = round(ttc_unit * qte, 2)
    line_ht = round(ht_unit * qte, 2)
    return qte, brut, remise, ht_unit, line_ttc, line_ht, tva_pct


def invoice_totals(items) -> tuple[float, float, float]:
    hors = 0.0
    ttc = 0.0
    for item in items or ():
        _qte, _brut, _remise, _ht, line_ttc, line_ht, _tva = line_amounts(item)
        hors += line_ht
        ttc += line_ttc
    hors = round(hors, 2)
    ttc = round(ttc, 2)
    return hors, round(ttc - hors, 2), ttc


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
    elif charset == "tva":
        text = format_tva(parse_money(text) if text.strip() else layout.TVA_RATE)
    elif charset == "desc":
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        return text[: spec["max"]]
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
    prenom = str(out.get("prenom") or "").strip()
    nom = str(out.get("nom") or "").strip()
    if prenom and nom:
        out["nom"] = f"{nom} {prenom}" if prenom not in nom else nom
    elif prenom:
        out["nom"] = prenom
    df = str(out.get("date_facture") or "").strip()
    if df:
        if not str(out.get("date_envoi") or "").strip():
            out["date_envoi"] = df
        if not str(out.get("date_echeance") or "").strip():
            out["date_echeance"] = df
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
