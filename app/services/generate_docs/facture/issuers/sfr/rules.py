import datetime
import re
from . import layout

# ----------------------------------------------------------------------

_FALSE = {"", "0", "false", "off", "no", "n"}
_TRUE = {"1", "true", "on", "yes", "y"}

# ----------------------------------------------------------------------

FIELDS = {
    "nom": {"min": 0, "max": 70, "charset": "text"},
    "prenom": {"min": 0, "max": 70, "charset": "text"},
    "adresse": {"min": 0, "max": 80, "charset": "text"},
    "cp": {"min": 0, "max": 10, "charset": "text"},
    "ville": {"min": 0, "max": 50, "charset": "text"},
    "service_faq_url": {"min": 0, "max": 50, "charset": "text"},
    "service_phone": {"min": 0, "max": 80, "charset": "text"},
    "service_siege": {"min": 0, "max": 100, "charset": "text"},
    "company_name": {"min": 0, "max": 80, "charset": "text"},
    "company_address": {"min": 0, "max": 80, "charset": "text"},
    "company_capital_rcs": {"min": 0, "max": 80, "charset": "text"},
    "company_tva_ape": {"min": 0, "max": 80, "charset": "text"},
    "titulaire_ligne": {"min": 0, "max": 60, "charset": "upper"},
    "num_compte_client": {"min": 0, "max": 30, "charset": "upper"},
    "date_facture": {"min": 0, "max": 12, "charset": "date"},
    "num_facture": {"min": 0, "max": 30, "charset": "upper"},
    "destinataire_nom": {"min": 0, "max": 60, "charset": "upper"},
    "destinataire_adresse": {"min": 0, "max": 80, "charset": "text"},
    "destinataire_cp_ville": {"min": 0, "max": 60, "charset": "text"},
    "montant_ht": {"min": 0, "max": 20, "charset": "money"},
    "montant_tva": {"min": 0, "max": 20, "charset": "money"},
    "taux_tva": {"min": 0, "max": 15, "charset": "text"},
    "total_ttc": {"min": 0, "max": 20, "charset": "money"},
    "solde_ht": {"min": 0, "max": 20, "charset": "money"},
    "solde_ttc": {"min": 0, "max": 20, "charset": "money"},
    "net_a_payer_ht": {"min": 0, "max": 20, "charset": "money"},
    "net_a_payer_ttc": {"min": 0, "max": 20, "charset": "money"},
    "total_facture_ht": {"min": 0, "max": 20, "charset": "money_plain"},
    "total_facture_ttc": {"min": 0, "max": 20, "charset": "money_plain"},
    "mention_encaissement": {"min": 0, "max": 40, "charset": "text"},
    "footer_note": {"min": 0, "max": 120, "charset": "text"},
    "sepa_ligne1": {"min": 0, "max": 140, "charset": "text"},
    "sepa_ligne2": {"min": 0, "max": 140, "charset": "text"},
}

ITEM_FIELDS = {
    "numero_ligne": {"min": 0, "max": 30, "charset": "text"},
    "description": {"min": 0, "max": 100, "charset": "text"},
    "date": {"min": 0, "max": 15, "charset": "date"},
    "montant_ttc": {"min": 0, "max": 20, "charset": "money"},
}

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

def clean_date(value) -> str:
    text = _raw(value).strip()
    match_iso = re.match(r"^(\d{4})[./-](\d{1,2})[./-](\d{1,2})$", text)
    if match_iso:
        y, m, d = int(match_iso.group(1)), int(match_iso.group(2)), int(match_iso.group(3))
        return f"{y:04d}-{m:02d}-{d:02d}"
    match_fr = re.match(r"^(\d{1,2})[./-](\d{1,2})[./-](\d{2,4})$", text)
    if match_fr:
        d, m, y = int(match_fr.group(1)), int(match_fr.group(2)), int(match_fr.group(3))
        if y < 100:
            y += 2000
        return f"{y:04d}-{m:02d}-{d:02d}"
    digits = re.sub(r"\D", "", text)
    if len(digits) == 8:
        if digits.startswith("20") or digits.startswith("19"):
            return f"{int(digits[:4]):04d}-{int(digits[4:6]):02d}-{int(digits[6:]):02d}"
        return f"{int(digits[4:]):04d}-{int(digits[2:4]):02d}-{int(digits[:2]):02d}"
    return text[:12]

# ----------------------------------------------------------------------

def compute_sepa_date(date_str: str) -> str:
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", date_str)
    if not m:
        return date_str
    y, month, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if month == 12:
        y += 1
        month = 1
    else:
        month += 1
    return f"{y:04d}-{month:02d}-{d:02d}"

# ----------------------------------------------------------------------

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

# ----------------------------------------------------------------------

def format_money_sfr(value: float) -> str:
    val = round(value, 2)
    if val == int(val):
        return str(int(val))
    s = f"{val:.2f}"
    if s.endswith("0"):
        s = s[:-1]
    return s

# ----------------------------------------------------------------------

def format_euro(value: float) -> str:
    return f"{format_money_sfr(value)}€"

# ----------------------------------------------------------------------

def parse_rate(value) -> float:
    text = _raw(value).strip().replace("%", "").strip()
    try:
        return float(text)
    except ValueError:
        return 20.0

# ----------------------------------------------------------------------

def invoice_totals(items, taux_tva: str = "20.0 %", solde_ht_val: float = 0.0, solde_ttc_val: float = 0.0) -> dict:
    total_ttc = round(sum(parse_money(getattr(it, "montant_ttc", 0) if hasattr(it, "montant_ttc") else it.get("montant_ttc", 0)) for it in (items or ())), 2)
    rate = parse_rate(taux_tva)
    if solde_ttc_val != 0.0 and solde_ht_val == 0.0:
        solde_ht_val = round(solde_ttc_val / (1.0 + rate / 100.0), 2)
    montant_ht = round(total_ttc / (1.0 + rate / 100.0), 2)
    montant_tva = round(total_ttc - montant_ht, 2)
    net_ht = round(montant_ht - solde_ht_val, 2)
    net_ttc = round(total_ttc - solde_ttc_val, 2)
    return {
        "total_ttc": format_euro(total_ttc),
        "montant_ht": format_euro(montant_ht),
        "montant_tva": format_euro(montant_tva),
        "solde_ht": format_euro(solde_ht_val),
        "solde_ttc": format_euro(solde_ttc_val),
        "net_a_payer_ht": format_euro(net_ht),
        "net_a_payer_ttc": format_euro(net_ttc),
        "total_facture_ht": format_money_sfr(montant_ht),
        "total_facture_ttc": format_money_sfr(total_ttc),
    }

# ----------------------------------------------------------------------

def clean(field_id: str, value, spec=None) -> str:
    spec = spec or FIELDS.get(field_id) or {"max": 120, "charset": "text"}
    text = _raw(value)
    charset = spec.get("charset")
    if charset == "date":
        text = clean_date(text)
    elif charset == "upper":
        text = re.sub(r"\s+", " ", text).strip().upper()
    elif charset == "money":
        val = parse_money(text)
        text = format_euro(val) if text.strip() else ""
    elif charset == "money_plain":
        val = parse_money(text)
        text = format_money_sfr(val) if text.strip() else ""
    else:
        text = text.replace("\r", "").replace("\n", " ").strip()
    return text[: spec["max"]]

# ----------------------------------------------------------------------

def clean_item(item: dict) -> dict:
    item = as_dict(item)
    out = {}
    for k, sp in ITEM_FIELDS.items():
        out[k] = clean(k, item.get(k, ""), sp)
    desc = out.get("description", "")
    m_ttc = out.get("montant_ttc", "")
    has_custom_desc = "description" in item and bool(item["description"])
    has_custom_m = "montant_ttc" in item and bool(item["montant_ttc"])
    if desc:
        match_desc = re.search(r":\s*(\d+(?:[.,]\d+)?)\s*€?", desc)
        if has_custom_m:
            val = parse_money(m_ttc)
            if val > 0 and match_desc:
                sfr_val = format_money_sfr(val)
                if "," in match_desc.group(1):
                    sfr_val = sfr_val.replace(".", ",")
                out["description"] = re.sub(r":\s*\d+(?:[.,]\d+)?\s*€?", f": {sfr_val} €", desc)
        elif has_custom_desc and match_desc:
            val = parse_money(match_desc.group(1))
            if val > 0:
                out["montant_ttc"] = format_euro(val)
        elif m_ttc and match_desc:
            val = parse_money(m_ttc)
            if val > 0:
                sfr_val = format_money_sfr(val)
                if "," in match_desc.group(1):
                    sfr_val = sfr_val.replace(".", ",")
                out["description"] = re.sub(r":\s*\d+(?:[.,]\d+)?\s*€?", f": {sfr_val} €", desc)
    return out

# ----------------------------------------------------------------------

def apply_payload(data: dict | None) -> dict:
    data = as_dict(data)
    out = dict(data)
    prenom = str(data.get("prenom") or "").strip()
    nom = str(data.get("nom") or "").strip()
    adresse = str(data.get("adresse") or "").strip()
    cp = str(data.get("cp") or "").strip()
    ville = str(data.get("ville") or "").strip()

    if prenom and nom:
        full = f"{prenom.upper()} {nom.upper()}"
        out["destinataire_nom"] = full
        out["titulaire_ligne"] = full
    elif nom:
        out["destinataire_nom"] = nom.upper()
        out["titulaire_ligne"] = nom.upper()
    elif prenom:
        out["destinataire_nom"] = prenom.upper()
        out["titulaire_ligne"] = prenom.upper()

    if adresse:
        out["destinataire_adresse"] = adresse

    if cp or ville:
        out["destinataire_cp_ville"] = f"{cp} {ville}".strip()

    for fid in FIELDS:
        if fid in out and not isinstance(out[fid], bool):
            out[fid] = clean(fid, out[fid])
    raw_items = out.get("items")
    if isinstance(raw_items, list):
        items = []
        for it in raw_items[: layout.MAX_ITEMS]:
            if isinstance(it, dict):
                items.append(clean_item(it))
        out["items"] = items
    return out

# ----------------------------------------------------------------------

def apply_doc(doc):
    card = doc.card
    nom = getattr(card, "nom", "") or ""
    prenom = getattr(card, "prenom", "") or ""
    if prenom and nom:
        full = f"{prenom.upper()} {nom.upper()}"
        card.destinataire_nom = full
        card.titulaire_ligne = full
    elif nom:
        card.destinataire_nom = nom.upper()
        card.titulaire_ligne = nom.upper()
    elif prenom:
        card.destinataire_nom = prenom.upper()
        card.titulaire_ligne = prenom.upper()
    elif not card.destinataire_nom:
        card.destinataire_nom = "LUCAS MARTIN"
        card.titulaire_ligne = "LUCAS MARTIN"

    if not card.titulaire_ligne and card.destinataire_nom:
        card.titulaire_ligne = card.destinataire_nom

    adresse = getattr(card, "adresse", "") or ""
    if adresse:
        card.destinataire_adresse = adresse

    cp = getattr(card, "cp", "") or ""
    ville = getattr(card, "ville", "") or ""
    if cp or ville:
        card.destinataire_cp_ville = f"{cp} {ville}".strip()

    card.date_facture = clean_date(card.date_facture)

    for fid in FIELDS:
        if hasattr(card, fid):
            val = getattr(card, fid)
            setattr(card, fid, clean(fid, val))

    cleaned = []
    for it in card.items[: layout.MAX_ITEMS]:
        payload = {k: getattr(it, k, "") for k in ITEM_FIELDS}
        d = clean_item(payload)
        if not d.get("date") and card.date_facture:
            d["date"] = card.date_facture
        for k, v in d.items():
            setattr(it, k, v)
        cleaned.append(it)
    card.items = cleaned

    if card.items:
        s_ht = parse_money(card.solde_ht)
        s_ttc = parse_money(card.solde_ttc)
        calcs = invoice_totals(card.items, card.taux_tva, s_ht, s_ttc)
        card.montant_ht = calcs["montant_ht"]
        card.montant_tva = calcs["montant_tva"]
        card.total_ttc = calcs["total_ttc"]
        card.solde_ht = calcs["solde_ht"]
        card.solde_ttc = calcs["solde_ttc"]
        card.net_a_payer_ht = calcs["net_a_payer_ht"]
        card.net_a_payer_ttc = calcs["net_a_payer_ttc"]
        card.total_facture_ht = calcs["total_facture_ht"]
        card.total_facture_ttc = calcs["total_facture_ttc"]

    if card.num_compte_client and card.date_facture:
        sepa_date = compute_sepa_date(card.date_facture)
        card.sepa_ligne2 = f"conformément à votre Mandat de prélèvement SEPA référencé {card.num_compte_client}-00000 le {sepa_date}."

    return doc

# ----------------------------------------------------------------------

def public_rules() -> dict:
    out = {
        fid: {"min": sp["min"], "max": sp["max"], "charset": sp["charset"]}
        for fid, sp in FIELDS.items()
    }
    out["items"] = {
        k: {"min": sp["min"], "max": sp["max"], "charset": sp["charset"]}
        for k, sp in ITEM_FIELDS.items()
    }
    return out

# ----------------------------------------------------------------------

def public_limits() -> dict:
    limits = {fid: sp["max"] for fid, sp in FIELDS.items()}
    limits["max_items"] = layout.MAX_ITEMS
    limits.update({f"item_{k}": sp["max"] for k, sp in ITEM_FIELDS.items()})
    return limits
