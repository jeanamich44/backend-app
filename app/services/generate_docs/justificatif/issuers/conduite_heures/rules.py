"""Règles justificatif heures : jour 3 lettres, date, heures."""

import re
import unicodedata

from . import layout

_FALSE = {"", "0", "false", "off", "no", "n"}
_TRUE = {"1", "true", "on", "yes", "y"}

_JOUR_MAP = {
    "lundi": "Lun.",
    "lun": "Lun.",
    "mardi": "Mar.",
    "mar": "Mar.",
    "mercredi": "Mer.",
    "mer": "Mer.",
    "jeudi": "Jeu.",
    "jeu": "Jeu.",
    "vendredi": "Ven.",
    "ven": "Ven.",
    "samedi": "Sam.",
    "sam": "Sam.",
    "dimanche": "Dim.",
    "dim": "Dim.",
}

FIELDS = {
    "nom": {"min": 0, "max": 40, "charset": "text"},
    "prenom": {"min": 0, "max": 40, "charset": "text"},
    "num_eleve": {"min": 0, "max": 20, "charset": "digits"},
    "eleve": {"min": 0, "max": layout.MAX_ELEVE, "charset": "text"},
    "edition_date": {"min": 0, "max": layout.MAX_DATE, "charset": "date"},
    "edition_time": {"min": 0, "max": layout.MAX_TIME, "charset": "time"},
    "edition": {"min": 0, "max": layout.MAX_EDITION, "charset": "text"},
}
for _i in range(1, layout.MAX_ROWS + 1):
    FIELDS[f"rdv{_i}_jour"] = {"min": 0, "max": layout.MAX_JOUR, "charset": "jour"}
    FIELDS[f"rdv{_i}_date"] = {"min": 0, "max": layout.MAX_DATE, "charset": "date"}
    FIELDS[f"rdv{_i}_debut"] = {"min": 0, "max": layout.MAX_TIME, "charset": "time"}
    FIELDS[f"rdv{_i}_fin"] = {"min": 0, "max": layout.MAX_TIME, "charset": "time"}
    FIELDS[f"rdv{_i}_activite"] = {"min": 0, "max": layout.MAX_ACTIVITE, "charset": "text"}
    FIELDS[f"rdv{_i}_commentaire"] = {"min": 0, "max": layout.MAX_COMMENT, "charset": "text"}


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


def _fold(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return text.lower()


def _raw(value) -> str:
    if value is None or isinstance(value, bool):
        return ""
    if isinstance(value, (int, float)):
        text = str(value)
    elif isinstance(value, str):
        text = value
    else:
        return ""
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\u00a0", " ").replace("\u202f", " ")
    return re.sub(r"[\x00-\x09\x0b-\x1f\x7f]", " ", text)


def clean_jour(value) -> str:
    token = re.sub(r"[^a-z]", "", _fold(_raw(value).split()[0] if _raw(value).strip() else ""))
    if not token:
        return ""
    for name in sorted(_JOUR_MAP, key=len, reverse=True):
        if token == name or (len(name) >= 3 and token.startswith(name)):
            return _JOUR_MAP[name]
    return ""


def clean_date(value) -> str:
    parts = re.findall(r"\d+", _raw(value))
    if not parts:
        return ""
    if len(parts) == 1:
        digits = parts[0][:8]
        if len(digits) <= 2:
            return digits
        if len(digits) <= 4:
            return digits[:2] + "/" + digits[2:]
        day, month, year = digits[:2], digits[2:4], digits[4:]
        parts = [day, month, year]
    day = parts[0][:2]
    month = parts[1][:2] if len(parts) > 1 else ""
    if len(parts) == 2:
        if len(day) == 2 and len(month) == 2:
            d, m = int(day), int(month)
            d = max(1, min(d, 31))
            m = max(1, min(m, 12))
            return f"{d:02d}/{m:02d}"
        return f"{day}/{month}"
    year = parts[2][:4]
    if len(year) == 2:
        year = "20" + year
    d, m = int(day or 1), int(month or 1)
    d = max(1, min(d, 31))
    m = max(1, min(m, 12))
    if len(year) < 4:
        return f"{d:02d}/{m:02d}/{year}"
    return f"{d:02d}/{m:02d}/{year}"


def clean_time(value) -> str:
    text = re.sub(r"[^0-9:]", "", _raw(value))
    if ":" in text:
        left, _, right = text.partition(":")
        hours = re.sub(r"[^0-9]", "", left)[:2]
        mins = re.sub(r"[^0-9]", "", right)[:2]
        if not hours:
            return ""
        if not mins:
            return hours
        if len(mins) < 2:
            return f"{hours}:{mins}"
        hh = min(int(hours), 23)
        mm = min(int(mins), 59)
        return f"{hh:02d}:{mm:02d}"
    digits = re.sub(r"[^0-9]", "", text)[:4]
    if len(digits) < 4:
        return digits
    hh = min(int(digits[:2]), 23)
    mm = min(int(digits[2:]), 59)
    return f"{hh:02d}:{mm:02d}"


def split_jour_date(value) -> tuple[str, str]:
    text = _raw(value).strip()
    if not text:
        return "", ""
    match = re.search(r"\d", text)
    if not match:
        return text, ""
    return text[: match.start()], text[match.start() :]


def clean(field_id: str, value) -> str:
    spec = FIELDS.get(field_id)
    text = _raw(value)
    if spec is None:
        return re.sub(r" +", " ", text).strip()
    kind = spec["charset"]
    if kind == "jour":
        return clean_jour(text)
    if kind == "date":
        return clean_date(text)
    if kind == "time":
        return clean_time(text)
    text = re.sub(r" +", " ", text).strip()
    max_n = spec["max"]
    if max_n is not None:
        text = text[:max_n]
    return text


def _clean_rdv_item(item: dict) -> dict:
    jour = item.get("jour")
    date = item.get("date")
    if not jour:
        left, right = split_jour_date(date or "")
        if clean_jour(left):
            jour, date = left, right
    else:
        left, right = split_jour_date(date or "")
        if clean_jour(left) and right:
            date = right
    return {
        "jour": clean("rdv1_jour", jour),
        "date": clean("rdv1_date", date),
        "debut": clean("rdv1_debut", item.get("debut")),
        "fin": clean("rdv1_fin", item.get("fin")),
        "activite": clean("rdv1_activite", item.get("activite")),
        "commentaire": clean("rdv1_commentaire", item.get("commentaire")),
    }


def apply_payload(data: dict) -> dict:
    data = as_dict(data)
    out = dict(data)
    if any(k in out for k in ("nom", "prenom", "num_eleve")):
        nom = str(out.get("nom") or "").strip()
        prenom = str(out.get("prenom") or "").strip()
        num = re.sub(r"[^0-9A-Za-z-]", "", str(out.get("num_eleve") or "").strip())
        name_parts = []
        if nom:
            name_parts.append(nom.capitalize() if nom.islower() else nom)
        if prenom:
            name_parts.append(prenom.upper())
        name_str = " ".join(name_parts)
        if num:
            out["eleve"] = f"{name_str} [{num}]".strip() if name_str else f"[{num}]"
        elif name_str:
            out["eleve"] = name_str
    elif "eleve" in out and out["eleve"]:
        raw_eleve = str(out["eleve"]).strip()
        m = re.match(r"^(.*?)\s*\[?([0-9A-Za-z-]+)\]?$", raw_eleve)
        if m and not raw_eleve.endswith("]"):
            base_name, n_code = m.group(1).strip(), m.group(2).strip()
            if base_name and n_code:
                out["eleve"] = f"{base_name} [{n_code}]"

    if "edition_date" in out or "edition_time" in out:
        e_date = clean_date(out.get("edition_date") or "")
        e_time = clean_time(out.get("edition_time") or "")
        if e_date and e_time:
            out["edition"] = f"{e_date} {e_time}"
        elif e_date:
            out["edition"] = e_date
        elif e_time:
            out["edition"] = e_time

    for i in range(layout.MAX_ROWS):
        n = i + 1
        day_key = f"rdv{n}_date"
        jour_key = f"rdv{n}_jour"
        if day_key in out and jour_key not in out:
            left, right = split_jour_date(out[day_key])
            if clean_jour(left):
                out[jour_key] = left
                out[day_key] = right
    for field_id in FIELDS:
        if field_id in out and not isinstance(out[field_id], bool):
            out[field_id] = clean(field_id, out[field_id])
    raw = out.get("rdvs")
    if isinstance(raw, list):
        rows = []
        for item in raw[: layout.MAX_ROWS]:
            if isinstance(item, dict):
                rows.append(_clean_rdv_item(item))
        out["rdvs"] = rows
    return out


def apply_doc(doc):
    card = doc.card
    card.eleve = clean("eleve", card.eleve)
    card.edition = clean("edition", card.edition)
    card.rdvs = list(card.rdvs[: layout.MAX_ROWS])
    for i, rdv in enumerate(card.rdvs):
        cleaned = _clean_rdv_item({
            "jour": getattr(rdv, "jour", ""),
            "date": rdv.date,
            "debut": rdv.debut,
            "fin": rdv.fin,
            "activite": rdv.activite,
            "commentaire": rdv.commentaire,
        })
        rdv.jour = cleaned["jour"]
        rdv.date = cleaned["date"]
        rdv.debut = cleaned["debut"]
        rdv.fin = cleaned["fin"]
        rdv.activite = cleaned["activite"]
        rdv.commentaire = cleaned["commentaire"]
    return doc


def public_rules() -> dict:
    return {
        field_id: {"min": spec["min"], "max": spec["max"], "charset": spec["charset"]}
        for field_id, spec in FIELDS.items()
    }


def public_limits() -> dict:
    limits = {field_id: spec["max"] for field_id, spec in FIELDS.items()}
    limits["max_rows"] = layout.MAX_ROWS
    return limits
