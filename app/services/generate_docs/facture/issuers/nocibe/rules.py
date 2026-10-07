import re
from . import layout

# ----------------------------------------------------------------------

_FALSE = {"", "0", "false", "off", "no", "n"}
_TRUE = {"1", "true", "on", "yes", "y"}

# ----------------------------------------------------------------------

BLOCKS = {
    "header": True,
    "header_logo": True,
    "header_titre": True,
    "header_facturation": True,
    "header_livraison": True,
    "header_commande": True,
    "middle": True,
    "middle_table": True,
    "middle_totals": True,
    "middle_details": True,
}

# ----------------------------------------------------------------------

FIELDS = {
    "facture_num": {"min": 0, "max": 35, "charset": "text"},
    "date_emission": {"min": 0, "max": 30, "charset": "text"},
    "facturation_titre": {"min": 0, "max": 40, "charset": "text"},
    "nom": {"min": 0, "max": 35, "charset": "text"},
    "prenom": {"min": 0, "max": 35, "charset": "text"},
    "adresse": {"min": 0, "max": 80, "charset": "text"},
    "cp": {"min": 0, "max": 10, "charset": "text"},
    "ville": {"min": 0, "max": 40, "charset": "text"},
    "pays": {"min": 0, "max": 30, "charset": "text"},
    "client_nom": {"min": 0, "max": 35, "charset": "text"},
    "client_rue": {"min": 0, "max": 80, "charset": "text"},
    "client_ville": {"min": 0, "max": 45, "charset": "text"},
    "client_pays": {"min": 0, "max": 30, "charset": "text"},
    "livraison_titre": {"min": 0, "max": 40, "charset": "text"},
    "livraison_nom": {"min": 0, "max": 35, "charset": "text"},
    "livraison_prenom": {"min": 0, "max": 35, "charset": "text"},
    "livraison_adresse": {"min": 0, "max": 80, "charset": "text"},
    "livraison_cp": {"min": 0, "max": 10, "charset": "text"},
    "livraison_rue": {"min": 0, "max": 80, "charset": "text"},
    "livraison_ville": {"min": 0, "max": 45, "charset": "text"},
    "livraison_pays": {"min": 0, "max": 30, "charset": "text"},
    "commande_date": {"min": 0, "max": 50, "charset": "text"},
    "commande_mode": {"min": 0, "max": 65, "charset": "text"},
    "commande_expedition": {"min": 0, "max": 60, "charset": "text"},
    "commande_etat": {"min": 0, "max": 40, "charset": "text"},
    "total_ht": {"min": 0, "max": 20, "charset": "money"},
    "total_tva": {"min": 0, "max": 20, "charset": "money"},
    "total_ttc": {"min": 0, "max": 20, "charset": "money"},
    "tva_rate_pct": {"min": 0, "max": 15, "charset": "text"},
    "tva_base_ht": {"min": 0, "max": 20, "charset": "money"},
    "tva_montant": {"min": 0, "max": 20, "charset": "money"},
    "reglement_date": {"min": 0, "max": 25, "charset": "text"},
    "reglement_mode": {"min": 0, "max": 30, "charset": "text"},
    "reglement_montant": {"min": 0, "max": 20, "charset": "money"},
}

# ----------------------------------------------------------------------

ITEM_FIELDS = {
    "ref": {"min": 0, "max": 15, "charset": "text"},
    "desc": {"min": 0, "max": 80, "charset": "text"},
    "tva_rate": {"min": 0, "max": 15, "charset": "text"},
    "qty": {"min": 0, "max": 10, "charset": "digits"},
    "unit_price": {"min": 0, "max": 15, "charset": "money"},
    "remise": {"min": 0, "max": 15, "charset": "money"},
    "remise_code": {"min": 0, "max": 45, "charset": "text"},
    "net_ht": {"min": 0, "max": 15, "charset": "money"},
}

# ----------------------------------------------------------------------

_DOC_ATTR = {key: ("card", key) for key in FIELDS}
_ITEM_KEYS = tuple(ITEM_FIELDS)

# ----------------------------------------------------------------------

def as_dict(data) -> dict:
    return data if isinstance(data, dict) else {}

# ----------------------------------------------------------------------

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

# ----------------------------------------------------------------------

def flag(data: dict, key: str, default: bool = True) -> bool:
    if key not in data:
        return default
    return as_bool(data[key], default)

# ----------------------------------------------------------------------

def _raw(value) -> str:
    if value is None or isinstance(value, bool):
        return ""
    if isinstance(value, (int, float)):
        return str(value)
    return str(value) if isinstance(value, str) else ""

# ----------------------------------------------------------------------

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

# ----------------------------------------------------------------------

def parse_qty(value) -> int:
    try:
        return max(1, int(float(parse_money(value))))
    except (ValueError, TypeError):
        return 1

# ----------------------------------------------------------------------

def format_money(value: float) -> str:
    return f"{value:.2f}"

# ----------------------------------------------------------------------

def clean(field_id: str, value, spec=None) -> str:
    spec = spec or FIELDS.get(field_id) or {"max": 80, "charset": "text"}
    text = _raw(value)
    charset = spec.get("charset")
    if charset == "digits":
        text = re.sub(r"[^\d]", "", text)
    elif charset == "upper":
        text = re.sub(r"\s+", " ", text).strip().upper()
    elif charset == "money":
        text = text.replace("\r", "").replace("\n", " ").strip()
    else:
        text = text.replace("\r", "")
    return text[: spec["max"]]

# ----------------------------------------------------------------------

def clean_item(item: dict) -> dict:
    item = as_dict(item)
    out = {}
    for key, spec in ITEM_FIELDS.items():
        out[key] = clean(key, item.get(key, ""), spec)
    return out

# ----------------------------------------------------------------------

def compute_item_net(item: dict) -> str:
    explicit = str(item.get("net_ht", "")).strip()
    if explicit:
        return explicit
    qty = parse_qty(item.get("qty", 1))
    price = parse_money(item.get("unit_price", item.get("price", 0.0)))
    remise = parse_money(item.get("remise", 0.0))
    calc = (qty * price) - remise
    return format_money(calc)

# ----------------------------------------------------------------------

def compute_totals(items: list, total_ht=None, total_tva=None, total_ttc=None) -> dict:
    if total_ht is not None and total_tva is not None and total_ttc is not None:
        ht_str = str(total_ht).strip()
        tva_str = str(total_tva).strip()
        ttc_str = str(total_ttc).strip()
        return {
            "total_ht": ht_str,
            "total_tva": tva_str,
            "total_ttc": ttc_str,
            "tva_base_ht": ht_str.replace(",", "."),
            "tva_montant": tva_str,
            "reglement_montant": ttc_str,
        }
    sum_net = sum(parse_money(compute_item_net(it if isinstance(it, dict) else it.__dict__)) for it in items)
    calc_tva = sum_net * 0.20
    calc_ttc = sum_net + calc_tva
    return {
        "total_ht": format_money(sum_net).replace(".", ","),
        "total_tva": format_money(calc_tva),
        "total_ttc": format_money(calc_ttc),
        "tva_base_ht": format_money(sum_net),
        "tva_montant": format_money(calc_tva),
        "reglement_montant": format_money(calc_ttc),
    }

# ----------------------------------------------------------------------

def field_issue(field_id: str, value) -> str | None:
    spec = FIELDS.get(field_id)
    if spec is None:
        return None
    cleaned = clean(field_id, value, spec)
    min_len = spec.get("min", 0)
    if len(cleaned) < min_len:
        return "min"
    return None

# ----------------------------------------------------------------------

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

# ----------------------------------------------------------------------

def apply_payload(data: dict) -> dict:
    data = as_dict(data)
    out = dict(data)
    for field_id in FIELDS:
        if field_id in out and not isinstance(out[field_id], bool):
            out[field_id] = clean(field_id, out[field_id])
    raw_items = out.get("items")
    if isinstance(raw_items, list):
        cleaned_items = []
        for it in raw_items[: layout.MAX_ROWS]:
            if isinstance(it, dict):
                cleaned_items.append(clean_item(it))
        out["items"] = cleaned_items
    return out

# ----------------------------------------------------------------------

def apply_doc(doc):
    for field_id, (group, attr) in _DOC_ATTR.items():
        obj = getattr(doc, group)
        if hasattr(obj, attr):
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

# ----------------------------------------------------------------------

def public_rules() -> dict:
    return {
        "blocks": BLOCKS,
        "fields": {
            field_id: {"min": spec["min"], "max": spec["max"], "charset": spec["charset"]}
            for field_id, spec in FIELDS.items()
        },
        "item_fields": {
            key: {"min": spec["min"], "max": spec["max"], "charset": spec["charset"]}
            for key, spec in ITEM_FIELDS.items()
        },
    }

# ----------------------------------------------------------------------

def public_limits() -> dict:
    limits = {field_id: spec["max"] for field_id, spec in FIELDS.items()}
    limits["max_rows"] = layout.MAX_ROWS
    limits["max_items"] = layout.MAX_ROWS
    limits.update({f"item_{key}": spec["max"] for key, spec in ITEM_FIELDS.items()})
    return limits

# ----------------------------------------------------------------------

LIMITS = public_limits()
