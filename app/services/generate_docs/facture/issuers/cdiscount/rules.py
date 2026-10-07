"""Règles preuve d'achat Cdiscount : dates JJ/MM/AAAA."""

import re

from . import copy as texts
from . import layout

_FALSE = {"", "0", "false", "off", "no", "n"}
_TRUE = {"1", "true", "on", "yes", "y"}

FIELDS = {
    "nom": {"min": 0, "max": layout.MAX_NOM, "charset": "text"},
    "adresse": {"min": 0, "max": layout.MAX_ADRESSE, "charset": "text"},
    "cp_ville": {"min": 0, "max": layout.MAX_CP_VILLE, "charset": "text"},
    "livraison_nom": {"min": 0, "max": layout.MAX_NOM, "charset": "text"},
    "livraison_adresse": {"min": 0, "max": layout.MAX_ADRESSE, "charset": "text"},
    "livraison_cp_ville": {"min": 0, "max": layout.MAX_CP_VILLE, "charset": "text"},
    "num_commande": {"min": 0, "max": layout.MAX_REF, "charset": "text"},
    "date_commande": {"min": 0, "max": layout.MAX_DATE, "charset": "date"},
    "payment": {"min": 0, "max": layout.MAX_PAY, "charset": "text"},
    "port": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
    "vendeur": {"min": 0, "max": layout.MAX_VENDEUR, "charset": "text"},
    "immat": {"min": 0, "max": layout.MAX_IMMAT, "charset": "text"},
    "total": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
}

ITEM_FIELDS = {
    "desc": {"min": 0, "max": layout.MAX_DESC, "charset": "text"},
    "qte": {"min": 0, "max": layout.MAX_QTE, "charset": "qty"},
    "montant": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
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
        return f"{day:02d}/{month:02d}/{int(year)}"
    digits = re.sub(r"\D", "", text)[:8]
    if len(digits) == 8:
        return f"{int(digits[:2]):02d}/{int(digits[2:4]):02d}/{int(digits[4:])}"
    return text[: layout.MAX_DATE]


def parse_money(value) -> float:
    text = _raw(value).strip().replace("\u00a0", " ").replace(" ", "")
    text = text.replace("€", "").replace("Eur", "").replace("EUR", "")
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
    return f"{round(value, 2):.2f}".replace(".", ",")


def format_eur(value: float) -> str:
    return format_money(value) + " Eur"


def format_qty(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return format_money(value)


def items_total(items) -> float:
    return round(
        sum(parse_money(getattr(item, "montant", 0)) for item in items or ()),
        2,
    )


def clean_item(item: dict) -> dict:
    item = as_dict(item)
    return {key: clean(key, item.get(key, ""), spec) for key, spec in ITEM_FIELDS.items()}


def clean(field_id: str, value, spec=None) -> str:
    spec = spec or FIELDS.get(field_id) or ITEM_FIELDS.get(field_id) or {
        "max": 80, "charset": "text",
    }
    text = _raw(value)
    charset = spec.get("charset")
    if charset == "date":
        text = clean_date(text)
    elif charset == "money":
        text = format_money(parse_money(text)) if text.strip() else ""
    elif charset == "qty":
        text = format_qty(parse_money(text)) if text.strip() else ""
    else:
        text = text.replace("\r", "").replace("\n", " ").strip()
    return text[: spec["max"]]


def apply_payload(data: dict) -> dict:
    data = as_dict(data)
    out = dict(data)
    for field_id in FIELDS:
        if field_id in out and not isinstance(out[field_id], bool):
            out[field_id] = clean(field_id, out[field_id])
    if "sold_by_cdiscount" in out:
        out["sold_by_cdiscount"] = as_bool(out["sold_by_cdiscount"], True)
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
    doc.card.sold_by_cdiscount = as_bool(getattr(doc.card, "sold_by_cdiscount", True), True)
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


def format_titulaire(name: str) -> str:
    """M. + prénom nom en minuscules (casse gabarit, pas celle de la rue)."""
    text = re.sub(r"\s+", " ", _raw(name)).strip()
    text = re.sub(r"^(m\.|mr\.?|monsieur)\s+", "", text, flags=re.I)
    text = text.lower()
    if not text:
        return ""
    return texts.CIVILITY + text


def format_street(value: str) -> str:
    """Rue / CP-ville : CAPITALES gabarit, pas la casse du titulaire."""
    return _raw(value).upper()


def titulaire_lines(name: str, split_nom: bool) -> tuple:
    """Facturation = une ligne. Livraison gabarit = M. prénom / nom."""
    text = format_titulaire(name)
    if not text:
        return ()
    if not split_nom:
        return (text,)
    rest = text[len(texts.CIVILITY):] if text.startswith(texts.CIVILITY) else text
    parts = rest.split(None, 1)
    if len(parts) == 2:
        return (texts.CIVILITY + parts[0], parts[1])
    return (text,)


def addr_ys(name_lines: tuple) -> tuple:
    """Après le nom : 1 ligne vide puis rue, 2 lignes vides puis CP."""
    y = layout.ADDR_Y0
    pitch = layout.ADDR_PITCH
    n = max(len(name_lines), 1)
    street = y + n * pitch + pitch
    cp = street + 3 * pitch
    return street, cp
