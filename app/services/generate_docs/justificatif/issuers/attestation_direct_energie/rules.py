"""Règles Direct Energie : titulaire gabarit (M. + CAPITALES), rues CAPITALES."""

import re

from . import copy as texts
from . import layout

_FALSE = {"", "0", "false", "off", "no", "n"}
_TRUE = {"1", "true", "on", "yes", "y"}

FIELDS = {
    "civilite": {"min": 0, "max": layout.MAX_NOM, "charset": "text"},
    "nom": {"min": 0, "max": layout.MAX_NOM, "charset": "text"},
    "prenom": {"min": 0, "max": layout.MAX_NOM, "charset": "text"},
    "adresse": {"min": 0, "max": layout.MAX_ADRESSE, "charset": "text"},
    "cp": {"min": 0, "max": 10, "charset": "text"},
    "ville": {"min": 0, "max": layout.MAX_CP_VILLE, "charset": "text"},
    "cp_ville": {"min": 0, "max": layout.MAX_CP_VILLE, "charset": "text"},
    "date": {"min": 0, "max": layout.MAX_DATE, "charset": "text"},
    "num_client": {"min": 0, "max": layout.MAX_CLIENT, "charset": "digits"},
    "depuis": {"min": 0, "max": layout.MAX_DEPUIS, "charset": "text"},
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


def format_nom(name: str) -> str:
    text = re.sub(r"\s+", " ", _raw(name)).strip()
    text = re.sub(
        r"^(mme\.?|madame|mlle\.?|mademoiselle|m\.|mr\.?|monsieur)\s+",
        "", text, flags=re.I,
    )
    return text.upper()


def format_titulaire(name: str) -> str:
    text = format_nom(name)
    if not text:
        return ""
    return texts.CIVILITY + text


def format_street(value: str) -> str:
    return _raw(value).upper()


def window_lines(card) -> tuple:
    cp_ville = getattr(card, "cp_ville", "") or f"{getattr(card, 'cp', '')} {getattr(card, 'ville', '')}".strip()
    civ = getattr(card, "civilite", None)
    if civ is not None:
        civ_clean = str(civ).strip()
        civ_prefix = f"{civ_clean} " if civ_clean else ""
        first_line = civ_prefix + format_nom(getattr(card, "nom", ""))
    else:
        first_line = format_titulaire(getattr(card, "nom", ""))
    lines = (
        first_line,
        format_street(getattr(card, "adresse", "")),
        format_street(cp_ville),
    )
    return tuple(line for line in lines if line)


def body_lines(card) -> tuple:
    cp_ville = getattr(card, "cp_ville", "") or f"{getattr(card, 'cp', '')} {getattr(card, 'ville', '')}".strip()
    lines = (
        format_nom(getattr(card, "nom", "")),
        format_street(getattr(card, "adresse", "")),
        format_street(cp_ville),
    )
    return tuple(line for line in lines if line)


def clean(field_id: str, value, spec=None) -> str:
    spec = spec or FIELDS.get(field_id) or {"max": 80, "charset": "text"}
    text = _raw(value).replace("\r", "").replace("\n", " ").strip()
    charset = spec.get("charset")
    if charset == "digits":
        text = re.sub(r"\D", "", text)
    return text[: spec["max"]]


def apply_payload(data: dict) -> dict:
    data = as_dict(data)
    out = dict(data)
    if "civilite" in out and isinstance(out["civilite"], str):
        c_val = out["civilite"].strip()
        if c_val == "Mr.":
            c_val = "M."
        out["civilite"] = c_val
    if "prenom" in out and isinstance(out["prenom"], str):
        p_val = out["prenom"].strip()
        p_val = re.sub(
            r"^(?:mr\.|mr|m\.|monsieur|mme\.|mme|madame|mlle\.|mlle|mle)\s+",
            "",
            p_val,
            flags=re.IGNORECASE,
        ).strip()
        out["prenom"] = p_val
    if "nom" in out and isinstance(out["nom"], str):
        nom_val = out["nom"].strip()
        cleaned_nom = re.sub(
            r"^(?:mr\.|mr|m\.|monsieur|mme\.|mme|madame|mlle\.|mlle|mle|mr\.?\s*et\s*mme\.?|mr\.?\s*ou\s*mme\.?)\s+",
            "",
            nom_val,
            flags=re.IGNORECASE,
        ).strip()
        prenom_val = str(out.get("prenom") or "").strip()
        if prenom_val and prenom_val.lower() not in cleaned_nom.lower():
            out["nom"] = f"{cleaned_nom} {prenom_val}".strip()
        elif cleaned_nom:
            out["nom"] = cleaned_nom
    cp_val = str(out.get("cp") or "").strip()
    ville_val = str(out.get("ville") or "").strip()
    if cp_val and ville_val:
        out["cp_ville"] = f"{cp_val} {ville_val}".strip()
    elif cp_val and not out.get("cp_ville"):
        out["cp_ville"] = cp_val
    elif ville_val and not out.get("cp_ville"):
        out["cp_ville"] = ville_val
    elif not out.get("cp_ville") and "adresse" in out and isinstance(out["adresse"], str):
        addr = out["adresse"].strip()
        m = re.search(r"\b(\d{5})\s+([A-Za-zÀ-ÿ\- ]+)$", addr)
        if m:
            if not out.get("cp"):
                out["cp"] = m.group(1)
            if not out.get("ville"):
                out["ville"] = m.group(2).strip()
            out["cp_ville"] = f"{m.group(1)} {m.group(2).strip()}".strip()
            out["adresse"] = addr[: m.start()].strip().rstrip(",")
    if not cp_val and not ville_val and out.get("cp_ville"):
        m = re.match(r"^(\d{5})\s+(.+)$", str(out["cp_ville"]).strip())
        if m:
            out["cp"] = m.group(1)
            out["ville"] = m.group(2).strip()
    if "date" in out and out["date"]:
        d_val = str(out["date"]).strip()
        if d_val and not re.match(r"^[a-zA-ZÀ-ÿ\s'-]+,\s*le\s*", d_val, re.IGNORECASE):
            out["date"] = f"Paris, le {d_val}"
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
