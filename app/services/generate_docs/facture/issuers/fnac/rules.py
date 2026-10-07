"""Règles facture Fnac : canal magasin/en ligne, HT/TTC indépendants."""

import re

from . import copy as texts
from . import layout

_FALSE = {"", "0", "false", "off", "no", "n"}
_TRUE = {"1", "true", "on", "yes", "y"}

FIELDS = {
    "livraison_email": {"min": 0, "max": layout.MAX_EMAIL, "charset": "text"},
    "livraison_nom": {"min": 0, "max": layout.MAX_NOM, "charset": "text"},
    "livraison_adresse": {"min": 0, "max": layout.MAX_ADRESSE, "charset": "text"},
    "livraison_cp_ville": {"min": 0, "max": layout.MAX_VILLE, "charset": "text"},
    "livraison_pays": {"min": 0, "max": layout.MAX_PAYS, "charset": "text"},
    "facturation_email": {"min": 0, "max": layout.MAX_EMAIL, "charset": "text"},
    "facturation_nom": {"min": 0, "max": layout.MAX_NOM, "charset": "text"},
    "facturation_adresse": {"min": 0, "max": layout.MAX_ADRESSE, "charset": "text"},
    "facturation_cp_ville": {"min": 0, "max": layout.MAX_VILLE, "charset": "text"},
    "facturation_pays": {"min": 0, "max": layout.MAX_PAYS, "charset": "text"},
    "store_nom": {"min": 0, "max": layout.MAX_STORE, "charset": "text"},
    "store_l1": {"min": 0, "max": layout.MAX_STORE, "charset": "text"},
    "store_l2": {"min": 0, "max": layout.MAX_STORE, "charset": "text"},
    "store_l3": {"min": 0, "max": layout.MAX_STORE, "charset": "text"},
    "num_commande": {"min": 0, "max": layout.MAX_REF, "charset": "upper"},
    "date_commande": {"min": 0, "max": layout.MAX_DATE, "charset": "text"},
    "num_facture": {"min": 0, "max": layout.MAX_REF, "charset": "upper"},
    "date_facture": {"min": 0, "max": layout.MAX_DATE, "charset": "text"},
    "nref": {"min": 0, "max": layout.MAX_NREF, "charset": "text"},
    "matricule": {"min": 0, "max": layout.MAX_MAT, "charset": "text"},
    "payment_mode": {"min": 0, "max": layout.MAX_PAY, "charset": "text"},
    "echeance": {"min": 0, "max": layout.MAX_DATE, "charset": "text"},
    "tva_code": {"min": 0, "max": layout.MAX_CODE, "charset": "upper"},
    "tva_rate": {"min": 0, "max": 8, "charset": "text"},
    "frais_ht": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
    "tva_frais": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
    "pays_expedition": {"min": 0, "max": 160, "charset": "text"},
    "total": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
}

ITEM_FIELDS = {
    "nom": {"min": 0, "max": layout.MAX_PRODUIT, "charset": "text"},
    "subtitle": {"min": 0, "max": layout.MAX_NOTE, "charset": "text"},
    "ean": {"min": 0, "max": layout.MAX_EAN, "charset": "text"},
    "reference": {"min": 0, "max": layout.MAX_REF, "charset": "text"},
    "qte": {"min": 0, "max": layout.MAX_QTE, "charset": "qty"},
    "pu_ht": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
    "pu_ttc": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
    "pu_brut_ht": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
    "remise_ht": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
    "serial": {"min": 0, "max": layout.MAX_NOTE, "charset": "text"},
    "distribution": {"min": 0, "max": layout.MAX_NOTE, "charset": "text"},
    "pieces": {"min": 0, "max": layout.MAX_NOTE, "charset": "text"},
    "garantie": {"min": 0, "max": layout.MAX_NOTE, "charset": "text"},
    "eco_ht": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
    "eco_ttc": {"min": 0, "max": layout.MAX_MONEY, "charset": "money"},
}

_DOC_ATTR = {key: ("card", key) for key in FIELDS}
_ITEM_KEYS = tuple(ITEM_FIELDS)

FOOTER_WEB = "web"
FOOTER_MAG = "magasin"


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
    return f"{value:.2f}"


def format_amount(value: float, en_ligne: bool) -> str:
    body = format_money(value)
    return f"{body}€" if en_ligne else f"{body} €"


def parse_qty(value) -> float:
    return parse_money(value)


def format_qty(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return format_money(value)


def en_ligne(card) -> bool:
    return as_bool(getattr(card, "en_ligne", True), True)


def footer_kind(card) -> str:
    return FOOTER_WEB if en_ligne(card) else FOOTER_MAG


def line_amounts(item):
    qte = parse_qty(getattr(item, "qte", 0))
    ht = parse_money(getattr(item, "pu_ht", 0))
    ttc = parse_money(getattr(item, "pu_ttc", 0))
    return qte, ht, ttc, qte * ht, qte * ttc


def items_ht(items) -> float:
    total = 0.0
    for item in items or ():
        total += line_amounts(item)[3]
    return total


def items_ttc(items) -> float:
    total = 0.0
    for item in items or ():
        total += line_amounts(item)[4]
    return total


def eco_ht(items) -> float:
    total = 0.0
    for item in items or ():
        qte = parse_qty(getattr(item, "qte", 0))
        total += qte * parse_money(getattr(item, "eco_ht", 0))
    return total


def eco_ttc(items) -> float:
    total = 0.0
    for item in items or ():
        qte = parse_qty(getattr(item, "qte", 0))
        total += qte * parse_money(getattr(item, "eco_ttc", 0))
    return total


def has_remise(item) -> bool:
    return abs(parse_money(getattr(item, "remise_ht", 0))) > 0


def has_eco(item) -> bool:
    return abs(parse_money(getattr(item, "eco_ht", 0))) > 0 or abs(
        parse_money(getattr(item, "eco_ttc", 0))
    ) > 0


def frais_ht(card) -> float:
    return eco_ht(getattr(card, "items", ())) + parse_money(getattr(card, "frais_ht", 0))


def tva_frais(card) -> float:
    eco = eco_ttc(getattr(card, "items", ())) - eco_ht(getattr(card, "items", ()))
    return eco + parse_money(getattr(card, "tva_frais", 0))


def recap_ht(card) -> float:
    return items_ht(getattr(card, "items", ()))


def recap_ttc(card) -> float:
    return items_ttc(getattr(card, "items", ()))


def recap_tva(card) -> float:
    return recap_ttc(card) - recap_ht(card)


def grand_total(card) -> float:
    return recap_ttc(card)


def tva_row_label(card) -> str:
    code = (_raw(getattr(card, "tva_code", "")) or texts.TVA_CODE_WEB).strip()
    rate = (_raw(getattr(card, "tva_rate", "")) or texts.TVA_RATE).strip()
    if not rate.endswith("%"):
        if "." not in rate and rate:
            rate = f"{parse_money(rate):.2f}%"
        elif rate:
            rate = f"{rate}%" if "%" not in rate else rate
        else:
            rate = f"{texts.TVA_RATE}%"
    return f"{code} - {rate}"


def barcode_value(card) -> str:
    from . import barcode as code39
    return code39.payload(_raw(getattr(card, "num_facture", "")))


def clean(field_id: str, value, spec=None) -> str:
    spec = spec or FIELDS.get(field_id) or {"max": 80, "charset": "text"}
    text = _raw(value)
    charset = spec.get("charset")
    if charset == "upper":
        text = re.sub(r"\s+", " ", text).strip().upper()
    elif charset == "digits":
        text = re.sub(r"\D", "", text)
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
    pu_ttc_val = parse_money(out.get("pu_ttc", 0))
    pu_ht_val = parse_money(out.get("pu_ht", 0))
    if pu_ttc_val > 0 and pu_ht_val == 0:
        pu_ht_val = round(pu_ttc_val / 1.20, 2)
        out["pu_ht"] = format_money(pu_ht_val)
    elif pu_ht_val > 0 and pu_ttc_val == 0:
        pu_ttc_val = round(pu_ht_val * 1.20, 2)
        out["pu_ttc"] = format_money(pu_ttc_val)
    rem_val = parse_money(out.get("remise_ht", 0))
    brut_val = parse_money(out.get("pu_brut_ht", 0))
    if rem_val > 0 and brut_val == 0 and pu_ht_val > 0:
        out["pu_brut_ht"] = format_money(pu_ht_val + rem_val)
    elif brut_val == 0 and pu_ht_val > 0:
        out["pu_brut_ht"] = format_money(pu_ht_val)
    eco_ht_val = parse_money(out.get("eco_ht", 0))
    eco_ttc_val = parse_money(out.get("eco_ttc", 0))
    if eco_ht_val > 0 and eco_ttc_val == 0:
        out["eco_ttc"] = format_money(round(eco_ht_val * 1.20, 2))
    elif eco_ttc_val > 0 and eco_ht_val == 0:
        out["eco_ht"] = format_money(round(eco_ttc_val / 1.20, 2))
    return out


def apply_payload(data: dict) -> dict:
    data = as_dict(data)
    out = dict(data)
    p = str(data.get("prenom") or "").strip()
    n = str(data.get("nom") or "").strip()
    if p and n:
        gen_nom = n if p in n else f"{n} {p}"
    else:
        gen_nom = n or p

    lp = str(data.get("livraison_prenom") or p).strip()
    ln = str(data.get("livraison_nom") or gen_nom).strip()
    if lp and ln:
        out["livraison_nom"] = ln if lp in ln else f"{ln} {lp}"
    elif lp or ln:
        out["livraison_nom"] = ln or lp

    fp = str(data.get("facturation_prenom") or p).strip()
    fn = str(data.get("facturation_nom") or gen_nom).strip()
    if fp and fn:
        out["facturation_nom"] = fn if fp in fn else f"{fn} {fp}"
    elif fp or fn:
        out["facturation_nom"] = fn or fp

    lcp = str(data.get("livraison_cp") or "").strip()
    lville = str(data.get("livraison_ville") or "").strip()
    if lcp or lville:
        out["livraison_cp_ville"] = f"{lcp} {lville}".strip()

    fcp = str(data.get("facturation_cp") or "").strip()
    fville = str(data.get("facturation_ville") or "").strip()
    if fcp or fville:
        out["facturation_cp_ville"] = f"{fcp} {fville}".strip()

    nom_ref = fn or ln or n or "Martin"
    prenom_ref = fp or lp or p or "Lucas"
    num_fac = str(data.get("num_facture") or "2027880107").strip()
    init_nom = nom_ref[0].upper() if nom_ref else "M"
    p_upper = re.sub(r"[^A-Za-z]", "", prenom_ref).upper() or "LUCAS"
    computed_nref = f"{num_fac} - {init_nom}{p_upper} -FND"

    curr_nref = str(data.get("nref") or "").strip()
    if not curr_nref or curr_nref.startswith("100110078") or curr_nref == "2027880107 - MLUCAS -FND":
        if nom_ref != "Martin" or prenom_ref != "Lucas" or num_fac != "2027880107":
            out["nref"] = computed_nref
        elif not curr_nref or curr_nref.startswith("100110078"):
            out["nref"] = computed_nref
    elif not curr_nref.startswith(num_fac):
        out["nref"] = computed_nref

    for field_id in FIELDS:
        if field_id in out and not isinstance(out[field_id], bool):
            out[field_id] = clean(field_id, out[field_id])
    if "en_ligne" in out:
        out["en_ligne"] = as_bool(out["en_ligne"], True)
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
    doc.card.en_ligne = as_bool(getattr(doc.card, "en_ligne", True), True)
    cleaned = []
    for item in getattr(doc.card, "items", ())[: layout.MAX_ROWS]:
        payload = {key: getattr(item, key, "") for key in _ITEM_KEYS}
        data = clean_item(payload)
        for key, value in data.items():
            setattr(item, key, value)
        cleaned.append(item)
    doc.card.items = cleaned
    doc.card.total = format_money(grand_total(doc.card))
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
