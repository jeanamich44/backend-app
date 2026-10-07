"""Règles attestation EDF : min/max, charset."""

import re

from . import layout

_FALSE = {"", "0", "false", "off", "no", "n"}
_TRUE = {"1", "true", "on", "yes", "y"}

FIELDS = {
    "civilite": {"min": 0, "max": layout.MAX_CIV, "charset": "text"},
    "nom": {"min": 0, "max": layout.MAX_NOM, "charset": "text"},
    "prenom": {"min": 0, "max": layout.MAX_NOM, "charset": "text"},
    "adresse": {"min": 0, "max": layout.MAX_ADRESSE, "charset": "text"},
    "ville": {"min": 0, "max": layout.MAX_VILLE, "charset": "text"},
    "cp": {"min": 0, "max": layout.MAX_CP, "charset": "text"},
    "num_client": {"min": 0, "max": layout.MAX_CLIENT, "charset": "text"},
    "num_compte": {"min": 0, "max": layout.MAX_COMPTE, "charset": "text"},
    "pdl": {"min": 0, "max": layout.MAX_PDL, "charset": "text"},
    "puissance": {"min": 0, "max": layout.MAX_PUIS, "charset": "text"},
    "date": {"min": 0, "max": layout.MAX_DATE, "charset": "text"},
    "email": {"min": 0, "max": layout.MAX_EMAIL, "charset": "text"},
}

for _key in (
    "contact_titre", "client_side_libelle", "par_internet", "site",
    "app_mobile", "app_nom", "mail_libelle", "par_telephone", "horaires",
    "num_court", "service_appel", "serveur_vocal", "num_vocal", "prix_appel",
    "par_courrier", "courrier_l1", "courrier_l2", "courrier_l3",
    "cheque_titre", "cheque_courrier", "cheque_l1", "cheque_l2",
    "lieu_titre", "titulaire_libelle", "contrat_libelle",
    "n_client_libelle", "n_compte_libelle", "compte_hint1", "compte_hint2",
    "tarif_bleu", "pdl_libelle", "n_pdl", "puissance_libelle", "unite_kva",
    "pour_servir", "cachet_l1", "cachet_l2", "cachet_l3",
    "conseillere", "conseillere_libelle",
):
    FIELDS[_key] = {"min": 0, "max": layout.MAX_CHROME, "charset": "text"}

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


def digits(value: str) -> str:
    return re.sub(r"\D", "", value or "")


def window_lines(card):
    nom = (getattr(card, "nom", "") or "").upper()
    adresse = (getattr(card, "adresse", "") or "").upper()
    cp = getattr(card, "cp", "") or ""
    ville = (getattr(card, "ville", "") or "").upper()
    return nom, adresse, f"{cp} {ville}".strip()


def body_text(card) -> str:
    civ = (getattr(card, "civilite", "") or "").strip()
    nom = (getattr(card, "nom", "") or "").strip()
    who = f"{civ} {nom}".strip()
    adresse = (getattr(card, "adresse", "") or "").strip()
    cp = (getattr(card, "cp", "") or "").strip()
    ville = (getattr(card, "ville", "") or "").strip()
    city = f"{cp} {ville}".strip()
    return (
        f"Par la présente, EDF atteste que {who} est actuellement titulaire "
        f"d'un contrat auprès d'EDF pour le logement situé au {adresse}, "
        f"{city}. Ce contrat a été établi au nom de {who} sur la "
        f"base de ses déclarations."
    )


def _raw(value) -> str:
    if value is None or isinstance(value, bool):
        return ""
    if isinstance(value, (int, float)):
        return str(value)
    return str(value) if isinstance(value, str) else ""


def clean(field_id: str, value, spec=None) -> str:
    spec = spec or FIELDS.get(field_id) or {"max": 80, "charset": "text"}
    text = _raw(value).replace("\r", "").replace("\n", " ").strip()
    return text[: spec["max"]]


def apply_payload(data: dict) -> dict:
    data = as_dict(data)
    out = dict(data)
    if out.get("civilite") == "M.":
        out["civilite"] = "Mr."
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
    if "num_client" in out and out["num_client"]:
        d_client = digits(str(out["num_client"]))
        if len(d_client) == 10:
            out["num_client"] = f"{d_client[0]} {d_client[1:4]} {d_client[4:7]} {d_client[7:10]}"
    if "num_compte" in out and out["num_compte"]:
        d_compte = digits(str(out["num_compte"]))
        if len(d_compte) == 13:
            out["num_compte"] = f"{d_compte[0]} {d_compte[1:3]} {d_compte[3]} {d_compte[4:7]} {d_compte[7]} {d_compte[8:10]} {d_compte[10:13]}"
    if "adresse" in out and isinstance(out["adresse"], str):
        addr = out["adresse"].strip()
        if not out.get("cp") or not out.get("ville"):
            m = re.search(r"\b(\d{5})\s+([A-Za-zÀ-ÿ\- ]+)$", addr)
            if m:
                if not out.get("cp"):
                    out["cp"] = m.group(1)
                if not out.get("ville"):
                    out["ville"] = m.group(2).strip()
                out["adresse"] = addr[: m.start()].strip().rstrip(",")
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
