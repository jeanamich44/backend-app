"""Règles Engie Gaz : titulaire CAPITALES, rues selon bloc, ids chiffres."""

import re

from . import copy as texts
from . import layout

_FALSE = {"", "0", "false", "off", "no", "n"}
_TRUE = {"1", "true", "on", "yes", "y"}

FIELDS = {
    "civilite": {"min": 0, "max": 10, "charset": "text"},
    "nom": {"min": 0, "max": layout.MAX_NOM, "charset": "text"},
    "adresse": {"min": 0, "max": layout.MAX_ADRESSE, "charset": "text"},
    "cp_ville": {"min": 0, "max": layout.MAX_CP_VILLE, "charset": "text"},
    "date_facture": {"min": 0, "max": layout.MAX_DATE, "charset": "date"},
    "num_facture": {"min": 0, "max": layout.MAX_FACTURE, "charset": "digits"},
    "num_client": {"min": 0, "max": layout.MAX_CLIENT, "charset": "digits"},
    "num_contrat": {"min": 0, "max": layout.MAX_CONTRAT, "charset": "digits"},
    "lieu_pce": {"min": 0, "max": layout.MAX_LIEU, "charset": "text"},
    "lieu_bat": {"min": 0, "max": layout.MAX_LIEU, "charset": "text"},
    "montant_gaz": {"min": 0, "max": layout.MAX_MONTANT, "charset": "euro"},
    "montant_prestations": {"min": 0, "max": layout.MAX_MONTANT, "charset": "euro"},
    "total": {"min": 0, "max": layout.MAX_MONTANT, "charset": "euro"},
    "montant_ht": {"min": 0, "max": layout.MAX_MONTANT, "charset": "euro"},
    "montant_tva": {"min": 0, "max": layout.MAX_MONTANT, "charset": "euro"},
    "compte": {"min": 0, "max": layout.MAX_COMPTE, "charset": "text"},
}

_DOC_ATTR = {key: ("card", key) for key in FIELDS}


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


def digits(value) -> str:
    return re.sub(r"\D", "", _raw(value))


def group3(value: str) -> str:
    raw = digits(value)
    if not raw:
        return ""
    return " ".join(raw[i:i + 3] for i in range(0, len(raw), 3))


def format_nom(name: str) -> str:
    text = re.sub(r"\s+", " ", _raw(name)).strip()
    text = re.sub(
        r"^(mme\.?|madame|mlle\.?|mademoiselle|m\.|mr\.?|monsieur)\s+",
        "", text, flags=re.I,
    )
    return text.upper()


def format_titulaire(name: str, civ: str = "") -> str:
    text = format_nom(name)
    if not text:
        return ""
    c = _raw(civ).strip().upper().rstrip(".")
    if not c:
        c = texts.CIVILITY.strip()
    if c == "MR":
        c = "M"
    return f"{c} {text}".strip()


def format_window_street(value: str) -> str:
    text = re.sub(r"\s+", " ", _raw(value)).strip().upper()
    text = re.sub(r"^(\d+)\s*,\s*", r"\1 ", text)
    return text


def format_lieu_street(value: str) -> str:
    text = re.sub(r"\s+", " ", _raw(value)).strip().upper()
    match = re.match(r"^(\d+)\s*,?\s+(.*)$", text)
    if match and match.group(2):
        return f"{match.group(1)}, {match.group(2)}"
    return text


def window_lines(card) -> tuple:
    lines = (
        format_titulaire(getattr(card, "nom", ""), getattr(card, "civilite", "")),
        format_window_street(getattr(card, "adresse", "")),
        format_window_street(getattr(card, "cp_ville", "")),
    )
    return tuple(line for line in lines if line)


def lieu_lines(card) -> tuple:
    return (
        _raw(getattr(card, "lieu_pce", "")).strip(),
        _raw(getattr(card, "lieu_bat", "")).strip(),
        format_lieu_street(getattr(card, "adresse", "")),
        format_window_street(getattr(card, "cp_ville", "")),
    )


def client_value(card) -> str:
    grouped = group3(getattr(card, "num_client", ""))
    return f" {grouped}" if grouped else ""


def contrat_value(card) -> str:
    return group3(getattr(card, "num_contrat", ""))


def banner_meta(card) -> str:
    date = _raw(getattr(card, "date_facture", "")).strip()
    num = group3(getattr(card, "num_facture", ""))
    if not date and not num:
        return ""
    return f" DU {date} N° {num}"


def barcode_value(card) -> str:
    facture = digits(getattr(card, "num_facture", "")).zfill(layout.MAX_FACTURE)
    client = digits(getattr(card, "num_client", "")).zfill(layout.MAX_CLIENT)
    if not facture.strip("0") and not client.strip("0"):
        return ""
    return f"ZISUBILL{facture}0{client}"


def clean_date(value) -> str:
    text = _raw(value).strip()
    match = re.match(r"^(\d{1,2})[./-](\d{1,2})[./-](\d{2,4})$", text)
    if match:
        day, month, year = int(match.group(1)), int(match.group(2)), match.group(3)
        if len(year) == 4:
            year = year[-2:]
        return f"{day:02d}/{month:02d}/{year}"
    return text[: layout.MAX_DATE]


def clean(field_id: str, value, spec=None) -> str:
    spec = spec or FIELDS.get(field_id) or {"max": 80, "charset": "text"}
    text = _raw(value).replace("\r", "").replace("\n", " ").strip()
    charset = spec.get("charset")
    if charset == "digits":
        text = digits(text)
    elif charset == "date":
        text = clean_date(text)
    elif charset == "euro":
        text = clean_euro(text)
    return text[: spec["max"]]


def parse_cents(value) -> int | None:
    text = re.sub(r"[^\d,.\-]", "", _raw(value))
    if not text or text in {",", ".", "-", "-.", "-,"}:
        return None
    if "," in text and "." in text:
        text = text.replace(".", "").replace(",", ".")
    elif "," in text:
        text = text.replace(",", ".")
    try:
        return int(round(float(text) * 100))
    except ValueError:
        return None


def clean_euro(value) -> str:
    cents = parse_cents(value)
    if cents is None:
        return ""
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}{cents // 100},{cents % 100:02d}"


def format_euro(value) -> str:
    text = clean_euro(value)
    return f"{text} €" if text else ""


def format_ttc(card) -> str:
    total_val = getattr(card, "total", "")
    if total_val:
        cents = parse_cents(total_val)
        if cents is not None:
            sign = "-" if cents < 0 else ""
            c = abs(cents)
            return f"{sign}{c // 100},{c % 100:02d} €"
    gaz = parse_cents(getattr(card, "montant_gaz", ""))
    prest = parse_cents(getattr(card, "montant_prestations", ""))
    if gaz is None and prest is None:
        return ""
    total = (gaz or 0) + (prest or 0)
    sign = "-" if total < 0 else ""
    total = abs(total)
    return f"{sign}{total // 100},{total % 100:02d} €"


def _date_parts(card):
    text = clean_date(getattr(card, "date_facture", ""))
    match = re.match(r"^(\d{2})/(\d{2})/(\d{2})$", text)
    if not match:
        return None
    day, month, year = int(match.group(1)), int(match.group(2)), int(match.group(3))
    return day, month, 2000 + year


def next_invoice_line(card) -> str:
    parts = _date_parts(card)
    if not parts:
        return ""
    day, month, year = parts
    month += 1
    if month == 13:
        month, year = 1, year + 1
    return f"autour du {day} {texts.MONTHS_FR[month - 1]} {year}"


def each_month_line(card) -> str:
    parts = _date_parts(card)
    if not parts:
        return ""
    return f"autour du {parts[0]} de chaque mois"


def preleve_line(card) -> str:
    date = _raw(getattr(card, "date_facture", "")).strip()
    return f"(PRELEVE LE {date})" if date else ""


def echeance_line(card) -> str:
    date = _raw(getattr(card, "date_facture", "")).strip()
    return f" (échéance au {date})" if date else ""


def hors_tva_line(card) -> str:
    ht = format_euro(getattr(card, "montant_ht", ""))
    return f"Dont Total hors TVA ({ht})" if ht else ""


def tva_line(card) -> str:
    tva = format_euro(getattr(card, "montant_tva", ""))
    return f"Dont Total TVA ({tva})" if tva else ""


def apply_payload(data: dict) -> dict:
    data = as_dict(data)
    out = dict(data)
    civilite = str(data.get("civilite") or "").strip()
    if civilite:
        out["civilite"] = civilite
    prenom = str(data.get("prenom") or "").strip()
    nom = str(data.get("nom") or "").strip()
    if prenom and nom:
        out["nom"] = f"{nom.upper()} {prenom.upper()}" if prenom.upper() not in nom.upper() else nom.upper()
    elif nom:
        out["nom"] = nom.upper()
    elif prenom:
        out["nom"] = prenom.upper()
    cp = str(data.get("cp") or "").strip()
    ville = str(data.get("ville") or "").strip()
    if cp or ville:
        out["cp_ville"] = f"{cp} {ville}".strip().upper()
    for field_id in FIELDS:
        if field_id in out and not isinstance(out[field_id], bool):
            out[field_id] = clean(field_id, out[field_id])
    return out


def apply_doc(doc):
    for field_id, (group, attr) in _DOC_ATTR.items():
        obj = getattr(doc, group)
        setattr(obj, attr, clean(field_id, getattr(obj, attr)))
    return doc


def public_rules() -> dict:
    return {
        field_id: {"min": spec["min"], "max": spec["max"], "charset": spec["charset"]}
        for field_id, spec in FIELDS.items()
    }


def public_limits() -> dict:
    return {field_id: spec["max"] for field_id, spec in FIELDS.items()}
