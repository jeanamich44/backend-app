import re

from . import layout

_FALSE = {"", "0", "false", "off", "no", "n"}
_TRUE = {"1", "true", "on", "yes", "y"}

FIELDS = {
    "nom": {"min": 0, "max": layout.MAX_NOM, "charset": "text"},
    "adresse": {"min": 0, "max": layout.MAX_ADRESSE, "charset": "text"},
    "cp_ville": {"min": 0, "max": layout.MAX_CP_VILLE, "charset": "text"},
    "pays": {"min": 0, "max": layout.MAX_PAYS, "charset": "text"},
    "livraison_nom": {"min": 0, "max": layout.MAX_NOM, "charset": "text"},
    "livraison_extra": {"min": 0, "max": layout.MAX_EXTRA, "charset": "text"},
    "livraison_adresse": {"min": 0, "max": layout.MAX_ADRESSE, "charset": "text"},
    "livraison_cp_ville": {"min": 0, "max": layout.MAX_CP_VILLE, "charset": "text"},
    "livraison_pays": {"min": 0, "max": layout.MAX_PAYS, "charset": "text"},
    "livraison_mode": {"min": 0, "max": 16, "charset": "mode"},
    "magasin_nom": {"min": 0, "max": layout.MAX_MAGASIN, "charset": "text"},
    "num_client": {"min": 0, "max": layout.MAX_REF, "charset": "text"},
    "num_commande": {"min": 0, "max": layout.MAX_REF, "charset": "text"},
    "num_facture": {"min": 0, "max": layout.MAX_REF, "charset": "text"},
    "date_commande": {"min": 0, "max": layout.MAX_DATE, "charset": "date"},
    "date_facture": {"min": 0, "max": layout.MAX_DATE, "charset": "date"},
    "payment": {"min": 0, "max": layout.MAX_PAY, "charset": "text"},
    "remise": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
    "port": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
    "total": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
}

ITEM_FIELDS = {
    "sku": {"min": 0, "max": layout.MAX_SKU, "charset": "text"},
    "desc": {"min": 0, "max": layout.MAX_DESC, "charset": "text"},
    "couleur": {"min": 0, "max": layout.MAX_ATTR, "charset": "text"},
    "taille": {"min": 0, "max": layout.MAX_ATTR, "charset": "text"},
    "qte": {"min": 0, "max": layout.MAX_QTE, "charset": "qty"},
    "pu": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
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


def clean_mode(value) -> str:
    text = _raw(value).strip().lower()
    if any(k in text for k in ("magasin", "store", "shop")):
        return layout.MODE_MAGASIN
    if any(k in text for k in ("domicile", "24h", "express", "home")):
        return layout.MODE_DOMICILE
    return layout.MODE_CHRONO


def clean_date(value) -> str:
    text = _raw(value).strip()
    match = re.match(r"^(\d{1,2})[./-](\d{1,2})[./-](\d{2,4})$", text)
    if match:
        day, month, year = int(match.group(1)), int(match.group(2)), match.group(3)
        if len(year) == 2:
            year = "20" + year
        return f"{day:02d}/{month:02d}/{int(year)}"
    digits = re.sub(r"\D", "", text)[:8]
    if len(digits) == 8:
        return f"{int(digits[:2]):02d}/{int(digits[2:4]):02d}/{int(digits[4:])}"
    return text[: layout.MAX_DATE]


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


def parse_qty(value) -> float:
    return parse_money(value)


def format_money(value: float) -> str:
    return f"{round(value, 2):.2f}".replace(".", ",")


def format_euro(value: float) -> str:
    value = round(value, 2)
    if value == int(value):
        return f"{int(value)} €"
    return format_money(value) + " €"


def format_qty(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return format_money(value)


def format_tva(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return format_money(value)


def format_tva_line(value: float) -> str:
    return format_tva(value) + "%"


def format_total_amount(value: float, bold: bool = False) -> str:
    text = format_euro(value)
    return (" " + text) if bold else text


def clean(field_id: str, value, spec=None) -> str:
    spec = spec or FIELDS.get(field_id) or ITEM_FIELDS.get(field_id) or {
        "max": 80, "charset": "text",
    }
    text = _raw(value)
    charset = spec.get("charset")
    if field_id == "num_facture":
        text = re.sub(r"^(?:FAC(?:TURE)?\s*(?:N°?)?\s*[-:]?\s*)", "", text, flags=re.IGNORECASE).strip()
    elif field_id == "num_commande":
        text = re.sub(r"^(?:CMD\s*[-:]?\s*)", "", text, flags=re.IGNORECASE).strip()
    elif field_id == "num_client":
        text = re.sub(r"^(?:CLI(?:ENT)?\s*[-:]?\s*)", "", text, flags=re.IGNORECASE).strip()
    if charset == "date":
        text = clean_date(text)
    elif charset == "mode":
        text = clean_mode(text)
    elif charset == "money":
        text = format_money(parse_money(text)) if text.strip() else ""
    elif charset == "qty":
        text = format_qty(parse_qty(text)) if text.strip() else ""
    elif charset == "tva":
        text = format_tva(parse_money(text) if text.strip() else layout.TVA_RATE)
    else:
        text = text.replace("\r", "").replace("\n", " ").strip()
    return text[: spec["max"]]


def line_cost(item) -> tuple[float, float, float]:
    qte = parse_qty(getattr(item, "qte", 0))
    pu = parse_money(getattr(item, "pu", 0))
    return qte, pu, round(qte * pu, 2)


def line_tva_rate(item) -> float:
    raw = getattr(item, "tva", "") or ""
    if str(raw).strip():
        return parse_money(raw)
    return float(layout.TVA_RATE)


def invoice_totals(card) -> tuple[float, float, float, float, float, float]:
    ht = 0.0
    tva_amt = 0.0
    for item in getattr(card, "items", ()) or ():
        _qte, _pu, line = line_cost(item)
        ht += line
        tva_amt += round(line * line_tva_rate(item) / 100.0, 2)
    ht = round(ht, 2)
    tva_amt = round(tva_amt, 2)
    ttc = round(ht + tva_amt, 2)
    remise = parse_money(getattr(card, "remise", 0))
    port = parse_money(getattr(card, "port", 0))
    due = round(ttc - remise + port, 2)
    if ttc:
        dont = round(tva_amt * max(0.0, ttc - remise) / ttc, 2)
    else:
        dont = 0.0
    return ht, ttc, remise, port, due, dont


def clean_item(item: dict) -> dict:
    item = as_dict(item)
    return {key: clean(key, item.get(key, ""), spec) for key, spec in ITEM_FIELDS.items()}


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


def ship_lines(card) -> tuple:
    mode = (getattr(card, "livraison_mode", "") or "").strip().lower()
    if mode == layout.MODE_MAGASIN:
        raw = (
            getattr(card, "magasin_nom", "") or "",
            getattr(card, "livraison_nom", "") or "",
            getattr(card, "livraison_adresse", "") or "",
            getattr(card, "livraison_cp_ville", "") or "",
            getattr(card, "livraison_pays", "") or "",
        )
    elif mode == layout.MODE_DOMICILE:
        raw = (
            getattr(card, "livraison_nom", "") or "",
            getattr(card, "livraison_adresse", "") or "",
            getattr(card, "livraison_extra", "") or "",
            getattr(card, "livraison_cp_ville", "") or "",
            getattr(card, "livraison_pays", "") or "",
        )
    else:
        raw = (
            getattr(card, "livraison_extra", "") or getattr(card, "magasin_nom", "") or "",
            getattr(card, "livraison_nom", "") or "",
            getattr(card, "livraison_adresse", "") or "",
            getattr(card, "livraison_cp_ville", "") or "",
            getattr(card, "livraison_pays", "") or "",
        )
    return tuple(line for line in raw if line)


def bill_lines(card) -> tuple:
    return tuple(
        line for line in (
            getattr(card, "nom", "") or "",
            getattr(card, "adresse", "") or "",
            getattr(card, "cp_ville", "") or "",
            getattr(card, "pays", "") or "",
        ) if line
    )
