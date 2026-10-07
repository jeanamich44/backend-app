"""Règles facture Amazon : longueurs, dates libres, montants HT/TTC indépendants."""

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
    "seller_nom": {"min": 0, "max": layout.MAX_SELLER, "charset": "text"},
    "seller_adresse": {"min": 0, "max": layout.MAX_ADRESSE, "charset": "text"},
    "seller_adresse2": {"min": 0, "max": layout.MAX_ADRESSE, "charset": "text"},
    "seller_cp_ville": {"min": 0, "max": layout.MAX_VILLE, "charset": "text"},
    "seller_pays": {"min": 0, "max": layout.MAX_PAYS, "charset": "text"},
    "seller_tva": {"min": 0, "max": layout.MAX_TVA, "charset": "upper"},
    "payment_ref": {"min": 0, "max": layout.MAX_REF, "charset": "upper"},
    "num_facture": {"min": 0, "max": layout.MAX_REF, "charset": "upper"},
    "date_facture": {"min": 0, "max": layout.MAX_DATE, "charset": "text"},
    "total": {"min": 0, "max": layout.MAX_MONEY, "charset": "money_eur"},
    "num_commande": {"min": 0, "max": layout.MAX_REF, "charset": "upper"},
    "date_commande": {"min": 0, "max": layout.MAX_DATE, "charset": "text"},
    "expedition_ht": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
    "expedition_ttc": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
    "remise_ht": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
    "remise_ttc": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
    "tva_rate": {"min": 0, "max": 8, "charset": "text"},
}

ITEM_FIELDS = {
    "nom": {"min": 0, "max": layout.MAX_PRODUIT, "charset": "text"},
    "note": {"min": 0, "max": layout.MAX_NOTE, "charset": "text"},
    "qte": {"min": 0, "max": layout.MAX_QTE, "charset": "qty"},
    "pu_ht": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
    "pu_ttc": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
    "asin": {"min": 0, "max": layout.MAX_ASIN, "charset": "upper"},
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


def parse_money(value) -> float:
    text = _raw(value).strip().replace("\u00a0", " ").replace("€", "")
    text = text.replace(" ", "")
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
    return f"{value:.2f}".replace(".", ",")


def format_money_eur(value: float) -> str:
    return f"{format_money(value)} €"


def parse_qty(value) -> float:
    return parse_money(value)


def format_qty(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return format_money(value)


def line_amounts(item):
    qte = parse_qty(getattr(item, "qte", 0))
    ht = parse_money(getattr(item, "pu_ht", 0))
    ttc = parse_money(getattr(item, "pu_ttc", 0))
    return qte, ht, ttc, qte * ht, qte * ttc


def items_ht(items) -> float:
    total = 0.0
    for item in items or ():
        _qte, _ht, _ttc, line_ht, _line_ttc = line_amounts(item)
        total += line_ht
    return total


def items_ttc(items) -> float:
    total = 0.0
    for item in items or ():
        _qte, _ht, _ttc, _line_ht, line_ttc = line_amounts(item)
        total += line_ttc
    return total


def extras_ht(card) -> float:
    return parse_money(getattr(card, "expedition_ht", 0)) + parse_money(getattr(card, "remise_ht", 0))


def extras_ttc(card) -> float:
    return parse_money(getattr(card, "expedition_ttc", 0)) + parse_money(getattr(card, "remise_ttc", 0))


def grand_total(card) -> float:
    return items_ttc(getattr(card, "items", ())) + extras_ttc(card)


def recap_ht(card) -> float:
    return items_ht(getattr(card, "items", ())) + extras_ht(card)


def recap_tva(card) -> float:
    return grand_total(card) - recap_ht(card)


def has_remise(card) -> bool:
    return abs(parse_money(getattr(card, "remise_ht", 0))) > 0 or abs(
        parse_money(getattr(card, "remise_ttc", 0))
    ) > 0


def sold_by_amazon(card) -> bool:
    return as_bool(getattr(card, "sold_by_amazon", True), True)


FOOTER_EU = "eu"
FOOTER_OSS = "oss"


def footer_kind(card) -> str:
    """Footer figé à la création de chaque page : EU si vendu par Amazon, OSS sinon."""
    return FOOTER_EU if sold_by_amazon(card) else FOOTER_OSS


def tva_label(card) -> str:
    text = (_raw(getattr(card, "tva_rate", "")) or "").strip()
    if not text:
        return f"{layout.TVA_RATE} %"
    if "%" in text:
        return text
    return f"{text} %"


def clean(field_id: str, value, spec=None) -> str:
    spec = spec or FIELDS.get(field_id) or {"max": 80, "charset": "text"}
    text = _raw(value)
    charset = spec.get("charset")
    if charset == "upper":
        text = re.sub(r"\s+", " ", text).strip().upper()
    elif charset == "money":
        text = format_money(parse_money(text)) if text.strip() else ""
    elif charset == "money_eur":
        text = format_money_eur(parse_money(text)) if text.strip() else ""
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
    if "sold_by_amazon" in out:
        out["sold_by_amazon"] = as_bool(out["sold_by_amazon"], True)
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
    doc.card.sold_by_amazon = as_bool(getattr(doc.card, "sold_by_amazon", True), True)
    cleaned = []
    for item in getattr(doc.card, "items", ())[: layout.MAX_ROWS]:
        payload = {key: getattr(item, key, "") for key in _ITEM_KEYS}
        data = clean_item(payload)
        for key, value in data.items():
            setattr(item, key, value)
        cleaned.append(item)
    doc.card.items = cleaned
    if not getattr(doc.card, "total", None):
        doc.card.total = format_money_eur(grand_total(doc.card))
    else:
        doc.card.total = clean("total", doc.card.total)
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
